"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms


class Imgur_Requester(comms.Cog):
    """ Requester for imgur """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Test command """

    @comms.command()
    async def a_test_command(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Imgur_Requester(bot))
