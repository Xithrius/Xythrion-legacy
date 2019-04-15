'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries
# /////////////////////////////////////////////////////////
# Built-in modules, third-party modules, custom modules
# //////////////////////////////////////////////////////////////////////////// #


import uuid
import hashlib
import random
import string
import datetime

from discord.ext import commands as comms
import discord


# //////////////////////////////////////////////////////////////////////////// #
# Passwords cog
# /////////////////////////////////////////////////////////
# Keeping passwords safe
# //////////////////////////////////////////////////////////////////////////// #


class PasswordCog(comms.Cog):

    # //////////////////////// # Object(s): bot
    def __init__(self, bot):
        self.bot = bot

# //////////////////////////////////////////////// # Commands
    # //////////////////////// # Hash a password
    @comms.command()
    async def passwords(self, ctx):

        def hash_password(password):
            # uuid is used to generate a random number
            salt = uuid.uuid4().hex
            return hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ':' + salt

        def check_password(hashed_password, user_password):
            password, salt = hashed_password.split(':')
            return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()

        new_pass = input('Please enter a password: ')
        hashed_password = hash_password(new_pass)
        print('The string to store in the db is: ' + hashed_password)
        old_pass = input('Now please enter the password again to check: ')
        if check_password(hashed_password, old_pass):
            print('You entered the right password')
        else:
            print('I am sorry but the password does not match')

    # //////////////////////// # Give a random password of inputted length
    @comms.command()
    async def random_password(self, ctx, length=10, personal='true'):
        """ Random password of default length 10. '$random_password <length>'"""
        if length > 0:
            password = ''.join(str(y) for y in [random.choice(string.ascii_letters + string.digits) for i in range(length)])
            embed = discord.Embed(title='[ Random Password Generator ]', timestamp=datetime.datetime.now() + datetime.timedelta(hours=8), colour=0xc27c0e)
            embed.add_field(name=f'Password of length {length}:', value=password, inline=False)
            if personal == 'true':
                await ctx.author.send(embed=embed, delete_after=30)
            else:
                await ctx.send(embed=embed, delete_after=180)
        else:
            if personal == 'true':
                await ctx.author.send(f'{length} is an invalid parameter.')
            else:
                await ctx.send(f'{length} is an invalid parameter')


def setup(bot):
    bot.add_cog(PasswordCog(bot))
