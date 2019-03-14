import discord
from discord.ext import commands as comms
import sys
import json

# Main cog
class MainCog:

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command(name='repeat', aliases=['copy', 'mimic'])
    async def do_repeat(self, ctx, *, our_input: str):
        """ """
        await ctx.send(our_input)

    @comms.command(name='add', aliases=['plus'])
    @comms.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        """ """
        total = first + second
        await ctx.send(f"{first}+{second}={total}")

    @comms.command(name='me')
    @comms.is_owner()
    async def only_me(self, ctx):
        """ """
        await ctx.send(f'Hello {ctx.author.mention}. This command can only be used by you!!')

    @comms.command(name='randomPass')
    @comms.guild_only()
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


login = [196664644113268736, "NTI0NzgyNTI3MzI4NTUwOTY2.Dx_xWA.DDuKgkK_8vo_G2qX6jpu0n1BhXY"]
bot = comms.Bot(command_prefix="$", owner_id=login[0], description='A demonic bot')
bot.remove_command("help")
bot.add_cog(MainCog(bot))
bot.run(login[1], bot=True, reconnect=True)
