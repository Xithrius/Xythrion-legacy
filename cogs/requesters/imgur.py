"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
# import discord

# from modules.output import get_filename, cs, now, path


class Imgur_Requester(comms.Cog):
    """ """

    def __init__(self, bot):

        #: Setting Xythrion(comms.Bot) as a class attribute
        self.bot = bot


def setup(bot):
    bot.add_cog(Imgur_Requester(bot))
