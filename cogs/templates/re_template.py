'''
>> ARi0
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
import json
import asyncio
import aiohttp

from discord.ext import commands as comms
import discord

from ARi0.containers.QOL.shortened import now
from ARi0.containers.QOL.pathing import path
from ARi0.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# placeholder_type
# //////////////////////////////////////////////////////////////////////////// #
# Get information from placeholder
# //////////////////////////////////////////////////////////////////////////// #


class PLACEHOLDER_COG(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task for checking token
        """
        self.bot = bot
        self.background_service = self.bot.loop.create_task(self.load_service())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.background_service.cancel()

    """

    Background tasks

    """
    async def load_service(self):
        """

        """
        await self.bot.wait_until_ready()
        if not self.bot.is_closed():
            self.active_service = False
            if not self.active_service:
                printc('[...]: CHECKING PLACEHOLDER SERVICE AVAILABILITY')
                # self.token = json.load(open(path('ARi0', 'configuration', 'config.json')))['']
                async with aiohttp.ClientSession() as session:
                    async with session.get() as test_response:
                        if test_response.status == 200:
                            printc('[ ! ]: PLACEHOLDER SERVICE AVAILABLE')
                            self.active_service = True
                        else:
                            raise ValueError(f'WARNING: PLACEHOLDER SERVICE NOT AVAILABLE {test_response}')

    """

    Commands

    """
    @comms.group()
    async def placeholder(self, ctx):
        if ctx.invoked_subcommand is None:
            """
            Help the user
            """
            embed = discord.Embed(title='', colour=0xc27c0e, timestamp=now())
            help = '''
            `$placeholder arg1 arg2`
            `arg1`: ``
            `arg2`: ``
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)

    @placeholder.command()
    async def separate(self, ctx, *args):
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
                        await ctx.send(f'Placeholder: status code {r.status}')

    """

    Events

    """
    @comms.Cog.listener
    async def on_message(self, message):
        pass


def setup(bot):
    bot.add_cog(PLACEHOLDER_COG(bot))
