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


import sys
import datetime

import discord
from discord.ext import commands as comms

from essentials.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
#
# /////////////////////////////////////////////////////////
#
# //////////////////////////////////////////////////////////////////////////// #


class WarningsCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# //////////////////////////////////////////////// # Commands
# //////////////////////// #
    @comms.command(hidden=True)
    async def cleanup(self, ctx):
        pass

# //////////////////////////////////////////////// # Events
# //////////////////////// # Sends error to the user
    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

# //////////////////////// # Sends warning when the bot disconnects from the network
    @comms.Cog.listener()
    async def on_disconnect(self):
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        print(f'[{now}]: WARNING: BOT HAS DISCONNECTED FROM NETWORK')

# //////////////////////// # Sends warning when there's an update in the status of a member
    @comms.Cog.listener()
    async def on_member_update(self, before, after):
        pass

# //////////////////////// # Tracking, blocking, and removing files
    @comms.Cog.listener()
    async def on_message(self, message):

        # Logging the message into the console and saving in it's own file
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        with open(path('logs', message.guild, message.channel, f'{message.author}.txt'), 'a') as f:
            f.write(f"[{now}]: 'message.content'")

        # Blocking pictures if the description doesn't want them
        pic_extensions = ['.jpg', '.png', '.jpeg', '.gif']
        for extension in pic_extensions:
            try:
                if message.attachments[0].filename.endswith(extension) and message.channel.topic == 'No pictures':
                    await message.delete()
                    await message.author.send(f'No pictures in channel {message.channel} of the server {message.guild}!')
            except IndexError:
                pass
            except discord.errors.Forbidden:
                await message.guild.owner.send(f'I should be able to remove pictures from a channel that does not want any. Please give me the permissions to do so.')


def setup(bot):
    bot.add_cog(WarningsCog(bot))
