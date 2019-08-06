"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""

import os
import shutil

from discord.ext import commands as comms
import discord

from handlers.modules.output import path


class Cog_Builder(comms.Cog):
    """ Commands with a small amount of personality """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Commands """

    @comms.command()
    @comms.is_owner()
    async def create_cog(self, ctx, cog_type, cog_name):
        types = [_type[:-1] for _type in os.listdir(path('cogs'))]
        cog_type = cog_type.lower()
        cog_name = cog_name.lower()
        file = f'{cog_name}.py'
        if cog_type not in types:
            await ctx.send(f'Unknown cog type {cog_type}. Accepted types: {", ".join(str(y) for y in types)}')
            return
        if os.path.isfile(path('cogs', f'{cog_type}s', cog_name)):
            await ctx.send(f'Cog {cog_name} in {cog_type}s already exists')
        shutil.copy2(path('repository', 'cog_parts', 'cog.txt'), path('cogs', f'{cog_type}s', file))
        replacedata = {
            'Cog_Type': f'{cog_name.title()}_{cog_type.title()}',
            'placeholder': cog_name,
            'desc': f'{cog_type.title()} for {cog_name}'
        }
        with open(path('repository', 'cog_parts', 'cog.txt'), 'r') as f:
            filedata = f.read()
            for k, v in replacedata.items():
                filedata = filedata.replace(k, v)
        with open(path('cogs', f'{cog_type}s', file), 'w') as f:
            f.write(filedata)
        await ctx.send(f'Cog {cog_name} successfully built. Loading into bot...')
        try:
            cog_path = f'cogs.{cog_type}s.{cog_name}'
            self.bot.load_extension(cog_path)
            self.bot.attached_extensions.append(cog_path)
            await ctx.send(f'Cog {cog_name} successfully loaded into bot')
        except Exception as e:
            await ctx.send(f'Fatal error loading {cog_name}: {e}')


def setup(bot):
    bot.add_cog(Cog_Builder(bot))
