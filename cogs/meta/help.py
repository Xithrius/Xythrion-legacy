"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms

from modules import gen_block
from tabulate import tabulate


class Help(comms.Cog):
    """Helping users interacting with the bot.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command(name='help', aliases=['idk'])
    async def _help(self, ctx, *, c: str = None):
        """Getting the user help with the bot.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]help
            >>> [prefix]help info

        """
        available_commands = sum([list(v.keys()) for v in self.bot.help_info.values()], [])

        # Getting information on the command
        if c and c.lower() in available_commands:
            for k, v in self.bot.help_info.items():
                if c.lower() in v.keys():
                    d = self.bot.help_info[k][c]
                    break
            table = [f'Help for the command "{c}":\n'] + tabulate(d.items()).split('\n')

        # If command cannot be found
        elif c and c.lower() not in available_commands:
            text = f'Command "{c}" not found. Here are all the options:'
            lst = [[k, ', '.join(str(y) for y in v.keys())] for k, v in self.bot.help_info.items()]
            table = [text] + tabulate(lst, ['Cogs', 'Commands']).split('\n')

        # Prints all available commands and their cogs.
        else:
            text = f'For specific command help (not cogs): "{self.bot.command_prefix}help [command]"\n'
            lst = [[k, ', '.join(str(y) for y in v.keys())] for k, v in self.bot.help_info.items()]
            table = [text] + tabulate(lst, ['Cogs', 'Commands']).split('\n')

        await ctx.send(gen_block(table))


def setup(bot):
    bot.add_cog(Help(bot))
