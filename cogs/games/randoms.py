"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from collections import OrderedDict, defaultdict
from random import choice, randint

import discord
from discord.ext import commands as comms

from modules import gen_block, ast


class Randoms(comms.Cog):
    """Picking a bunch of different things at random.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.
        card_values (list): All possible values for a card
        card_suites (list): All possible suites for a card

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
            rolls (int, optional): The amount of times the die will be rolled.

        Command examples:
            >>> [prefix]dice
            >>> [prefix]dice 100

        """
        if rolls > 10 or rolls < 0:
            return await ctx.send('`Rolls must be between 1 and 10.`')

        if rolls > 1:
            s = sum([randint(1, 6) for x in range(rolls)]) / rolls
            avg = f'`Die was rolled {rolls} times. Average output: {round(s, 2)}`'
        else:
            avg = f'`Die was rolled once. Output: {randint(1, 6)}`'

        embed = discord.Embed(description=avg)

        await ctx.send(embed=embed)

    @comms.command()
    async def card(self, ctx, amount: int = 1):
        """Picks cards from a deck.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            amount (int, optional): The amount of cards that will be picked.

        Command examples:
            >>> [prefix]card
            >>> [prefix]card 10

        """
        if amount > 10 or amount < 0:
            return await ctx.send('`Rolls must be between 1 and 10.`')

        d = defaultdict(int)
        for _ in range(amount):
            d[f'{choice(self.card_values)} of {choice(self.card_suites)}'] += 1

        lst = OrderedDict(sorted(d.items()))
        lst = [f'({v}) {k}' for k, v in d.items()]

        embed = discord.Embed(
            title=ast(f'Results from {amount} randomly chosen cards:'),
            description=gen_block(lst)
        )

        await ctx.send(embed=embed)

    @comms.command(aliases=['flip'])
    async def coin(self, ctx):
        """Flips a coin and tells you which side it landed on.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]coin
            >>> [prefix]flip

        """
        embed = discord.Embed(
            title=ast('Tossed a coin to your Witcher.'),
            description=f'`Landed {choice(["heads", "tails"])} facing up.`'
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Randoms(bot))
