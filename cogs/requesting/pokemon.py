"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from tabulate import tabulate

from modules import http_get


class Pokemon(comms.Cog):
    """Getting information about items and pokemon within pokemon.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.cooldown(100, 60, BucketType.default)
    @comms.command(aliases=['poke', 'p'], enabled=False)
    async def pokemon(self, ctx, info_type: str, option: str):
        """Getting many different things such as berries and moves.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]pokemon berry cheri

        """
        # NOTE: Do not use pokebase, as it is *very* slow.
        url = f'https://pokeapi.co/api/v2/{info_type}/{option}/'
        await http_get(url, session=self.bot.session)


def setup(bot):
    bot.add_cog(Pokemon(bot))
