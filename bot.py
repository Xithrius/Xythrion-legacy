import discord
from discord.ext import commands as comms
import sys
import json

from sepFuncs import path


# Main cog
class MainCog:

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command()
    async def random_password(self, ctx, length=10, personal="false"):
        """ """
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

# Events
    @staticmethod
    async def on_member_ban(self, guild, user):
        """ """
        print(f"{user.name}-{user.id} was banned from {guild.name}-{guild.id}")

    @staticmethod
    async def on_message(self, message):
        """ """
        print(message.content)

    @comms.Cog.listener()
    async def on_ready(self):
        """ """
        print(f"Logging in as {self.bot.user}")
        print(f"{self.bot.user} ID: {self.bot.user.id}")
        print("Awaiting...")
        await bot.change_presence(activity=discord.Game(f"discord.py {discord.__version__}"))
        print(f"Presence changed to 'discord.py {discord.__version__}'")


# Starting the bot
def main(bot, login):
    bot.add_cog(MainCog(bot))
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
    main(bot, login)
