"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
import discord


class Notes(comms.Cog):
    """Summary for Notes

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command()
    @comms.is_owner()
    async def create_note(self, ctx, name: str, *, note: str):
        """Creates a note and puts it into the database of all notes.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            name (str): The name of the note.
            note (str): The content of the note.

        """
        pass

    @comms.command()
    @comms.cooldown(1, 1, BucketType.user)
    async def note(self, ctx, *, query: str):
        """Searches for the note within the database. 

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            query (str): The name of the note that the user wants to search for and possibly recieve.

        """
        pass


def setup(bot):
    bot.add_cog(Notes(bot))
