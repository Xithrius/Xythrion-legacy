"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import random

from discord.ext import commands as comms

from modules.shortcuts import embed


class Reddit_Requester(comms.Cog):
    """ """

    def __init__(self, bot):

        #: Setting Xythrion(comms.Bot) as a class attribute
        self.bot = bot

    """ Commands """

    @comms.command()
    async def reddit(self, ctx, subreddit='all', status='hot', interval=None):
        """Sending 5 posts from a subreddit at a set interval and status.

        Args:
            status (str): The category the post should be in of the subreddit.
            interval (str): The time interval that the post should be in.
            subreddit (str): The subreddit that the posts should be found in.

        Returns:
            An embed with an image and description of the post.

        Raises:
            Possible errors if subreddit cannot be found.

        Example usage:
            (prefix)reddit pics top week

        """
        statuses = ['hot', 'new', 'controversial', 'top', 'rising']
        
        if status.lower() not in statuses:
            raise ValueError(
                f'Set status is not in options of {", ".join(str(y) for y in statuses)}.')
            return

        if status.lower() in ['hot', 'new', 'rising']:
            interval = None
        else:
            intervals = ['hour', 'day', 'week', 'month', 'year', 'all']
            if interval.lower() not in intervals:
                raise ValueError(
                    f'Set interval is not in options of {", ".join(str(y) for y in intervals)}')
                return

        if ['r/', '/r/'] in subreddit:
            subreddit = subreddit[subreddit.rindex('/') + 1:]

        if interval is None:
            url = f'https://www.reddit.com/r/{subreddit}/{status}/.json'
        else:
            url = f'https://www.reddit.com/r/{subreddit}/{status}/.json?t={interval}'

        async with self.bot.session.get(url) as r:
            assert r.status == 200
            I = await r.json()
            I = I['data']['children'][random.randint(0, 25)]['data']

        desc = {
            'Author': I['author'],
            'Upvotes': I['ups']
        }

        e = embed(I['title'], desc, {'url': I['permalink']})
        await ctx.send(content=I['url'], embed=e)

        # https://www.reddit.com/r/hentai/comments/dvr5vh/dva/
        # https://www.reddit.com/r/cosplaygirls/top/?t=week



def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
