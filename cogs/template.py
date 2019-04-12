'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries
# /////////////////////////////////////////////////////////
# Built-in modules, third-party modules, custom modules
# //////////////////////////////////////////////////////////////////////////// #


import asyncio

from discord.ext import commands as comms
# import discord

# from essentials. import


# //////////////////////////////////////////////////////////////////////////// #
#
# /////////////////////////////////////////////////////////
#
# //////////////////////////////////////////////////////////////////////////// #


class TemplateCog(comms.Cog):

    # //////////////////////// # Object(s): bot and background task(s)
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.check_stock_reminders())

    # //////////////////////// # Cancel background task(s) when cog is unloaded
    def cog_unload(self):
        self.bg_task.cancel()

# //////////////////////////////////////////////// # Commands
    # //////////////////////// # Description
    @comms.command()
    async def foo(self, ctx):
        pass

# //////////////////////////////////////////////// # Events
    # //////////////////////// # Description
    @comms.Cog.listener()
    async def on_foo_event(self, ctx):
        pass

# //////////////////////////////////////////////// # Background tasks
# //////////////////////// # Description
    async def foo_reminder(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(TemplateCog(bot))
