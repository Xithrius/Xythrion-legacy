from discord.ext import commands as comms
import discord
import asyncio


class HelpCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    @comms.command()
    async def help(self, ctx, option):
        options = []
        for i in self.bot.commands:
            print(i)
            if str(i).startswith(option):
                options.append(i)
        if len(options) == 1:
            pass
        elif len(options) > 1 and len(options) < 4:
            pass
        else:
            msg = await ctx.send('Command not found. List all commands?')
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) == '👍'

            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('👎')
            else:
                await ctx.send('👍')


def setup(bot):
    bot.add_cog(HelpCog(bot))
