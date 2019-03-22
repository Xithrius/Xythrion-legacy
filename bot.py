from discord.ext import commands as comms
import discord
import sys
import traceback
import os
import aiohttp
import logging

from essentials.pathing import path
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt

# Logging stuff
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=path('logs', 'discord.log'), encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Main cog
class MainCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command()
    async def poke(self, ctx, member: discord.User = None):
        if member is None:
            await ctx.author.send('Hi')
        else:
            possibleMembers = []
            _members = ctx.message.guild.members
            for i in range(len(_members)):
                if _members[i].startswith(member):
                    possibleMembers.append(_members[i])
            await ctx.send(ctx.message.discord.User)
            if len(possibleMembers) > 1:
                await ctx.send(f"Searched member {member} has multiple possibilities: {', '.join(str(x) for x in possibleMembers)}")
            if len(possibleMembers) == 1:
                member = discord.User(possibleMembers)
                await ctx.member.send("Testing stuff")

# Commands for realoading, unloading, and loading cogs
    @comms.command(name='reload', hidden=True)
    @comms.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """ Reload specific cog(s) """
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Reload complete for {cog}')

    @comms.command(name='load', hidden=True)
    @comms.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """ Load in a specific cog(s) """
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Load complete for {cog}')

    @comms.command(name='unload', hidden=True)
    @comms.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """ Unload a specific cog(s) """
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Unload complete for {cog}')
# Logging out the bot
    @comms.command()
    @comms.is_owner()
    async def exit(self, ctx):
        """ Make the bot logout """
        print('Exiting...')
        await self.bot.logout()

# Events
    @comms.Cog.listener()
    async def on_ready(self):
        print(f'Logging in as {self.bot.user}')
        print(f'{self.bot.user} ID: {self.bot.user.id}')
        print('Awaiting...')
        await bot.change_presence(activity=discord.Game(f'discord.py rewrite {discord.__version__}'))
        print(f"Presence changed to 'discord.py {discord.__version__}'")


# Starting the bot
def main(bot):
    # Adding the main cog to the bot
    bot.add_cog(MainCog(bot))
    bot.remove_command('help')

    # Searching for cogs within the cogs directory
    fileCogs = []
    for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
        fileCogs.extend(filenames)
        break

    # Making the names of cogs start with cogs.
    cogs = []
    for file in fileCogs:
        if file[-3:] == '.py':
            cogs.append(f'cogs.{file[:len(file) - 3]}')

    # Loading all cogs in as extensions of the main cog
    for i in cogs:
        try:
            bot.load_extension(i)
        except Exception as e:
            print(e)
            print(f'Failed to load extension {i}.', file=sys.stderr)
            traceback.print_exc()

    # Looping the input until token is correct
    checkToken = True
    while checkToken:
        try:
            with open(path('credentials', 'discord_token.txt'), 'r') as f:
                login = f.read().strip()
                # Running the bot
                bot.run(login, bot=True, reconnect=True)
                checkToken = False
        except FileNotFoundError or discord.errors.LoginFailure:
            with open(path('credentials', 'discord_token.txt'), 'w') as f:
                login = input('Input Discord bot token: ')
                f.write(login)


if __name__ == '__main__':
    bot = comms.Bot(connector=aiohttp.TCPConnector(ssl=False), command_prefix='$')

    # Calling main to run the bot
    main(bot)
