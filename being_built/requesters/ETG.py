"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from bs4 import BeautifulSoup
import platform
import aiohttp

from discord.ext import commands as comms
import discord

from handlers.modules.output import printc, now


class ETG_Requester(comms.Cog):
    """ Get information from the enter the gungeon wiki """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task for checking token
        """
        self.bot = bot
        self.load_service = self.bot.loop.create_task(self.load_ETG())

    def cog_unload(self):
        """ Cancel background task(s) when cog is unloaded """
        self.load_service.cancel()

    """ Background tasks """

    async def load_ETG(self):
        """ Checks if ETG service is accessable """
        await self.bot.wait_until_ready()
        if not self.bot.is_closed():
            self.active_ETG = False
            if not self.active_ETG:
                printc('[...]: CHECKING ETG SERVICE AVAILABILITY')
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://enterthegungeon.gamepedia.com/Guns') as test_response:
                        if test_response.status == 200:
                            printc('[ ! ]: ETG SERVICE AVAILABLE')
                            self.active_ETG = True
                        else:
                            raise ValueError(f'[WARNING]: ETG SERVICE NOT AVAILABLE {test_response}')

    """ Commands """
    @comms.command()
    async def etg(self, ctx, item):
        """ Helps the user with ETG commands """
        if item not in ['guns', 'items', 'gungeoneers', 'bosses']:
            embed = discord.Embed(title='`Usage of the Enter the Gungeon (ETG) commands`', colour=0xc27c0e, timestamp=now())
            help = '''
            `$etg <> <>`
            `<>`: ``
            `<>`: ``
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)
        else:
            await self.ETG_check_object(ctx, item.title())

    async def ETG_check_object(self, ctx, item):
        base_url = 'https://enterthegungeon.gamepedia.com/'
        url = f'{base_url}{item}'
        obj = ' '.join(ctx.message.content.split()[2:])
        await ctx.send(f'Getting information for object {item}: {obj}')
        if self.active_ETG:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    if r.status == 200:
                        data = await r.read()
                        soup = BeautifulSoup(data, "lxml")
                        table = soup.find('table')
                        found = False
                        for tag in table.find_all('tr'):
                            for nextTag in tag.find_all('a', class_='image'):
                                testGun = nextTag.find_all('img')[0]['alt']
                                if testGun[:testGun.index('.')] in [obj, obj.lower()]:
                                    thumbnail = nextTag.find_all('img')[0]['src']
                                    b_tags = [x.text.strip() for x in tag.find_all('b')]
                                    td_tags = [x.text.strip() for x in tag.find_all('td')]
                                    all_tags = list(zip(b_tags, td_tags))
                                    print(all_tags)
                                    embed = discord.Embed(title='Enter The Gungeon information', colour=0xc27c0e, timestamp=now())
                                    embed.set_thumbnail(url=thumbnail)
                                    embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                                    await ctx.send(embed=embed)
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            await ctx.send(f'ETG: item {obj} of type {item} could not be found')
                    else:
                        await ctx.send(f'ETG: status code {r.status}')


def setup(bot):
    bot.add_cog(ETG_Requester(bot))
