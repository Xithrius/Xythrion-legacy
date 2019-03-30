#!/usr/bin/env python


'''

MIT License

Copyright (c) 2019 Xithrius

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import asyncio

from discord.ext import commands as comms

# from essentials.pathing import path, mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


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
