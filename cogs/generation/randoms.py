"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from collections import OrderedDict, defaultdict
from random import choice, randint

import discord
from discord.ext import commands as comms

from modules import ast, gen_block


class Randoms(comms.Cog):
    """Picking a bunch of different things at random (games based on random chance).

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
        self.rps_options = {
            'rock': ['fire', 'scissors', 'snake', 'human', 'wolf', 'sponge', 'tree'],
            'paper': ['air', 'rock', 'water', 'devil', 'dragon', 'lightning'],
            'fire': ['scissors', 'paper', 'snake', 'human', 'tree', 'wolf', 'sponge'],
            'scissors': ['air', 'tree', 'paper', 'snake', 'human', 'wolf', 'sponge'],
            'gun': ['rock', 'tree', 'fire', 'scissors', 'snake', 'human', 'wolf'],
            'water': ['devil', 'dragon', 'rock', 'fire', 'scissors', 'gun', 'lightning'],
            'air': ['fire', 'rock', 'water', 'devil', 'gun', 'dragon', 'lightning'],
            'sponge': ['paper', 'air', 'water', 'devil', 'dragon', 'gun', 'lightning'],
            'human': ['tree', 'wolf', 'sponge', 'paper', 'air', 'water', 'dragon'],
            'devil': ['rock', 'fire', 'scissors', 'gun', 'lightning', 'snake', 'human'],
            'dragon': ['devil', 'lightning', 'fire', 'rock', 'scissors', 'gun', 'snake'],
            'lightning': ['gun', 'scissors', 'rock', 'tree', 'fire', 'snake', 'human'],
            'snake': ['human', 'wolf', 'sponge', 'tree', 'paper', 'air', 'water'],
            'wolf': ['sponge', 'paper', 'air', 'water', 'lightning', 'dragon', 'devil'],
            'tree': ['wolf', 'dragon', 'sponge', 'paper', 'air', 'water', 'devil']
        }

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

    @comms.command(aliases=['rockpaperscissors'])
    async def RPS(self, ctx, option: str):
        """Plays a game of rock paper sissors against the bot.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            option (str): The option that the user chooses.

        Command examples:
            >>> [prefix]RPS
            >>> [prefix]rps wolf

        """
        option = option.lower()
        if option not in self.options.keys():
            m = max(map(len, list(self.options.keys())))
            block = gen_block(
                content=[str(k).rjust(m) + ' : ' + ', '.join(
                    str(y) for y in v) for k, v in {'[ choice ]': ['[ beats ]'], **self.options}.items()],
                lines=True
            )
            block = f'`Unknown option "{option}". Please pick from the possible options:`\n' + block
            await ctx.send(block)
        else:
            lst = list(self.options.keys())
            lst.remove(option)
            computer_choice = choice(lst)

            embed = discord.Embed(
                title=ast(f'Computer {"lost" if computer_choice in self.options[option] else "won"}'),
                description=f'`Computer picked {computer_choice}, and you picked {option}.`'
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Randoms(bot))
