import discord
from discord.ext import commands as comms
import sys
import json
import traceback
import os

from separateFunctions import path


# Main cog
class MainCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command(name='reload', hidden=True)
    @comms.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send('Reload Complete')

    @comms.command()
    @comms.is_owner()
    async def exit(self, ctx):
        print("Exiting...")
        await self.bot.logout()
        
# Events
    async def on_ready(self):
        """ """
        print(f"Logging in as {self.bot.user}")
        print(f"{self.bot.user} ID: {self.bot.user.id}")
        print("Awaiting...")
        await bot.change_presence(activity=discord.Game(f"discord.py {discord.__version__}"))
        print(f"Presence changed to 'discord.py {discord.__version__}'")


# Starting the bot
def main(bot, login):
    bot.run(login, bot=True, reconnect=True)


if __name__ == '__main__':
    # If using code on different bot(s)
    if len(sys.argv) == 3:
        login = sys.argv[1]
    # If using code on own bot(s)
    elif len(sys.argv) == 1:
        with open(path("credentials", "DStoken.txt"), "r") as f:
            login = f.read().strip()
    bot = comms.Bot(command_prefix="$", description='A demonic bot')
    # Adding the main cog to the bot
    bot.add_cog(MainCog(bot))
    # Searching for cogs within the cogs directory
    fileCogs = []
    for (dirpath, dirnames, filenames) in os.walk(path("cogs")):
        fileCogs.extend(filenames)
        break
    # Making the names of cogs start with cogs.
    cogs = []
    for file in fileCogs:
        if file[-3:] == ".py":
             cogs.append(f"cogs.{file[:len(file) - 3]}")
    # Loading all cogs in as extensions of the main cog
    for i in cogs:
        try:
            bot.load_extension(i)
        except Exception as e:
            print(f'Failed to load extension {i}.', file=sys.stderr)
            traceback.print_exc()
    # Calling main to run the bot
    main(bot, login)
