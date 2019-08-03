"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime
import secrets

from discord.ext import commands as comms
import discord

from handlers.modules.output import now


class Simples_Cog(comms.Cog):
    """ A cog for all the simple commands """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Commands """

    @comms.command()
    async def from_timestamp(self, ctx, stamp):
        """ Converts from timestamp to readable time """
        dt_object = datetime.datetime.fromtimestamp(int(stamp))
        await ctx.send(f'**Date from timestamp:** {dt_object}')

    @comms.command()
    async def time(self, ctx):
        """ Gets the current time. Will be based on user time zone soon """
        await ctx.send(f'**Current time:** {now()}')

    @comms.command(name='members')
    @comms.guild_only()
    async def get_members(self, ctx):
        """ Get all users that exist within the guild """
        embed = discord.Embed(name=f'Members on the server', value=f'{ctx.message.guild}', colour=0xc27c0e, timestamp=now())
        embed.add_field(name='Members:', value=', '.join(str(x) for x in ctx.message.guild.members))
        await ctx.send(embed=embed)

    @comms.command(name='password')
    async def random_password(self, ctx, userRange=14):
        """ Give a random password to the user """
        await ctx.send(secrets.token_urlsafe(userRange))

    @comms.command()
    async def invite(self, ctx):
        """ Gives an invite like for the bot, with barely any permissions """
        await ctx.send(f'https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=32885952')

    @comms.command()
    async def ping_vc(self, ctx):
        """ Pings everyone that's in the same voice channel as the caller """
        vc = ctx.message.author.voice.channel.members
        print(vc)

    @comms.command()
    async def user_icon(self, ctx, member: discord.Member):
        """ Returns the user icon """
        await ctx.send(member.avatar_url)

    @comms.command()
    async def purge(self, ctx, amount=10):
        """ Deletes an amount of messages """
        try:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
        except Exception as e:
            print(e)

    @comms.command()
    async def emojis(self, ctx):
        emojis = [str(i) + '\N{combining enclosing keycap}' for i in range(10)]
        emojis.append('\N{keycap ten}')
        embed = discord.Embed(title=f'**Emojis 0-10**\n{" ".join(emojis)}', colour=0xc27c0e, timestamp=now())
        msg = await ctx.send(embed=embed)
        for emoji in emojis:
            await msg.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Simples_Cog(bot))
