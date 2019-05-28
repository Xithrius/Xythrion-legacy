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


import platform
import time
import pytemperature
import json
import asyncio
import aiohttp

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now
from rehasher.containers.QOL.pathing import path
from rehasher.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Warframe request cog
# //////////////////////////////////////////////////////////////////////////// #
# Getting information from Warframe
# //////////////////////////////////////////////////////////////////////////// #


class Warframe_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task for checking service avalibility
        """
        self.bot = bot
        self.load_service = self.bot.loop.create_task(self.load_warframe())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.load_service.cancel()

    """

    Background tasks

    """
    async def load_warframe(self):
        """
        Checks if the Warframe API is accessable
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.active_warframe = False
            if not self.active_warframe:
                printc('[...]: CHECKING WARFRAME SERVICE AVAILABILITY')
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api.warframestat.us/pc/conclaveChallenges') as test_response:
                        if test_response.status == 200:
                            printc('[ ! ]: WARFRAME SERVICE AVAILABLE')
                            self.active_warframe = True
                            break
                        else:
                            raise ValueError(f'WARNING: WARFRAME SERVICE NOT AVAILABLE {test_response}')
                            await asyncio.sleep(60)

    """

    Commands

    """
    @comms.group()
    async def warframe(self, ctx):
        """
        Warframe help command
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='`Usage of the Warframe command`', colour=0xc27c0e, timestamp=now())
            help = '''
            `$warframe <thing> <another thing>`
            `<thing>`: ``
            `<another thing>`: ``
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)

    @warframe.command(name='cetusCycle')
    async def WARFRAME_cetusCycle(self, ctx, option='pc'):
        """
        Cetus status
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/cetusCycle') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The Cetus status`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='concaveChallenge')
    async def WARFRAME_concaveChallenge(self, ctx, option='pc'):
        """
        Concave challenge data
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/concaveChallenges') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The Concave challenge data`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='contructionProgress')
    async def WARFRAME_contructionProgress(self, ctx, option='pc'):
        """
        Construction Progress for Fomorians and Razorbacks
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/contructionProgress') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The construction progress for Fomorians and Razorbacks`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='dailyDeals')
    async def WARFRAME_dailyDeals(self, ctx, option='pc'):
        """
        Daily Deal information from Darvo
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/dailyDeals') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The daily deal information from Darvo`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='earthCycle')
    async def WARFRAME_earthCycle(self, ctx, option='pc'):
        """
        Current Earth rotation information
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/earthCycle') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The current Earth rotation information`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='fissures')
    async def WARFRAME_fissures(self, ctx, option='pc'):
        """
        Current fissures
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/fissures') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The current fissures`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='flashSales')
    async def WARFRAME_flashSales(self, ctx, option='pc'):
        """
        Current Flash Sales from Darvos
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/flashSales') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The current Flash Sales from Darvo`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='globalUpgrades')
    async def WARFRAME_globalUpgrades(self, ctx, option='pc'):
        """
        Current Global Upgrades
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/globalUpgrades') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The current global upgrades`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='simaris')
    async def WARFRAME_simaris(self, ctx, option='pc'):
        """
        Current Sanctuary Status
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/simaris') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The current Sanctuary Status`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='timestamp')
    async def WARFRAME_timestamp(self, ctx, option='pc'):
        """
        Get the timestamp that the current worldstate was generated at
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/timestamp') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The timestamp that the current worldstate was generated at`', colour=0xc27c0e, timestamp=now())
                            embed.add_field(name='`timestamp`', value=data)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='vallisCycle')
    async def WARFRAME_vallisCycle(self, ctx, option='pc'):
        """
        Get the current state of the Orb Vallis
        """
        if self.active_warframe:
            options = ['pc', 'ps4', 'xb1', 'swi']
            if option in options:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.warframestat.us/{option}/vallisCycle') as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = discord.Embed(title='`Warframe: The current state of the Orb Vallis`', colour=0xc27c0e, timestamp=now())
                            for k, v in data.items():
                                embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'Warframe: status code {r.status}')
            else:
                await ctx.send(f'`Please rerun command with option that is in {", ".join(str(y) for y in options)}`')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='arcanes')
    async def WARFRAME_arcanes(self, ctx, option='pc'):
        """
        Get Arcane Enhancement Data
        """
        if self.active_warframe:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.warframestat.us/arcanes') as r:
                    if r.status == 200:
                        data = await r.json()
                        embed = discord.Embed(title='`Warframe: Arcane Enhancement Data`', colour=0xc27c0e, timestamp=now())
                        for k, v in data.items():
                            embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f'Warframe: status code {r.status}')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='persistentEnemy')
    async def WARFRAME_persistentEnemy(self, ctx):
        """
        Get Persistent Enemy translation data.
        """
        if self.active_warframe:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.warframestat.us/persistentEnemy') as r:
                    if r.status == 200:
                        data = await r.json()
                        embed = discord.Embed(title='`Warframe: Persistent Enemy translation data.`', colour=0xc27c0e, timestamp=now())
                        for k, v in data.items():
                            embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f'Warframe: status code {r.status}')
        else:
            await ctx.send('`Warframe service is currently not available`')

    @warframe.command(name='routes')
    async def WARFRAME_routes(self, ctx):
        """
        Get the available routes
        """
        if self.active_warframe:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.warframestat.us/routes') as r:
                    if r.status == 200:
                        data = await r.json()
                        embed = discord.Embed(title='`Warframe: The available routes`', colour=0xc27c0e, timestamp=now())
                        for k, v in data.items():
                            embed.add_field(name=f'`{k}`:', value=f'{v}', inline=False)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f'Warframe: status code {r.status}')
        else:
            await ctx.send('`Warframe service is currently not available`')

    # TODO: Events
    # TODO: Invasions
    # TODO: News
    # TODO: Nightwave
    # TODO: Enemy data
    # TODO: Riven data (non-q)
    # TODO: Riven data (q)
    # TODO: Sortie data
    # TODO: Syndicate mission nodes
    # TODO: Void trader information
    # TODO: Worldstate data for all platforms
    # TODO: Conclave challenge data
    # TODO: Faction translation information
    # TODO: Fissure modifier translation data
    # TODO: Language strings
    # TODO: Mission type translation keys
    # TODO: operation types data
    # TODO: Everything else below /solNodes


def setup(bot):
    bot.add_cog(Warframe_Requester(bot))
