"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from collections import OrderedDict, defaultdict
from random import choice, randint

import discord
from discord.ext import commands as comms

from modules import gen_block


class Randoms(comms.Cog):
    """Picking dice numbers and cards out of lists at random.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot
        self.card_values = [*range(2, 11), 'Jack', 'Queen', 'King', 'Ace']
        self.card_suites = ['Hearts', 'Clubs', 'Diamonds', 'Spades']

    """ Commands """

    @comms.command()
    async def dice(self, ctx, rolls: int = 1):
        """Rolls a die as many times as you want.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            rolls (int): The amount of times the die will be rolled.

        """
        if 1000 < rolls < 0:
            return await ctx.send('`Rolls must be between 1 and 1000.`')

        s = sum([randint(1, 6) for x in range(rolls)]) / rolls

        if rolls > 1:
            avg = f'`Die was rolled {rolls} times. Average output: {round(s, 2)}`'
        else:
            avg = f'`Die was rolled once. Output: {s}`'

        embed = discord.Embed(description=avg)

        await ctx.send(embed=embed)

    @comms.command()
    async def card(self, ctx, amount: int = 1):
        """Picks cards from a deck.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            amount (int): The amount of cards that will be picked.

        """
        if 250 < amount < 0:
            return await ctx.send('`Rolls must be between 1 and 250.`')

        d = defaultdict(int)
        for _ in range(amount):
            d[f'{choice(self.card_values)} of {choice(self.card_suites)}'] += 1

        lst = OrderedDict(sorted(d.items()))
        lst = [f'({v}) {k}' for k, v in d.items()]

        await ctx.send(gen_block(lst))


def setup(bot):
    bot.add_cog(Randoms(bot))
