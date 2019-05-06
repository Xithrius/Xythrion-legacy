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


import requests
import json
import asyncio

from discord.ext import commands as comms

from containers.output.printer import printc
from containers.QOL.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# riot.com request cog
# //////////////////////////////////////////////////////////////////////////// #
# Getting information from riot
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
        pass
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
            if response == {'status': {'message': 'Forbidden', 'status_code': 403}}:
                printc(f'WARNING: RIOT ACCOUNT CANNOT BE ACTIVATED\n{response["status"]["message"]}: {response["status"]["status_code"]}')
                await asyncio.sleep(60)
            else:
                self.riot_script_active = True
                printc('[ ! ]: RIOT SCRIPT CREDENTIALS ACTIVATED')

    """

    Commands

    """
    @comms.command()
    @comms.is_owner()
    async def user(self, ctx, user):
        """
        Gets information about a summoner
        """
        userRequest = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user}', headers=self.headers).json()
        userInfo = requests.get(f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{userRequest["id"]}', headers=self.headers).json()
        print(userInfo)


def setup(bot):
    bot.add_cog(Riot_Requester(bot))
