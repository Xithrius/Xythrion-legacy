"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info


This is the main Python file for the discord.py bot, as all important attributes,
checks, and background tasks are created here.

Example:
    First time usage (do it every so often to keep updated packages):
        $ py -3 -m pip install --user -r requirements.txt
    To run the bot:
        $ py -3 bot.py

Todo:
    * Literally rewrite the repository

"""


import collections
import json
import asyncio
import aiohttp
import os

from discord.ext import commands as comms
import discord

from modules.output import path, ds, get_extensions


class Robot(comms.Bot):
    """Creating connections, attributes, and background tasks.
    
    Preface: When ctx is args, it gives context on where the method was called, such as channel, member, and guild.
    
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #: Opening the config json file
        with open(path('config', 'config.json'), 'r', encoding='utf8') as f:
            data = json.load(f)

        with open(path('config', 'config_connections.json'), 'r') as f:
            self.testing_urls = json.load(f)['urls']

        #: Giving self.config recursive attributes from config.json
        self.config = json.loads(json.dumps(data), object_hook=lambda d: collections.namedtuple('config', d.keys())(*d.values()))

        self.services = data['services']

        self.owner_ids = set(self.config.owners)

        #: All requesters must have one testing link to make sure a connection is possible to the API.
        self.requester_status = {x[:-3]: False for x in os.listdir(path('cogs', 'requesters')) if x[-3:] == '.py'}

        #: Create async loop
        self.loop = asyncio.get_event_loop()

        future = asyncio.gather()
        
        #: Create tasks
        self.loop.create_task(self.create_tasks())
        self.loop.run_until_complete(future)

    """ subclass-specific functions """

    async def load_extensions(self):
        ds.w('Loading extensions...')
        broken_extensions = []
        for extension in get_extensions(self.config.blocked_extensions):
            try:
                self.load_extension(extension)
            except Exception as e:
                broken_extensions.append(f'{type(e).__name__}: {e}')
        for ext in broken_extensions:
            ds.w(ext)
        ds.r('Extensions finished loaded.')

    async def create_tasks(self):
        self.s = aiohttp.ClientSession()
        ds.r('Connections established.')

        self.connection_loop = asyncio.get_running_loop()
        await self.connection_loop.create_task(self.test_services())

        # self.request_limiter = asyncio.new_event_loop()

    async def test_services(self):
        """ """
        while not self.is_closed():
            self.broken_services = []
            for k, v in self.testing_urls.items():
                if k in self.config.blocked_extensions:
                    continue
                url = v['test_url']
                if 'TOKEN' in url:
                    url = url.replace('TOKEN', self.services[k])
                if 'headers' in v.keys():
                    headers = {k1: v1.replace('TOKEN', self.services[k]) for k1, v1 in v['headers'].items()}
                else:
                    headers = None
                async with self.s.get(url, headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        self.requester_status[k] = True
                    else:
                        self.broken_services.append(f'[ {k.upper()} ]: {r.status} - {r}')
            if self.broken_services:
                for broken_service in self.broken_services:
                    ds.f(broken_service)
            await asyncio.sleep(60)

    """ Events """

    async def on_ready(self):
        await self.load_extensions()
        await self.change_presence(status=discord.ActivityType.playing, activity=discord.Game('with user data'))
        ds.r('Startup completed.')

    async def close(self):
        """ Safely closes connections """
        try:
            await self.s.close()
            self.c.close()
        except Exception as e:
            pass
        await super().close()


class RobotCog(comms.Cog):
    """Essential commands for using the bot."""

    def __init__(self, bot):
        #: Robot(comms.Bot) as a class attribute
        self.bot = bot

    @comms.command(alias=['reload', 'refresh', 'r'])
    async def reload(self, ctx):
        extension_status = await self.load_extensions()
        if extension_status:
            for extension in extension_status:
                ds.w(extension)
        else:
            ds.s('Reloaded all cogs.')

    @comms.command(alias=['disconnect', 'dc', 'exit'])
    async def exit(self, ctx):
        """Logs out the bot.

        Returns:
            A possible timeout error.

        """
        ds.w('Logging out...')
        await ctx.bot.logout()


class InfoCog(comms.Cog):
    """Cog is meant to give information about owner and bot interactions."""

    def __init__(self, bot):
        #: Robot(comms.Bot) as a class attribute
        self.bot = bot

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot. It is not 'essential', but it's still useful.
        
        Returns:
            The invite link so the bot can be invited to a server.
        
        """
        await ctx.send(f'https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=32885952')

    @comms.command()
    async def about(self, ctx):
        """Returns information about this bot's origin
        
        Returns:
            An embed object with links to creator's information and bot's repository.
        
        """
        info = {
            'Twitter': 'https://twitter.com/_Xithrius',
            'Github': 'https://github.com/Xithrius/Xythrion'
        }
        embed = discord.Embed(title='Project creation date: March 30, 2019', description='\n'.join(f'[`{k}`]({v})' for k, v in info.items()), colour=self.bot.ec)
        await ctx.send(embed=embed)

    @comms.command()
    async def website(self, ctx):
        """Returns website for the bot (this replaced the README).
        
        Returns:
            An embed object containing the website link for the bot.
        
        """
        embed = discord.Embed(description='`https://xithrius.github.io/Xythrion/`')
        await ctx.send(embed=embed)


if __name__ == "__main__":
    bot = Robot(command_prefix=comms.when_mentioned_or('.'))
    bot.add_cog(RobotCog(bot))
    bot.add_cog(InfoCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
