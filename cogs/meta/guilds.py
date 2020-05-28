"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""

import discord
from discord.ext import commands as comms

from utils import asteriks as ast, codeblock, markdown_link


class Guilds(comms.Cog):
    """Getting information about guilds.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.
        guild_attributes (list): All information ever wanted about a guild.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot
        self.guild_attributes = [
            'name', 'region', 'afk_timeout',
            'unavailable', 'max_presences',
            'max_members', 'description', 'mfa_level', 'verification_level',
            'explicit_content_filter', 'premium_tier', 'premium_subscription_count',
            'preferred_locale', 'large', 'system_channel', 'rules_channel'
        ]

    """ Commands """

    @comms.command()
    async def guild_info(self, ctx):
        """Get a really large amount of information about a guild.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]guild_info

        """
        g = ctx.channel.guild
        m = g.__getattribute__('members')
        members = len([y for y in m if not y.bot])
        bots = len(m) - members

        lst = [(y, g.__getattribute__(y)) for y in self.guild_attributes]

        lst.append(('bots', bots))
        lst.append(('members', members))

        lst = [f'{y[0]} : {y[1]}' for y in lst]

        embed = discord.Embed(
            title=ast('Guild information:'),
            description=codeblock(lst)
        )
        await ctx.send(embed=embed)

    @comms.command()
    async def icon(self, ctx, user: discord.User = None):
        """Shows the icon of a user.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            user (discord.User, optional): The user to get the icon url from.

        Command examples:
            >>> [prefix]icon @Xithrius

        """
        user = user if user else ctx.author

        embed = discord.Embed(
            title=ast(f'Icon for user {user}:'),
            description=markdown_link('icon url', user.avatar_url)
        )

        embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    @comms.command()
    async def server_icon(self, ctx):
        """Shows the icon of a guild (server).

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]server_icon

        """
        embed = discord.Embed(title=ast('Icon for this server:'))

        embed = discord.Embed(
            title=ast('Icon for this server:'),
            description=markdown_link('icon url', ctx.guild.icon_url)
        )

        embed.set_image(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Guilds(bot))
