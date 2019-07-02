"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import platform
import json

from discord.ext import commands as comms
import discord

from handlers.modules.output import path


class Spotify_Detector(comms.Cog):
    """ Messages the user about spotify updates """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task for checking token
        """
        self.bot = bot
        self.background_service = self.bot.loop.create_task(self.update_detector())
        with open(path('repository', 'user_config', 'spotify.json'), 'r') as f:
            self.spotify_list = json.load(f)

    def cog_unload(self):
        """ Cancel background task(s) when cog is unloaded """
        self.background_service.cancel()

    """ Background tasks """

    async def update_detector(self):
        """ """
        await self.bot.wait_until_ready()
        # while not self.bot.is_closed():
        if not self.bot.is_closed():
            pass

    """ Commands """

    @comms.group()
    async def spotify(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('You can either enable or disable spotify notifications through discord. **There are no other options.**')

    @spotify.command()
    async def enable(self, ctx):
        self.spotify_list.append(ctx.message.author)

    @spotify.command()
    async def disable(self, ctx):
        pass

    @comms.command()
    async def spotify_playing(self, ctx):
        try:
            embed = discord.Embed(title=f'Currently playing for {ctx.author.name}:\n__*{ctx.author.activities[0].title} by {ctx.author.activities[0].artist}*__', colour=0xc27c0e)
            embed.set_author(name='Xithrius', icon_url='https://i.imgur.com/wzl5IHi.png')
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Spotify_Detector(bot))
