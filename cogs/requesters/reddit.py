"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import json
import aiohttp

from discord.ext import commands as comms

from handlers.modules.output import printc, path
import core


class Reddit_Requester(comms.Cog):
    """ Getting information from Reddit """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task
        """
        self.bot = bot
        self.load_credentials = self.bot.loop.create_task(self.load_reddit())

    def cog_unload(self):
        """ Cancel background task(s) when cog is unloaded """
        self.load_credentials.cancel()

    """ Background tasks """

    async def load_reddit(self):
        """ Checks if reddit is accessable """
        await self.bot.wait_until_ready()
        printc('[...]: CHECKING REDDIT SERVICE AVAILABILITY')
        while not self.bot.is_closed():
            self.active_reddit = False
            f = json.load(open(path('handlers', 'configuration', 'config.json')))['reddit']
            self.client_auth = aiohttp.BasicAuth(login=f['client_ID'], password=f['client_secret'])
            post_data = {"grant_type": "password", "username": f['username'], "password": f['password']}
            headers = {"User-Agent": f"Xiux/{core.__version__} by {f['username']}"}
            async with aiohttp.ClientSession(auth=self.client_auth, headers=headers) as session:
                async with session.post("https://www.reddit.com/api/v1/access_token", data=post_data) as test_response:
                    if test_response.status == 200:
                        js = await test_response.json()
                        if js != {'error': 'invalid_grant'}:
                            self.active_reddit = True
                            printc('[ ! ]: REDDIT SERVICE AVAILABLE')
                            self.headers = {"Authorization": f"bearer {js['access_token']}", **headers}
                            await asyncio.sleep(js['expires_in'])
                        else:
                            printc(f'WARNING: BROKEN REDDIT REQUESTER. ERROR CODE: {js}')
                            break
                    else:
                        printc(f'WARNING: REDDIT REQUESTS CANNOT BE ACTIVATED. ERROR CODE: {test_response.status}')
                        break

    """ Asynchronus functions """

    async def aiohttp_requester(self, ctx, url, data=None):
        """ Gets data from Reddit """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    await ctx.send(f'Status {response.status}: Currently cannot request from Reddit')

    """ Commands """

    @comms.command(name='r/random')
    async def user(self, ctx):
        info = await self.aiohttp_requester(ctx, 'https://oauth.reddit.com/random')
        with open(path('repository', 'tmp', 'info.json'), 'w') as f:
            json.dump(info, f)


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
