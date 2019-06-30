"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""

import time

from discord.ext import commands as comms

from handlers.modules.output import now


class Program_Evaluator(comms.Cog):
    """ Returning evaluations of programs """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Commands """

    @comms.command()
    @comms.is_owner()
    async def exec(self, ctx):
        """ Returns the execution of a python program """
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
                finish_time = round(((time.time() - start_time) / 1000), 3)
                await ctx.send(f':white_check_mark: Program finished in {finish_time}ms')
            except Exception as e:
                print(e)
                await ctx.send(f':x:{e}')


def setup(bot):
    bot.add_cog(Program_Evaluator(bot))
