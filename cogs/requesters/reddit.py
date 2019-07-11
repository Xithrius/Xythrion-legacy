"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import json
import aiohttp
import random

from discord.ext import commands as comms
import discord

from handlers.modules.output import printc, path, aiohttp_requester, now


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
            f = self.bot.config.reddit
            self.client_auth = aiohttp.BasicAuth(login=f.client_ID, password=f.client_secret)
            post_data = {"grant_type": "password", "username": f.username, "password": f.password}
            headers = {"User-Agent": f"Xiux/{self.bot.__version__} by {f.username}"}
            async with aiohttp.ClientSession(auth=self.client_auth, headers=headers) as session:
                async with session.post("https://www.reddit.com/api/v1/access_token", data=post_data) as test_response:
                    if test_response.status == 200:
                        js = await test_response.json()
                        self.active_reddit = True
                        printc('[ ! ]: REDDIT SERVICE AVAILABLE')
                        self.headers = {"Authorization": f"bearer {js['access_token']}", **headers}
                        await asyncio.sleep(js['expires_in'])
                    else:
                        printc(f'WARNING: REDDIT REQUESTS CANNOT BE ACTIVATED. ERROR CODE: {test_response.status}')

    """ Commands """

    @comms.command(name='r/search')
    async def search_subreddits(self, ctx, query):
        info = await aiohttp_requester(ctx, 'POST', 'https://oauth.reddit.com/api/search_subreddits', self.headers, {'query': query, 'include_over_18': True})
        info = info['subreddits']
        embed = discord.Embed(title=f'Reddit subreddit query for {query}', colour=0xc27c0e, timestamp=now())
        for i in range(5):
            try:
                q_info = {'Link': f"https://www.reddit.com/r/{info[i]['name']}",
                          'Subscribers': info[i]['subscriber_count'],
                          'Active users': info[i]['active_user_count']}
                q_info = '\n'.join(f'**{k}**: {v}' for k, v in q_info.items())
                embed.add_field(name=f'__Query #{i + 1}__', value=q_info, inline=False)
            except IndexError:
                break
        await ctx.send(embed=embed)

    @comms.command(name='r/top')
    async def topIn_subreddit(self, ctx, subreddit, top=5):
        info = await aiohttp_requester(ctx, 'GET', f'https://oauth.reddit.com/r/{subreddit}/top', self.headers, {'t': 'all', 'count': 1})
        info = info['data']['children']
        embed = discord.Embed(title=f'Top {top} posts of r/{subreddit}', colour=0xc27c0e, timestamp=now())
        for i in range(top):
            I = info[i]['data']
            try:
                q_info = {'Title': I['title'],
                          'Link': f"https://www.reddit.com{I['permalink']}",
                          'Upvotes': I['ups']}
                q_info = '\n'.join(f'**{k}**: {v}' for k, v in q_info.items())
                embed.add_field(name=f'__Top post #{i + 1}__', value=q_info, inline=False)
            except IndexError:
                break
        await ctx.send(embed=embed)

    @comms.command(name='r/preview')
    async def previewIn_subreddit(self, ctx, subreddit):
        info = await aiohttp_requester(ctx, 'GET', f'https://oauth.reddit.com/r/{subreddit}/top', self.headers, {'t': 'all', 'limit': 100})
        info = info['data']['children'][random.randint(1, 25)]['data']
        embed = discord.Embed(title=f'Preview of the {subreddit} subreddit', colour=0xc27c0e, timestamp=now())
        q_info = {'Title': info['title'], 'Link': f"https://www.reddit.com{info['permalink']}", 'Upvotes': info['ups']}
        q_info = '\n'.join(f'**{k}**: {v}' for k, v in q_info.items())
        embed.add_field(name='__**Info on post**__', value=q_info, inline=False)
        embed.set_image(url=info['url'])
        await ctx.send(embed=embed)

    @comms.command(name='r/hot')
    async def hotIn_subreddit(self, ctx, subreddit, amount=25):
        info = await aiohttp_requester(ctx, 'GET', f'https://oauth.reddit.com/r/{subreddit}/hot', self.headers, {'g': 'GLOBAL', 'count': amount})
        info = info['data']['children']
        for i in range(amount):
            embed = discord.Embed(title=f'Currently hot on the {subreddit} subreddit', colour=0xc27c0e, timestamp=now())
            I = info[random.randint(1, amount)]['data']
            try:
                if I['stickied']:
                    raise KeyError
                q_info = {'Link': f"https://www.reddit.com{I['permalink']}",
                          'Upvotes': I['ups']}
                q_info = '\n'.join(f'**{k}**: {v}' for k, v in q_info.items())
                embed.add_field(name=f"__{I['title']}__", value=q_info, inline=False)
                if not I['is_video']:
                    embed.set_image(url=I['url'])
                break
            except KeyError:
                continue
        if I['is_video']:
            await ctx.send(content=I['url'], embed=embed)
        else:
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
