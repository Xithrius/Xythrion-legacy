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
import datetime

from discord.ext import commands as comms


# //////////////////////////////////////////////////////////////////////////// #
# Memos cog
# /////////////////////////////////////////////////////////
# Reminds people of what they want at inputted date and time
# //////////////////////////////////////////////////////////////////////////// #


class MemosCog(comms.Cog):

    # //////////////////////// # Object(s): bot and background task(s)
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.check_reminder())

    # //////////////////////// # Cancel background task(s) when cog is unloaded
    def cog_unload(self):
        self.bg_task.cancel()

# //////////////////////////////////////////////// # Background tasks
    # //////////////////////// # Checking for reminders
    async def check_reminder(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            if datetime.datetime.today().weekday() >= 0 and datetime.datetime.today().weekday() <= 4:
                if datetime.datetime.now().hour == 16:
                    if datetime.datetime.now().minute >= 0:
                        pass
            await asyncio.sleep(10)


def setup(bot):
    bot.add_cog(MemosCog(bot))
