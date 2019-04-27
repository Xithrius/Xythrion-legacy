'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import asyncio

from discord.ext import commands as comms


# //////////////////////////////////////////////////////////////////////////// #
# Template cog
# //////////////////////////////////////////////////////////////////////////// #
# Nothing to see here
# //////////////////////////////////////////////////////////////////////////// #


class TemplateCog(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task
        """
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.foo_reminder())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.bg_task.cancel()

    """
    
    Commands
    
    """
    @comms.command(hidden=True)
    @comms.guild_only()
    @comms.is_owner()
    async def foo(self, ctx):
        """
        Description
        """
        await ctx.send('Test sent')

    """
    
    Events
    
    """
    @comms.Cog.listener()
    async def on_foo_event(self, ctx):
        """
        Description
        """
        pass

    """
    
    Background tasks
    
    """
    async def foo_reminder(self):
        """
        Description
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(TemplateCog(bot))
