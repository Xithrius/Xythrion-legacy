"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""

'''

    @comms.Cog.listener()
    async def on_message(self, message):
        """
        Blocking and logging whatever happens on servers that client is present on
        """

        # Logging messages for charts and the COH leveling system
        if str(message.author) != str(self.bot.user):
            try:
                with open(path('repository', 'logs', f'{message.author}.txt'), 'a') as f:
                    f.write(f'{message.created_at}~~~{message.guild}\n')
                with open(path('repository', 'logs', f'{message.author}.txt'), 'r') as f:
                    length = len(f.readlines())
                    if length == 1:
                        embed = discord.Embed(title=f'`Leveling system activated for user {message.author}!`', colour=0xc27c0e, timestamp=now())
                        info =
                        `You have been initiated to ascend into the next circles of hell!`
                        `You're currently starting at level 1, the first circle of hell.`
                        `Good luck on ascending to the next levels~`
                        embed.add_field(name='`Circles of hell`:', value=info)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await message.channel.send(embed=embed)
                    elif length % 75 == 0:
                        embed = discord.Embed(title=f'`User {message.author} has ascended!`', colour=0xc27c0e, timestamp=now())
                        info = {message.author.mention} `stats`:
                        `Circle of hell reached`: `Level {int(length / 75)}`
                        `Total messages sent:` `{length}`
                        embed.add_field(name='`Circles of hell`:', value=info)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await message.channel.send(embed=embed)
            except FileNotFoundError:
                with open(path('repository', 'logs', f'{message.author}.txt'), 'w') as f:
                    f.write(f'{message.created_at}~~~{message.guild}\n')

    """

    Commands

    """
    @comms.command(name='rank')
    async def check_COH_rank(self, ctx):
        levels = len((open(path('repository', 'logs', f'{ctx.message.author}.txt'), 'r')).readlines())
        embed = discord.Embed(title=f'`Current circle of hell for user {ctx.message.author}`', colour=0xc27c0e, timestamp=now())
        info =
        {ctx.message.author.mention} `stats`:
        `Current circle of hell`: `Level {round((levels / 75), 4)}`
        `Total messages sent:` `{levels}`
        embed.add_field(name='`Info`:', value=info)
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)
'''
