"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from random import choice

import discord
from discord.ext import commands as comms

from modules import ast, gen_block


class RockPaperScissors(comms.Cog):
    """Playing Rock Paper Scissors 15 ways with the computer.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.
        options (dict): All the options and a list of what they lose to.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot
        self.options = {
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
    bot.add_cog(RockPaperScissors(bot))
