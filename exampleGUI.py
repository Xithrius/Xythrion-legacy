'''
+
|  > Snipped.py
|  > Copyright (c) 2019 Xithrius
|  > MIT license, Refer to LICENSE for more info
+
'''


import tkinter as tk
import traceback
import json
import os
import sys

import discord
from discord.ext import commands as comms

from snipped.containers.QOL.pathing import path
from snipped.containers.output.printer import duplicate, printc
import snipped


'''
class Navbar(tk.Frame): ...
class Toolbar(tk.Frame): ...
class Statusbar(tk.Frame): ...
class Main(tk.Frame): ...
'''



class MainApplication(tk.Frame, comms.Cog):
    def __init__(self, master):
        tk.Frame.__init__(master)
        comms.Cog.__init__()
        # self.statusbar = Statusbar(self, ...)
        # self.toolbar = Toolbar(self, ...)
        # self.navbar = Navbar(self, ...)
        # self.main = Main(self, ...)

        # self.statusbar.pack(side="bottom", fill="x")
        # self.toolbar.pack(side="top", fill="x")
        # self.navbar.pack(side="left", fill="y")
        # self.main.pack(side="right", fill="both", expand=True)

        self.bot = comms.Bot(command_prefix='$', case_insensitive=False)
        self.cogs = cogs
        self.all_cogs = self.cogs
        self.presence = 'with reality'
        self.load_cog_task = self.bot.loop.create_task(self.load_cogs_in())

        """
        Passing objects into the MainCog, then running the bot
        """
        # Searching for cogs within the cogs directory
        self.cogs = []
        for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
            cog = '.'.join(str(y) for y in dirpath[len(path()):].split('\\'))
            if '__pycache__' not in cog:
                self.cogs.extend([f'{cog}.{i[:-3]}' for i in filenames if i[:-3] not in [x[:-1] for x in open(path('JAiRU', 'configuration', 'blocked_cogs.txt'), 'r').readlines()]])
        bot.add_cog(MainApplication(bot, cogs))
        # Looping the input until token is correct
        checkToken = True
        while checkToken:
            try:
                token = json.load(open(path('JAiRU', 'configuration', 'config.json')))['discord']
                bot.run(token, bot=True, reconnect=True)
                checkToken = False
            except FileNotFoundError:
                print('WARNING: TOKEN FILE NOT FOUND')
                checkToken = False
            except discord.errors.LoginFailure:
                print('WARNING: INCORRECT DISCORD TOKEN')
                checkToken = False


if __name__ == "__main__":
    MainApplication(tk.Tk()).mainloop()
