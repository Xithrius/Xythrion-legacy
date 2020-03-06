"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
import discord


class Responses(comms.Cog):
    """Learning how to respond to other users

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

    @comms.Cog.listener()
    async def on_message(self, message):
        """Records every single message sent by users for ranking.
        
        Args:
            message (discord.Message): Represents a message from Discord 

        """
        pass

    @comms.command(enabled=False)
    @comms.cooldown(1, 5, BucketType.user)
    async def respond(self, ctx):
        """Adds a response for the bot to a specific line, whoever gets the most repeats occurs the most.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        """
        pass


def setup(bot):
    bot.add_cog(Responses(bot))
