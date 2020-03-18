"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms

from modules import http_get


class Custom(comms.Cog):
    """Very customizable commands, like requests or executions.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    async def cog_check(self, ctx):
        """Checks if user if owner.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            True or false based off of if user is an owner of the bot.

        """
        return await self.bot.is_owner(ctx.author)

    @comms.command()
    async def request(self, ctx, *, url: str = 'https://httpbin.org/get'):
        """Requesting from a specific url.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            url (str, optional): The url of the service that you would like to request from.

        """
        info = await http_get(url, session=self.bot.session, block=True)
        await ctx.author.send(info, delete_after=10)


def setup(bot):
    bot.add_cog(Custom(bot))
