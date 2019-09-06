"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info


This is the main Python file for the discord.py bot, as all important attributes,
checks, and background tasks are created here.

Example:
    First time usage (do it every so often to keep updated packages):
        $ py -3 -m pip install --user -r requirements.txt
    To run the bot:
        $ py -3 bot.py

Todo:
    * Literally rewrite the repository

"""


import collections
import json
import asyncio

from discord.ext import commands as comms

from modules.output import path, ds


class Robot(comms.Bot):
    """Creating connections, attributes, and background tasks.
    
    Preface: When ctx is args, it gives context on where the method was called, such as channel, member, and guild.
    
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #: Opening the config json file
        with open(path('config', 'config.json'), 'r', encoding='utf8') as f:
            config = json.load(f)

        #: Giving self.config recursive attributes from config.json
        self.config = json.loads(json.dumps(config), object_hook=lambda d: collections.namedtuple('config', d.keys())(*d.values()))

        #: Create async loop for checking services
        

    async def create_service_connections(self):
        pass

    async def create_database_connection(self):
        pass

    async def test_services(self):
        pass


class RobotCog(comms.Cog):
    """Essential commands for using the bot."""

    def __init__(self, bot):
        #: Robot(comms.Bot) as a class attribute
        self.bot = bot

    @comms.command()
    async def exit(self, ctx):
        ds.w('Logging out.')
        await ctx.bot.logout()


class InfoCog(comms.Cog):
    """Cog is meant to give information about owner and bot interactions."""

    def __init__(self, bot):
        #: Robot(comms.Bot) as a class attribute
        self.bot = bot

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot. It is not 'essential', but it's still useful.
        
        Returns:
            The invite link so the bot can be invited to a server.
        
        """
        await ctx.send(f'https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=32885952')

    @comms.command()
    async def about(self, ctx):
        """Returns information about this bot's origin
        
        Returns:
            An embed object with links to creator's information and bot's repository.
        
        """
        info = {
            'Twitter': 'https://twitter.com/_Xithrius',
            'Github': 'https://github.com/Xithrius/Xythrion'
        }
        embed = discord.Embed(title='Project creation date: March 30, 2019', description='\n'.join(f'[`{k}`]({v})' for k, v in info.items()), colour=self.bot.ec)
        await ctx.send(embed=embed)

    @comms.command()
    async def website(self, ctx):
        """Returns website for the bot (this replaced the README).
        
        Returns:
            An embed object containing the website link for the bot.
        
        """
        embed = discord.Embed(description='`https://xithrius.github.io/Xythrion/`')
        await ctx.send(embed=embed)


if __name__ == "__main__":
    bot = Robot(command_prefix=comms.when_mentioned_or('.'))
    bot.add_cog(RobotCog(bot))
    bot.add_cog(InfoCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
