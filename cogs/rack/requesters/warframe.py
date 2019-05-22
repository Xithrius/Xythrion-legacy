'''
>> Rehasher.py
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


from discord.ext import commands as comms


# //////////////////////////////////////////////////////////////////////////// #
# Warframe request cog
# //////////////////////////////////////////////////////////////////////////// #
# Getting information from Warframe
# //////////////////////////////////////////////////////////////////////////// #


class Warframe_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task
        """
        self.bot = bot
        self.load_script = self.bot.loop.create_task(self.load_warframe_script())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.load_script.cancel()

    """

    Background tasks

    """
    async def load_warframe_script(self):
        """
        Checks if reddit is accessable
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            pass
            '''
            self.reddit_script_active = False
            self.headers = {"Authorization": f"{response['token_type']} {response['access_token']}", "User-Agent": f"Relay.py/{relay.__version__} by {f['username']}"}
            response = requests.get('url', headers=self.headers)
            if response.json() in []:
                printc('WARNING: REDDIT ACCOUNT CANNOT BE ACTIVATED')
                await asyncio.sleep(60)
            else:
                self.reddit_script_active = True
                printc('[ ! ]: REDDIT SCRIPT CREDENTIALS ACTIVATED')
                await asyncio.sleep(reset_time + 1)
            '''
    """

    Commands

    """
    @comms.group(name='operator')
    async def operator_requests(self, ctx):
        """
        Subreddit group command
        """
        if ctx.invoked_subcommand is None:
            pass

    @operator_requests.command(name='info')
    async def operator_info(self, ctx, operator):
        pass


def setup(bot):
    bot.add_cog(Warframe_Requester(bot))
