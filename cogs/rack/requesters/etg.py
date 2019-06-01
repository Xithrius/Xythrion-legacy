'''
>> Rehasher.py
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


from bs4 import BeautifulSoup
import platform
import time
import json
import asyncio
import aiohttp

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now
from rehasher.containers.QOL.pathing import path
from rehasher.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# enterthegungeon.gamepedia.com requesting cog
# //////////////////////////////////////////////////////////////////////////// #
# Get information from the enter the gungeon wiki
# //////////////////////////////////////////////////////////////////////////// #


class ETG_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task for checking token
        """
        self.bot = bot
        self.load_service = self.bot.loop.create_task(self.load_ETG())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.load_service.cancel()

    """

    Background tasks

    """
    async def load_ETG(self):
        """
        Checks if ETG service is accessable
        """
        await self.bot.wait_until_ready()
        if not self.bot.is_closed():
            self.active_ETG = False
            if not self.active_ETG:
                printc('[...]: CHECKING ETG SERVICE AVAILABILITY')
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://enterthegungeon.gamepedia.com/Guns') as test_response:
                        if test_response.status == 200:
                            printc('[ ! ]: ETG SERVICE AVAILABLE')
                            self.active_ETG = True
                        else:
                            raise ValueError(f'WARNING: ETG SERVICE NOT AVAILABLE {test_response}')

    """

    Commands

    """
    @comms.group()
    async def etg(self, ctx):
        """
        Helps the user with ETG commands
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='`Usage of the Enter the Gungeon (ETG) commands`', colour=0xc27c0e, timestamp=now())
            help = '''
            `$etg <> <>`
            `<>`: ``
            `<>`: ``
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)

    @etg.command(name='guns')
    async def ETG_guns(self, ctx, gun):
        if self.active_ETG:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://enterthegungeon.gamepedia.com/Guns') as r:
                    if r.status == 200:
                        data = await r.read()
                        soup = BeautifulSoup(data, "lxml")
                        table = soup.find('table')
                        for tag in table.find_all('tr'):
                            next(tag)
                            break
                    else:
                        await ctx.send(f'ETG: status code {r.status}')


def setup(bot):
    bot.add_cog(ETG_Requester(bot))

'''
soup = BeautifulSoup(page.content, "lxml")
table = soup.find('table')
mainTable = {}
for i in [tag.contents[0]['href'] for tag in table.find_all('h4')]:
    link = main_website[:main_website.index('/ooh')] + i
    # If page isn't reached in time, exception will be raised
    page = requests.get(link, timeout=5)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, "lxml")
    table = soup.find('table')
'''