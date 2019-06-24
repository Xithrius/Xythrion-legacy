'''
>> ARi0
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import platform
import time
import asyncio

from discord.ext import commands as comms
import discord

from ARi0.containers.QOL.shortened import now
from ARi0.containers.QOL.pathing import path
from ARi0.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Porgram evaluator
# //////////////////////////////////////////////////////////////////////////// #
# Returning evaluations of programs
# //////////////////////////////////////////////////////////////////////////// #


class Program_Evaluator(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    @comms.command()
    @comms.is_owner()
    async def exec(self, ctx):
        msg = ctx.message.content[9:len(ctx.message.content) - 4]
        if msg[0:2] == 'py':
            msg = msg[3:]
            try:
                print(f'[{now()}] RUNNING PROGRAM:')
                print('```py')
                print(msg)
                print('```')
                print(f'OUTPUT')
                start_time = time.time()
                exec(msg)
                finish_time = round((time.time() - start_time), 3)
                await ctx.send(f':white_check_mark: Program finished in {finish_time}s')
            except Exception as e:
                print(e)
                await ctx.send(f':x:{e}')


def setup(bot):
    bot.add_cog(Program_Evaluator(bot))
