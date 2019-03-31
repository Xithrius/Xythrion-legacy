'''

MIT License

Copyright (c) 2019 Xithrius

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


# ///////////////////////////////////////////////////////// #
# authorship information
# ////////////////////////
# Description of the author(s) information
# ///////////////////////////////////////////////////////// #


__author__ = 'Xithrius'

__copyright__ = 'MIT License, Copyright (c) 2019 Xithrius'

__credits__ = ["Xithrius", "Rapptz"]
# Xithrius : Project owner
# Rapptz   : Discord.py API wrapper creator

__license__ = "MIT"

__version__ = "0.00.0009"

__maintainer__ = "Xithrius"

__status__ = "Development"


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import random
import string
import datetime
import uuid
import hashlib

import discord
from discord.ext import commands as comms

# from essentials.pathing import path, mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


class PasswordCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

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
