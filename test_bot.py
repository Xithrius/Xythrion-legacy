'''
class Navbar(tk.Frame): ...
class Toolbar(tk.Frame): ...
class Statusbar(tk.Frame): ...
class Main(tk.Frame): ...
'''


import tkinter as tk
from discord.ext import commands as comms

from containers.output.printer import printc


class MainCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'NTYwNjIyMTM0NTY5NzMwMDUx.XMFaMQ.G-MOf6Uqbtsjir8C8JT3t-WOd84'
        self.bot.add_cog(MainCog(bot))
        self.bot.run(self.token, bot=True, reconnect=True)

    async def logout(self):
        """
        Make the bot logout
        """
        printc(f'WARNING: LOGGING OUT...')
        await bot.logout()


class MainApplication(tk.Frame, MainCog):
    def __init__(self, bot, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        MainCog.__init__(self, bot)
        # self.statusbar = Statusbar(self, ...)
        # self.toolbar = Toolbar(self, ...)
        # self.navbar = Navbar(self, ...)
        # self.main = Main(self, ...)

        # self.statusbar.pack(side="bottom", fill="x")
        # self.toolbar.pack(side="top", fill="x")
        # self.navbar.pack(side="left", fill="y")
        # self.main.pack(side="right", fill="both", expand=True)

        self.master.title('yes')
        tk.Button(self.master, text='reload', command=self.logout).grid()


if __name__ == "__main__":
    root = tk.Tk()
    bot = comms.Bot(command_prefix='$', case_insensitive=True)
    MainApplication(root, bot)
    root.mainloop()
