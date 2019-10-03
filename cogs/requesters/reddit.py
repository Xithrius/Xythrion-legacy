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

from discord.ext import commands as comms
import discord

from modules.output import path, now


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
            True if user is owner permissions and if the service is up, False otherwise.

        """
        return self.bot.requester_status['reddit']

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
        amount = int(amount)
        if amount not in range(1, 6):
            raise comms.UserInputError('Amount can only be in between 1 and 5')
        async with self.bot.s.get(f'https://www.reddit.com/r/{subreddit}/top/.json?t=all') as r:
            assert r.status == 200
            info = await r.json()
            info = info['data']['children']
            if amount in range(2, 6):
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
        amount = int(amount)
        if amount not in range(1, 6):
            raise comms.UserInputError('Amount can only be in between 1 and 5')
        async with self.bot.s.get(f'https://www.reddit.com/r/{subreddit}/hot.json') as r:
            assert r.status == 200
            info = await r.json()
            info = info['data']['children']
            info = sorted(info, key=lambda x: x['data']['ups'], reverse=True)
            if amount in range(2, 6):
                info = info[:amount]
                embed = discord.Embed(title=f'**Hot {amount} posts from r/{subreddit}**', colour=self.bot.ec)
                e_info = [f'#{num + 1}: [{i["data"]["title"]}](https://reddit.com{i["data"]["permalink"]})' for num, i in enumerate(info)]
                embed.description = '\n'.join(str(y) for y in e_info)
                await ctx.send(embed=embed)
            elif amount == 1:
                info = info[0]['data']
                temp_info = [
                    f"#1 hot post from r/{subreddit}: '{info['title']}'",
                    f"OP: u/{info['author_fullname']}, Upvotes: {info['ups']}"
                ]
                temp_info = '\n'.join(str(y) for y in temp_info)
                await ctx.send(f'```\n{temp_info}```{info["url"]}')


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
