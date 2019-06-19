'''
>> SoftBot
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import platform
import time
import pytemperature
import json
import asyncio
import aiohttp

from discord.ext import commands as comms
import discord

from SoftBot.containers.QOL.shortened import now
from SoftBot.containers.QOL.pathing import path
from SoftBot.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# <> request cog
# //////////////////////////////////////////////////////////////////////////// #
# Get information from <>
# //////////////////////////////////////////////////////////////////////////// #


class Twitter_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task for checking token
        """
        self.bot = bot
        self.background_service = self.bot.loop.create_task(self.load_twitter())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.background_service.cancel()

    """

    Background tasks

    """
    async def load_twitter(self):
        """

        """
        await self.bot.wait_until_ready()
        if not self.bot.is_closed():
            self.active_service = False
            if not self.active_service:
                printc('[...]: CHECKING TWITTER SERVICE AVAILABILITY')
                # self.token = json.load(open(path('SoftBot', 'configuration', 'config.json')))['']
                async with aiohttp.ClientSession() as session:
                    async with session.get() as test_response:
                        if test_response.status == 200:
                            printc('[ ! ]: TWITTER SERVICE AVAILABLE')
                            self.active_service = True
                        else:
                            raise ValueError(f'WARNING: TWITTER SERVICE NOT AVAILABLE {test_response}')

    """

    Commands

    """
    @comms.group()
    async def main_command(self, ctx):
        if ctx.invoked_subcommand is None:
            """
            Help the user
            """
            embed = discord.Embed(title='', colour=0xc27c0e, timestamp=now())
            help = '''
            `$ <> <>`
            `<>`: ``
            `<>`: ``
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)

    @main_command.command(name='')
    async def MAIN_COMMAND_seperate(self, ctx, *args):
        """

        """
        if self.active_service:
            async with aiohttp.ClientSession() as session:
                async with session.get('') as r:
                    if r.status == 200:
                        data = await r.json()
                        embed = discord.Embed(title='', colour=0xc27c0e, timestamp=now())
                        embed.add_field(name='', value=data, inline=False)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await ctx.author.send(embed=embed, delete_after=30)
                    else:
                        await ctx.send(f'Weather: status code {r.status}')

    """

    Events

    """
    @comms.Cog.listener
    async def on_message(self, message):
        pass


def setup(bot):
    bot.add_cog(Twitter_Requester(bot))
