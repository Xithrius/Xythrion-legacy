"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio

import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

from modules import gen_block


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

        """
        g = ctx.channel.guild
        # print(dir(g)) to get all attribute names of a guild.
        m = g.__getattribute__('members')
        members = len([y for y in m if not y.bot])
        bots = len(m) - members

        lst = [(y, g.__getattribute__(y)) for y in self.guild_attributes]

        lst.append(('bots', bots))
        lst.append(('members', members))

        lst = [f'{y[0]} : {y[1]}' for y in lst]
        embed = discord.Embed(title='*Guild information:*', description=gen_block(lst))
        await ctx.send(embed=embed)

    @comms.command(enabled=False)
    @comms.is_owner()
    async def generate_guild(self, ctx, *, name: str):
        """Creates a guild and returns the invite to the owner.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            name (str): The name of the guild.

        """
        # NOTE: Bot accounts in more than 10 guilds are not allowed to create guilds.
        pass

    @comms.cooldown(1, 60, BucketType.default)
    @comms.command()
    @comms.is_owner()
    async def message_owners(self, ctx, *, message: str):
        """Messages owners of all guilds that the bot is in a specific message.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            message (str): The name of the guild.

        """
        owners = [guild.owner for guild in self.bot.guilds]
        embed = discord.Embed(description=f'`Messaging {len(owners)} owners...`')
        msg = await ctx.send(embed=embed)

        owner_embed = discord.Embed(title=f'**Message from bot creator `(Xithrius#1318)`:**')
        owner_embed.description = message

        for guild in self.bot.guilds:
            await guild.owner.send(embed=owner_embed)
            await asyncio.sleep(1)

        embed.set_footer(text='Done.')
        await msg.edit(embed=embed)

    @comms.command()
    async def icon(self, ctx, user: discord.User = None):
        user = user if user else ctx.author
        await ctx.send(user.avatar_url)


def setup(bot):
    bot.add_cog(Guilds(bot))
