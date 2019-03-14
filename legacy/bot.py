# Python virtual environment libraries
from discord.ext import commands as comms  # <<< pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]
import discord
import random
import string
import datetime
import asyncio
# import sys
# import platform

# Local python functions
# import _error_prompt
import _file_check
# import _input_loop
# import _new_dir
import _path
# import _welcome_prompt


class MainCog:
    def __init__(self, bot):
        self.bot = bot
# Events
    @staticmethod
    async def on_ready():
        await bot.change_presence(activity=discord.Game("with Google Sheets"))
        print("Presence changed to 'Playing With Google Sheets'")
# Commands
# Random password generator
    @comms.command()
    async def random_password(self, ctx, length=10, personal="false"):
        if length > 0:
            password = ''.join(str(y) for y in [random.choice(string.ascii_letters + string.digits) for i in range(length)])
            embed = (discord.Embed(title="[ Random Password Generator ]", timestamp=datetime.datetime.now() + datetime.timedelta(hours=8)))
            embed.add_field(name=f"Password of length {length}:", value=password, inline=False)
            if personal == "true":
                await ctx.author.send(embed=embed, delete_after=30)
            else:
                await ctx.send(embed=embed, delete_after=180)
        else:
            if personal == "true":
                await ctx.author.send(f"{length} is an invalid parameter.")
            else:
                await ctx.send(f"{length} is an invalid parameter")
# Exiting
    @comms.command()
    async def exit(self, ctx):
        if await ctx.bot.is_owner(ctx.author):
            print("Exiting...")
            await self.bot.logout()
        else:
            await ctx.send(f"{ctx.author.mention} you cannot do this")


# Starting bot
class BotClient(comms.Bot):
    @staticmethod
    async def on_ready(self):
        print(f"Logging in as {bot.user}")
        print(f"{bot.user} ID: {bot.user.id}")
        print("Awaiting...")


login = _file_check.main()
bot = BotClient(command_prefix="$", owner_id=login[0])
bot.remove_command("help")
bot.add_cog(MainCog(bot))
bot.run(login[1])
