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


class Reddit_Requester(comms.Cog):
    """ Getting information from reddit """

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
        while not self.bot.is_closed():
            self.active_reddit = False
            if not self.active_reddit:
                f = json.load(open(path('Xiux', 'configuration', 'config.json')))['reddit']
                client_auth = aiohttp.BasicAuth(login=f['client_ID'], password=f['client_secret'])
                post_data = {"grant_type": "password", "username": f['username'], "password": f['password']}
                # headers = {"User-Agent": f"Xiux/{Xiux.__version__} by {f['username']}"}
                async with aiohttp.ClientSession(auth=client_auth, headers=headers) as session:
                    async with session.post("https://www.reddit.com/api/v1/access_token", data=post_data) as test_response:
                        if test_response.status == 200:
                            js = await test_response.json()
                            if js != {'error': 'invalid_grant'}:
                                self.active_reddit = True
                                await asyncio.sleep(js['expires_in'] + 1)
                                # self.headers = {"Authorization": f"{response['token_type']} {response['access_token']}", "User-Agent": f"Xiux.py/{Xiux.__version__} by {f['username']}"}
                                # response = requests.get('https://oauth.reddit.com/api/v1/me', headers=self.headers).json()
                                printc('[ ! ]: REDDIT REQUESTS ENABLED')
                            else:
                                printc(f'WARNING: BROKEN REDDIT REQUESTER. ERROR CODE: {js}')
                                break
                        else:
                            printc(f'WARNING: REDDIT REQUESTS CANNOT BE ACTIVATED. ERROR CODE: {test_response.status}')
                            break

    """ Commands """

    @comms.group(name='r/')
    async def subreddit_requests(self, ctx):
        """ Subreddit group command """
        if ctx.invoked_subcommand is None:
            pass

    @subreddit_requests.command(name='info')
    async def subreddit_top(self, ctx, subreddit):
        """ Request subreddit information """
        if self.active_reddit:
            pass
        else:
            await ctx.send('Requesting from reddit is currently unavalible')

    @comms.group(name='u/')
    async def reddit_user_requests(self, ctx):
        """ Reddit user group command """
        if ctx.invoked_subcommand is None:
            pass

    @reddit_user_requests.command(name='info')
    async def reddit_user_info(self, ctx, user):
        """ Request reddit user information """
        if self.active_reddit:
            pass
        else:
            await ctx.send('Requesting from reddit is currently unavalible')


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
