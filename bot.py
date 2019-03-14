import discord
from discord.ext import commands as comms


class MainCog:

    def __init__(self, bot):
        self.bot = bot

    @comms.command(name='repeat', aliases=['copy', 'mimic'])
    async def do_repeat(self, ctx, *, our_input: str):
        await ctx.send(our_input)

    @comms.command(name='add', aliases=['plus'])
    @comms.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        total = first + second
        await ctx.send(f"{first}+{second}={total}")

    @comms.command(name='me')
    @comms.is_owner()
    async def only_me(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}. This command can only be used by you!!')

    @comms.command(name='embeds')
    @comms.guild_only()
    async def example_embed(self, ctx):
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

    async def on_member_ban(self, guild, user):
        print(f"{user.name}-{user.id} was banned from {guild.name}-{guild.id}")


def setup(bot):
    bot.add_cog(MainCog(bot))
