import json
from collections import OrderedDict, defaultdict
from pathlib import Path
from random import choice, randint
from typing import Optional

import discord
from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed

with Path('xythrion/resources/randoms.json').open('r', encoding='utf8') as f:
    RANDOMS = json.load(f)

    CARD_VALUES = [*range(2, 11), *RANDOMS['card_values']]
    CARD_SUITES = RANDOMS['card_suites']
    RPS_OPTIONS = RANDOMS['rps_options']


class Randoms(Cog):
    """Picking a bunch of different things at random (games based on random chance)."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=('roll',))
    async def dice(self, ctx: Context, rolls: int = 1) -> None:
        """Rolls a die as many times as you want."""
        if rolls > 10 or rolls < 1:
            await ctx.send('`Rolls must be between 1 and 10.`')
            return

        elif rolls > 1:
            s = sum([randint(1, 6) for _ in range(rolls)]) / rolls
            avg = f'`Die was rolled {rolls} times. Average output: {round(s, 2)}`'

        else:
            avg = f'`Die was rolled once. Output: {randint(1, 6)}`'

        await ctx.send(embed=DefaultEmbed(description=avg))

    @command()
    async def card(self, ctx: Context, amount: int = 1) -> None:
        """Picks cards from a deck."""
        if amount > 5 or amount < 0:
            await ctx.send('`Rolls must be between 1 and 5.`')

        else:
            d = defaultdict(int)
            for _ in range(amount):
                d[f'{choice(CARD_VALUES)} of {choice(CARD_SUITES)}'] += 1

            lst = '\n'.join([f'({v}) {k}' for k, v in OrderedDict(sorted(d.items())).items()])

            embed = DefaultEmbed(description=f'```py\n{lst}```')

            await ctx.send(embed=embed)

    @command(name='rps', aliases=('rps15',))
    async def rock_paper_scissors_15(self, ctx: Context, option: Optional[str] = None) -> None:
        """Plays a game of rock paper scissors against the bot."""
        option = option.lower()

        if option not in RPS_OPTIONS.keys() or not option:
            url = 'https://umop.com/rps15.htm'
            block = f'`Unknown option "{option}". Please pick from the possible options:` ' + url

            await ctx.send(block)

        else:
            lst = list(RPS_OPTIONS.keys())
            lst.remove(option)
            computer_choice = choice(lst)

            embed = discord.Embed(
                title=f'`Computer {"lost" if computer_choice in RPS_OPTIONS[option] else "won"}`',
                description=f'`Computer picked {computer_choice}, and you picked {option}.`'
            )

            await ctx.send(embed=embed)
