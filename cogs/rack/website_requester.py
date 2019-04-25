'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries
# /////////////////////////////////////////////////////////
# Built-in modules, third-party modules, custom modules
# //////////////////////////////////////////////////////////////////////////// #


from lxml import html
import requests

from discord.ext import commands as comms


# //////////////////////////////////////////////////////////////////////////// #
# Reddit requester cog
# //////////////////////////////////////////////////////////////////////////// #
# Getting information from reddit
# //////////////////////////////////////////////////////////////////////////// #


class Reddit_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s): bot """
        self.bot = bot

# //////////////////////////////////////////////// # Commands

    @comms.command(name='karma', hidden=True)
    @comms.is_owner()
    async def request_karma(self, ctx, user):
        """ Gets the amount of karma a user has """
        try:
            karma = (html.fromstring((requests.get(f'https://www.reddit.com/u/{user}/')).content)).xpath('//*[@id="profile--id-card--highlight-tooltip--karma"]/text()')
            await ctx.send(f'User {user} has {karma} karma')
        except IndexError:
            await ctx.send(f'User {user} could not be found')


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
