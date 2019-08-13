"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import json
import aiohttp
import random
import os

from discord.ext import commands as comms
import discord

from handlers.modules.output import printc, path, now


class Osu_Requester(comms.Cog):
    """ Get information from WeatherBit """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot
        self.h = self.bot.services[os.path.basename(__file__)[:-3]]

    """ Permission checking """

    async def cog_check(self, ctx):
        """ """
        return all((ctx.message.author.id in self.bot.owner_ids, self.h))

    """ Commands """

    @comms.group()
    async def osu(self, ctx):
        """ """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Type the command **.help {ctx.command}** for help')

    @osu.command(name='user')
    async def _user(self, ctx, u, m=0, t='string', ed=1):
        """ Arguments:
        u  : username   (name or id of user depending on t)
        m  : mode       (0 = Osu! Standard, 1 = Taiko, 2 = CtB, 3 = Osu! Mania)
        t  : type       (string for usernames, id for user_ids)
        ed : event days (range from 1-31 of eventful days)
        """
        params = {'k': self.bot.config.services.osu, 'u': u, 'm': m, 'type': t, 'event_days': ed}
        async with self.bot.s.get(f'https://osu.ppy.sh/api/get_user', params=params) as r:
            if r.status == 200:
                _json = await r.json()
                info = '\n'.join(f'**{k}**: {v}' for k, v in _json[0].items())
                embed = discord.Embed(title=f'Osu! User info:')
                embed.add_field(name='', value='')
                await ctx.send(embed=embed)
            elif r.status == 404:
                await ctx.send(f'User **{u}** could not be found.')
            else:
                await ctx.send(f'Requester failed. Status code: **{r.status}**')


def setup(bot):
    bot.add_cog(Osu_Requester(bot))
