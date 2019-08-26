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
    async def top(self, ctx, subreddit, amount):
        """

        Args:
            ctx: Context object where the command is called.
            subreddit: The name of a subreddit.
            amount: How many links are to be provided (between 1 and 25).

        Returns:
            An embed with a list or a single list of top link(s).

        """
        try:
            amount = int(amount)
            if amount not in range(1, 26):
                raise ValueError
        except ValueError:
            await ctx.send('Amount can only be in between 1 and 25')
        async with self.bot.s.get(f'https://www.reddit.com/r/{subreddit}/top.json') as r:
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
                embed = discord.Embed(title=f"#1 post from r/{subreddit}: {info['title']}", colour=self.bot.ec)
                embed.set_image(url=info['url'])
                embed.set_footer(text=f'OP: u/{info["author_fullname"]}, Upvotes: {info["ups"]}')
                await ctx.send(embed=embed)

    @reddit.command()
    async def hot(self, ctx, subreddit, amount=5):
        """

        Args:
            ctx: Context object where the command is called.
            subreddit: The name of a subreddit.
            amount: How many links are to be provided (between 1 and 25).

        Returns:
            An embed with a list or a single list of hot link(s).

        """
        pass

    @reddit.command()
    async def search(self, ctx, subreddit, amount=5):
        """

        Args:
            ctx: Context object where the command is called.
            subreddit: The name of a subreddit
            amount: How many links are to be provided (between 1 and 25)

        Returns:
            An embed with a list or a single list of queries that are similar to the search.

        """
        pass

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
        print(error)
        # if ctx.command.cog_name == os.path.basename(__file__)[:-3] and type(error).__name__ == AssertionError:
        #    await ctx.send(f'Command **{ctx.command}** has failed at requesting information.')


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
