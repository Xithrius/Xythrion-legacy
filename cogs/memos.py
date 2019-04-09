'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import datetime
import asyncio

from discord.ext import commands as comms


# ///////////////////////////////////////////////////////// #
# Memo cog
# ////////////////////////
# Cog for reminding people of things that aren't stocks
# ///////////////////////////////////////////////////////// #


class MemosCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.check_reminder())

    def cog_unload(self):
        self.bg_task.cancel()

# Background tasks
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
