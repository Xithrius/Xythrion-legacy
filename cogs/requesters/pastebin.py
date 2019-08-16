"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord

from handlers.modules.output import path, now, get_filename


class Pastebin_Requester(comms.Cog):
    """ Requester for pastebin """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Permission checking """

    async def cog_check(self, ctx):
        """ """
        return ctx.message.author.id in self.bot.owner_ids

    """ Commands """

    @comms.command()
    async def c_pastebin(self, ctx, url):
        """ """
        i = url.rfind('/')
        url = f'{url[:i]}/raw{url[i:]}'
        await ctx.send(url)
        async with self.s.get(url) as r:
            assert r.status == 200
            info = await r.text()


def setup(bot):
    bot.add_cog(Pastebin_Requester(bot))
