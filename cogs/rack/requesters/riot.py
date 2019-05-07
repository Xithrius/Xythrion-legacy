'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import asyncio
import json
import requests

from discord.ext import commands as comms
import discord

from relay.containers.output.printer import printc
from relay.containers.QOL.pathing import path
from relay.containers.QOL.shortened import now


# //////////////////////////////////////////////////////////////////////////// #
# Riot request cog
# //////////////////////////////////////////////////////////////////////////// #
# Getting information from Riot
# //////////////////////////////////////////////////////////////////////////// #


class Riot_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task
        """
        self.bot = bot
        self.load_script = self.bot.loop.create_task(self.load_riot_script())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.load_script.cancel()

    """

    Background tasks

    """
    async def load_riot_script(self):
        """
        Checks if League of Legends is accessable
        """
        await self.bot.wait_until_ready()
        if not self.bot.is_closed():
            self.riot_script_active = False
            printc('[...]: CHECKING RIOT SCRIPT CREDENTIALS')
            self.headers = {
                "Origin": "https://developer.riotgames.com",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Riot-Token": json.load(open(path('relay', 'configuration', 'config.json')))['riot'],
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
            }
            response = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/dinoderp31', headers=self.headers).json()
            if next(iter(response)) == 'status':
                printc(f'WARNING: RIOT ACCOUNT CANNOT BE ACTIVATED\n{response["status"]["message"]}: {response["status"]["status_code"]}')
                await asyncio.sleep(60)
            else:
                self.riot_script_active = True
                printc('[ ! ]: RIOT SCRIPT CREDENTIALS ACTIVATED')

    """

    Commands

    """
    @comms.group()
    async def lol(self, ctx):
        """
        League of Legends group command
        """
        if ctx.invoked_subcommand is None:
            pass

    @lol.command(name='user')
    async def lol_summoner(self, ctx):
        """
        Gets information about a summoner
        """
        user = ctx.message.content[9:]
        print(user)
        userRequest = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user}', headers=self.headers).json()
        print(userRequest)
        userInfo = requests.get(f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{userRequest["id"]}', headers=self.headers).json()
        if len(userInfo) == 0:
            await ctx.send('No ranked data found on this user')
        else:
            embed = discord.Embed(title=f'Current summoner info on {user}', colour=0xc27c0e, timestamp=now())
            embed.set_thumbnail(url='https://imgur.com/oJsGQbQ')
            embed.add_field(name='test', value='test')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Riot_Requester(bot))
