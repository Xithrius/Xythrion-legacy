"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info

Todo:
    * Nothing at this current moment

"""


import asyncio
import json
import aiohttp
import random
import os

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, now


class Reddit_Requester(comms.Cog):
    """Getting information from Reddit."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Permission checking """

    async def cog_check(self, ctx):
        """Checks user permissions from config file.

        Args:
            ctx: Context object where the command is called.

        Returns:
            True if user has permissions, False otherwise.

        """
        return ctx.message.author.id in self.bot.owner_ids

    """ Commands """

    @comms.group()
    async def reddit(self, ctx):
        """Reddit group command.

        Args:
            ctx: Context object where the command is called.

        Returns:
            Gives the command for help if no subcommand is called.

        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Type the command **.help {ctx.command}** for help')

    @reddit.command()
    async def top(self, ctx, subreddit, amount=1):
        """

        Args:
            ctx: Context object where the command is called.
            subreddit: The name of a subreddit.
            amount: How many links are to be provided (between 1 and 25).

        Returns:
           An embed with information or a list of link(s).

        """
        try:
            amount = int(amount)
            if amount not in range(1, 26):
                raise ValueError
        except ValueError:
            await ctx.send('Amount can only be in between 1 and 25')
        async with self.bot.s.get(f'https://www.reddit.com/r/{subreddit}/top/.json?t=all') as r:
            assert r.status == 200
            info = await r.json()
            info = info['data']['children']
            if amount in range(2, 26):
                info = info[:amount]
                embed = discord.Embed(title=f'**Top {amount} posts from r/{subreddit}**', colour=self.bot.ec)
                e_info = [f'#{num + 1}: [{i["data"]["title"]}](https://reddit.com{i["data"]["permalink"]})' for num, i in enumerate(info)]
                embed.description = '\n'.join(str(y) for y in e_info)
                await ctx.send(embed=embed)
            elif amount == 1:
                info = info[0]['data']
                temp_info = [
                    info['url'],
                    f"`#1 top post from r/{subreddit}: '{info['title']}'`",
                    f"`OP: u/{info['author_fullname']}, Upvotes: {info['ups']}`"
                ]
                await ctx.send('\n'.join(str(y) for y in temp_info))

    @reddit.command()
    async def hot(self, ctx, subreddit, amount=1):
        """

        Args:
            ctx: Context object where the command is called.
            subreddit: The name of a subreddit.
            amount: How many links are to be provided (between 1 and 25).

        Returns:
            An embed with information or a list of link(s).

        """
        try:
            amount = int(amount)
            if amount not in range(1, 26):
                raise ValueError
        except ValueError:
            await ctx.send('Amount can only be in between 1 and 25')
        async with self.bot.s.get(f'https://www.reddit.com/r/{subreddit}/hot.json') as r:
            assert r.status == 200
            info = await r.json()
            info = info['data']['children']
            info = sorted(info, key=lambda x: x['data']['ups'], reverse=True)
            if amount in range(2, 26):
                info = info[:amount]
                embed = discord.Embed(title=f'**Top {amount} posts from r/{subreddit}**', colour=self.bot.ec)
                e_info = [f'#{num + 1}: [{i["data"]["title"]}](https://reddit.com{i["data"]["permalink"]})' for num, i in enumerate(info)]
                embed.description = '\n'.join(str(y) for y in e_info)
                await ctx.send(embed=embed)
            elif amount == 1:
                info = info[0]['data']
                temp_info = [
                    info['url'],
                    f"`#1 hot post from r/{subreddit}: '{info['title']}'`",
                    f"`OP: u/{info['author_fullname']}, Upvotes: {info['ups']}`"
                ]
                await ctx.send('\n'.join(str(y) for y in temp_info))

    """ Events """

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Catches errors specifically within this cog

        Args:
            ctx: Context object where the command is called.
            error: Error object of what the command caused.

        Returns:
            A specific string depending on the error within the cog.

        """
        if ctx.command.cog_name == self.__class__.__name__:
            await ctx.send('Requester failed to get subreddit information.')


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
