"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord


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

        lst = '\n'.join(f'{y[0]} : {y[1]}' for y in lst)
        embed = discord.Embed(title='*Guild information:*', description=f'```py\n{lst}\n```')
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


def setup(bot):
    bot.add_cog(Guilds(bot))
