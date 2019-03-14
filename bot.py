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

    @comms.command(name='embeds')
    @comms.guild_only()
    async def example_embed(self, ctx):
        """ """
        embed = discord.Embed(title='Example Embed',
                              description='Showcasing the use of Embeds...\nSee the visualizer for more info.',
                              colour=0x98FB98)
        embed.set_author(name='MysterialPy',
                         url='https://gist.github.com/MysterialPy/public',
                         icon_url='http://i.imgur.com/ko5A30P.png')
        embed.set_image(url='https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png')
        embed.add_field(name='Embed Visualizer', value='[Click Here!](https://leovoel.github.io/embed-visualizer/)')
        embed.add_field(name='Command Invoker', value=ctx.author.mention)
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(content='**A simple Embed for discord.py@rewrite in cogs.**', embed=embed)

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

# Events
    @staticmethod
    async def on_member_ban(self, guild, user):
        """ """
        print(f"{user.name}-{user.id} was banned from {guild.name}-{guild.id}")


# Class BotClient inhereting from comms.Bot with event of the bot being ready
class BotClient(comms.Bot):
    @staticmethod
    async def on_ready(self):
        print(f"Logging in as {bot.user}")
        print(f"{bot.user} ID: {bot.user.id}")
        print("Awaiting...")


# Starting the bot
def main(login):
    bot = BotClient(command_prefix="$", owner_id=login[1], description='A demonic bot')
    bot.remove_command("help")
    bot.add_cog(MainCog(bot))
    bot.run(login[0], bot=True, reconnect=True)


if __name__ == '__main__':
    for extension in ["cogs.simple", "cogs.members", "cogs.owner"]:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            sys.traceback.print_exc()
    # If using code on different bot
    if len(sys.argv) == 3:
        main([sys.argv[1], sys.argv[2]])
    elif len(sys.argv) == 1:
        with open()
