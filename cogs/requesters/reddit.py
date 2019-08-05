"""
>> 1Xq4417
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

from handlers.modules.output import printc, path, now, get_aiohttp


class Reddit_Requester(comms.Cog):
    """ Getting information from Reddit """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Checks """

    async def cog_check(self, ctx):
        return ctx.message.author.id in self.bot.services[os.path.basename(__file__)[:-3]]

    """ Commands """

    @comms.command(name='r/search')
    async def search_subreddits(self, ctx, query):
        info = await get_aiohttp('https://oauth.reddit.com/api/search_subreddits', self.bot.services['reddit'], {'query': query, 'include_over_18': True})
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
        info = await get_aiohttp(f'https://oauth.reddit.com/r/{subreddit}/top', self.bot.services['reddit'], {'t': 'all', 'count': 1})
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
        info = await get_aiohttp(f'https://oauth.reddit.com/r/{subreddit}/top', self.bot.services['reddit'], {'t': 'all', 'limit': 100})
        info = info['data']['children'][random.randint(1, 25)]['data']
        embed = discord.Embed(title=f'Preview of the {subreddit} subreddit', colour=0xc27c0e, timestamp=now())
        q_info = {'Title': info['title'], 'Link': f"https://www.reddit.com{info['permalink']}", 'Upvotes': info['ups']}
        q_info = '\n'.join(f'**{k}**: {v}' for k, v in q_info.items())
        embed.add_field(name='__**Info on post**__', value=q_info, inline=False)
        embed.set_image(url=info['url'])
        await ctx.send(embed=embed)

    @comms.command(name='r/hot')
    async def hotIn_subreddit(self, ctx, subreddit, amount=25):
        info = await get_aiohttp(f'https://oauth.reddit.com/r/{subreddit}/hot', self.bot.services['reddit'], {'g': 'GLOBAL', 'count': amount})
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
