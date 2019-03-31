'''

MIT License

Copyright (c) 2019 Xithrius

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


# ///////////////////////////////////////////////////////// #
# authorship information
# ////////////////////////
# Description of the author(s) information
# ///////////////////////////////////////////////////////// #


__author__ = 'Xithrius'

__copyright__ = 'MIT License, Copyright (c) 2019 Xithrius'

__credits__ = ["Xithrius", "Rapptz"]
# Xithrius : Project owner
# Rapptz   : Discord.py API wrapper creator

__license__ = "MIT"

__version__ = "0.00.0009"

__maintainer__ = "Xithrius"

__status__ = "Development"


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import discord
from discord.ext import commands as comms

# from essentials.pathing import path, mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


class ExampleCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command(name='embeds')
    @comms.guild_only()
    async def example_embed(self, ctx):
        """A simple command which showcases the use of embeds.

        Have a play around and visit the Visualizer."""

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

    @comms.command()
    @comms.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f'{member.display_name} joined on {member.joined_at}')

    @comms.command(name='coolbot')
    async def cool_bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('This bot is cool. :)')

    @comms.command(name='top_role', aliases=['toprole'])
    @comms.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member = None):
        """Simple command which shows the members Top Role."""
        if member is None:
            member = ctx.author
        await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')

    @comms.command(name='perms', aliases=['perms_for', 'permissions'])
    @comms.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member = None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""
        if not member:
            member = ctx.author
        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)
        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)
        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.

    @comms.command(name='repeat', aliases=['copy', 'mimic'])
    async def do_repeat(self, ctx, *, our_input: str):
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our comms as the first argument after self."""
        await ctx.send(our_input)

    @comms.command(name='add', aliases=['plus'])
    @comms.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        """A simple command which does addition on two integer values."""
        total = first + second
        await ctx.send(f'The sum of **{first}** and **{second}**  is  **{total}**')

    @comms.command(name='me')
    @comms.is_owner()
    async def only_me(self, ctx):
        """A simple command which only responds to the owner of the bot."""
        await ctx.send(f'Hello {ctx.author.mention}. This command can only be used by you!!')

    # Events
    async def on_member_ban(self, guild, user):
        """Event Listener which is called when a user is banned from the guild.
        For this example I will keep things simple and just print some info.
        Notice how because we are in a cog class we do not need to use @bot.event
        For more information:
        http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_member_ban
        Check above for a list of events.
        """
        print(f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')

    @comms.command()
    async def news(self, ctx):
        embed = discord.Embed(title='News Role', description='To get News role press on ✅ reaction', color=0x00ffff)
        thing = await ctx.send(embed=embed)
        await thing.add_reaction(emoji="✅")

    async def on_raw_reaction_add(self, ctx, reaction, user):
        embed = discord.Embed(title='News Role', description='The bot added role News', color=0x00ffff)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ExampleCog(bot))
