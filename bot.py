"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info

The main file for the graphing bot.

Running the bot (python 3.8+):
    First time usage:
        $ python -m pip install --user -r requirements.txt
    Starting the bot:
        $ python bot.py

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""


import json

from discord.ext import commands as comms

from modules.output import path


class Xythrion(comms.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open(path('config', 'config.json'), ) as f:
            self.token = json.load(f)['discord']

        self.add_cog(Main_Cog(self))

    async def on_ready(self):
        pass

    async def close(self):
        await super().close()


class Main_Cog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @comms.command()
    async def exit(self, ctx):
        await ctx.bot.logout()


if __name__ == "__main__":

    #: Running the bot
    bot = Xythrion(command_prefix=comms.when_mentioned_or(';'),
                   case_insensitive=True)
    bot.run(bot.token, bot=True, reconnect=True)
