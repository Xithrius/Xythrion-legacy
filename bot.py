"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import collections
import sqlite3
import json
import os
import asyncio
import aiohttp

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, now, printc, create_table, progress_bar


class Robot(comms.Bot):
    """ """

    def __init__(self, *args, **kwargs):
        """ Objects:
        Passing *args and **kwargs into comms.Bot
        Creating background task for checking services
        Creating requests database path
        """
        super().__init__(*args, **kwargs)

        self.db_path = path('repository', 'database', 'user_requests.db')

        self.create_Attributes()

        if not os.path.isfile(self.db_path):
            self.create_RequestsDB()

        self.background_services = self.loop.create_task(self.load_services())

    """ Preparing bot databases """

    def create_RequestsDB(self):
        """ Creation of the requesting database if it does not exist """
        possible_services = ', '.join(str(y) for y in [f'{k} TEXT' for k, v in self.services.items()])
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute(f'''CREATE TABLE RequestsDB (id INTEGER NOT NULL PRIMARY KEY UNIQUE, {possible_services})''')
        self.conn.commit()
        self.conn.close()

    def create_Attributes(self):
        """ """
        with open(path('handlers', 'configuration', 'config.json'), "r") as f:
            self.config = json.load(f)
            self.services = {k: False for k in self.config['services'].keys()}
            self.tokens = self.config['services']
            self.__version__ = 'v0.0.1'

    def cog_unload(self):
        """ Cancel background task(s) when cog is unloaded """
        self.background_services.cancel()

    async def load_services(self):
        await self.wait_until_ready()
        while not self.is_closed():

            """ Weather """
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={12345}&country=US&key={self.tokens["weather"]}') as test_response:
                    if test_response.status == 200:
                        if not self.services['weather']:
                            printc('[ ! ]: WEATHER SERVICE AVAILABLE')
                        self.services['weather'] = True
                    else:
                        printc(f'WARNING: WEATHER SERVICE NOT AVAILABLE: {test_response.status}')

            """ Reddit """

            f = self.tokens['reddit']
            self.client_auth = aiohttp.BasicAuth(login=f['ID'], password=f['secret'])
            post_data = {"grant_type": "password", "username": f['username'], "password": f['password']}
            headers = {"User-Agent": f"Xylene/{self.__version__} by {f['username']}"}
            async with aiohttp.ClientSession(auth=self.client_auth, headers=headers) as session:
                async with session.post("https://www.reddit.com/api/v1/access_token", data=post_data) as test_response:
                    if test_response.status == 200:
                        js = await test_response.json()
                        if not self.services['reddit']:
                            printc('[ ! ]: REDDIT SERVICE AVAILABLE')
                        self.services['reddit'] = {"Authorization": f"bearer {js['access_token']}", **headers}
                    else:
                        printc(f'WARNING: REDDIT SERVICE NOT AVAILABLE: {test_response.status}')

            await asyncio.sleep(60)

    """ Events """

    async def on_ready(self):
        """ Extensions are loaded as quickly as possible """
        printc('[. . .]: LOADING EXTENSION(S):')
        extensions = {}
        for folder in os.listdir(path('cogs')):
            extensions[folder] = [cog for cog in os.listdir(path('cogs', folder)) if cog[:-3] not in ['__pycach', *self.config['blocked_cogs']]]
        self.attached_extensions = []
        for k, v in extensions.items():
            self.attached_extensions.extend([f'cogs.{k}.{i[:-3]}' for i in v])
        cog_amount = len(self.attached_extensions)
        loaded_cogs = 0
        # progress_bar(0, cog_amount)
        for i, cog in enumerate(self.attached_extensions):
            try:
                self.load_extension(cog)
            except Exception as e:
                print(e)
            # progress_bar(i + 1, cog_amount)
        create_table({'Cogs:': ['Extensions:.py'], **extensions})
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='the users'))

    async def on_disconnect(self):
        """ Sends warning when the client disconnects from the network """
        printc('[WARNING]: CLIENT HAS DISCONNECTED FROM NETWORK')

    async def on_connect(self):
        """ Sends warning when the client connects to the network """
        printc('[WARNING]: CLIENT HAS CONNECTED TO NETWORK')

    async def on_resumed(self):
        """ Sends warning when the client resumes a session """
        printc('[WARNING]: CLIENT HAS RESUMED CURRENT SESSION')


class MainCog(comms.Cog):
    """ """

    def __init__(self, bot):
        """ Objects:
        Robot(comms.Bot) as a class attribute
        """
        self.bot = bot

    """ Checks """

    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.config['owners']

    """ Commands """

    @comms.command(name='r')
    async def reload_cog(self, ctx):
        broken_cogs = []
        for cog in self.bot.attached_extensions:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except discord.ext.commands.errors.ExtensionNotFound:
                self.bot.attached_extensions.remove(cog)
            except Exception as e:
                broken_cogs.append([cog, e])
        if not len(broken_cogs):
            await ctx.send(f'**{len(self.bot.attached_extensions)}** cog(s) have been reloaded')
        else:
            info = '\n'.join(f'[{y[0]}]: {type(y[1]).__name__} - #{y[1]}' for y in broken_cogs)
            await ctx.send(f'''```css\n{info}```''')

    @comms.command(name='l')
    async def unload_cog(self, ctx, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Extension {cog.split(".")[-1]} could not be loaded')

    @comms.command(name='u')
    async def load_cog(self, ctx, cog: str):
        """ Unloads a specific cog into the bot"""
        try:
            self.bot.unload_extension(cog)
            self.bot.attached_extensions.remove(cog)
        except Exception as e:
            await ctx.send(f'Extension {cog.split(".")[-1]} could not be unloaded')

    @comms.command(name='lst_cogs')
    async def list_all_cogs(self, ctx):
        """ Lists all current cogs loaded into the bot """
        await ctx.send(f'List of **{len(self.bot.attached_extensions)}** cog(s): {", ".join(y.split(".")[-1] for y in self.bot.attached_extensions)}')

    @comms.command()
    async def exit(self, ctx):
        """ Makes the client logout """
        printc('[WARNING]: CLIENT IS LOGGING OUT')
        try:
            self.conn.close()
        except AttributeError:
            pass
        await ctx.bot.logout()

    """ Events """

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            pass
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send(f'You do not have enough permissions to run the command **.{ctx.command.name}**')
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            msg = ctx.message.content
            try:
                msg = msg[:msg.index(' ')]
            except ValueError:
                pass
            possibilities = [x.name for x in self.bot.commands]
            if len(possibilities):
                embed = discord.Embed(title='\n'.join(str(y) for y in [x.name for x in self.bot.commands] if y in msg))
                await ctx.send(content=f'**{msg}** command not found. Maybe you meant one of the following?', embed=embed)
            else:
                await ctx.send(f'Could not find a command similar to **{msg}**')
        else:
            await ctx.send(f'Notifying owner <@{self.bot.owner_id}> of error `{error}`')


if __name__ == "__main__":
    bot = Robot(command_prefix=comms.when_mentioned_or('.'), help_command=None)
    bot.add_cog(MainCog(bot))
    bot.run(bot.config['discord'], bot=True, reconnect=True)
