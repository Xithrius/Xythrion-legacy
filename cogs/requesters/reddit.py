"""
>> Xylene
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
        Aiohttp session
        Required headers for requests
        """
        self.bot = bot
        self.s = aiohttp.ClientSession()
        self.h = self.bot.services[os.path.basename(__file__)[:-3]]

    """ Cog events """

    async def cog_unload(self):
        self.bot.loop.create_tank(self.s.close())

    """ Permission checking """

    async def cog_check(self, ctx):
        """ """
        _is_owner = ctx.message.author.id in self.bot.config['owners']
        return all((_is_owner, self.h))

    """ Commands """

    @comms.group()
    async def reddit(self, ctx):
        """ """
        if ctx.invoked_subcommand is None:
            pass

    @reddit.command()
    async def _search(self, ctx, query):
        """ Searches for a subreddit named similarly to <query>, returns top 5 results """
        data = {'query': query, 'include_over_18': True}
        async with self.s.get('https://oauth.reddit.com/api/search_subreddits', self.h, data) as r:
            if r.status == 200:
                _json = await r.json()
                info = _json['subreddits']
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
                await ctx.send(embed=embed, delete_after=60)
            elif r.status == 404:
                await ctx.send(f'Subreddit **{query}** could not be found.')
            else:
                await ctx.send(f'Requester failed. Status code: **{r.status}**')

    @reddit.command()
    async def _top(self, ctx, subreddit, top=5):
        """ Gives <top> links from the top of all time in <subreddit> """
        data = {'t': 'all', 'count': 1}
        async with self.s.get(f'https://oauth.reddit.com/r/{subreddit}/top', self.h, data) as r:
            if r.status == 200:
                _json = await r.json()
                info = _json['data']['children']
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
                await ctx.send(embed=embed, delete_after=60)
            elif r.status == 404:
                await ctx.send(f'Subreddit **{subreddit}** could not be found.')
            else:
                await ctx.send(f'Requester failed. Status code: **{r.status}**')

    @reddit.command()
    async def _preview(self, ctx, subreddit):
        """ Gives out a random post from the top 100 of all time in <subreddit> """
        data = {'t': 'all', 'limit': 100}
        async with self.s.get(f'https://oauth.reddit.com/r/{subreddit}/top', self.h, data) as r:
            if r.status == 200:
                _json = await r.json()
                info = _json['data']['children'][random.randint(1, 25)]['data']
                embed = discord.Embed(title=f'Preview of the {subreddit} subreddit', colour=0xc27c0e, timestamp=now())
                q_info = {'Title': info['title'], 'Link': f"https://www.reddit.com{info['permalink']}", 'Upvotes': info['ups']}
                q_info = '\n'.join(f'**{k}**: {v}' for k, v in q_info.items())
                embed.add_field(name='__**Info on post**__', value=q_info, inline=False)
                embed.set_image(url=info['url'])
                await ctx.send(embed=embed, delete_after=60)
            elif r.status == 404:
                await ctx.send(f'Subreddit **{subreddit}** could not be found.')
            else:
                await ctx.send(f'Requester failed. Status code: **{r.status}**')

    @reddit.command()
    async def _hot(self, ctx, subreddit. amount=10):
        """ Gives <amount> of links from what's currently hot in <subreddit> """
        data = {'g': 'GLOBAL', 'count': amount}
        async with self.s.get(f'https://oauth.reddit.com/r/{subreddit}/hot', self.h, data) as r:
            if r.status == 200:
                _json = await r.json()
                info = _json['data']['children']
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
                    await ctx.send(embed=embed, delete_after=60)
            elif r.status == 404:
                await ctx.send(f'Subreddit **{subreddit}** could not be found.')
            else:
                await ctx.send(f'Requester failed. Status code: **{r.status}**')


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
