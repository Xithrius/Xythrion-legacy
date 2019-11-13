"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
# import discord

# from modules.output import get_filename, cs, now, path


class Reddit_Requester(comms.Cog):
    """ """

    def __init__(self, bot):

        #: Setting Xythrion(comms.Bot) as a class attribute
        self.bot = bot

    """ Checks """

    async def cog_check(self, ctx):
        """Checks if the command caller is an owner.

        Returns:
            True or false, on config.json's 'owner' contents.

        """
        # return await self.bot.is_owner(ctx.author)
        return True

    """ Commands """

    @comms.command()
    async def a_command(self, ctx):
        """Description

        Args:
            None

        Raises:
            None

        Returns:
            None

        """
        pass

    """ Events """

    @comms.Cog.listener()
    async def on_something(self):
        """Description

        Args:
            None

        Raises:
            None

        Returns:
            None

        """
        pass


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
