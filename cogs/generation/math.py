"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms


class Math(comms.Cog):
    """Doing math without commands.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Events """

    # @comms.Cog.listener()
    # async def on_message(self, message):
    #     eq = re.search(r'\-*\d{1,5}\^\-*\d{1,5}', message.content)
    #     try:
    #         eq = eq.group().split('^')
    #         embed = discord.Embed(description=f'`{eq[0]}^{eq[1]} = {float(eq[0]) ** float(eq[1])}`')
    #         await message.channel.send(embed=embed)
    #     except (IndexError, AttributeError, discord.errors.HTTPException):
    #         pass


def setup(bot):
    bot.add_cog(Math(bot))
