from discord.ext import commands as comms
import discord
import datetime
import sys


class WarningsCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command(hidden=True)
    async def cleanup(self, ctx):
        pass

# Events
    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @comms.Cog.listener()
    async def on_disconnect(self):
        print(f'')

    @comms.Cog.listener()
    async def on_member_update(self, before, after):
        pass

    @comms.Cog.listener()
    async def on_message(self, message):
        # Logging the message into the console and saving in it's own file
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        try:
            if 'log' == sys.argv[1]:
                print(f"guild: '{message.guild}', channel: '{message.channel}', user: '{message.author}' sends:\n\t[{now}]  '{message.content}'")
        except IndexError:
            pass
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
