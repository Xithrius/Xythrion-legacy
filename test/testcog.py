class DeveloperCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def dm(ctx, user: discord.Member, *, message):
        if self.ctx.author.id == 257233913951289344:
            await self.user.send(f'{message}\n*This is a bot DM sent by* `{ctx.author.mention}`*, and replies cannot be read!*')
        else:
            await self.ctx.send("You can't do this!")

    @commands.command()
    async def activity(ctx, arg1, *, arg2):
        if self.ctx.author.id == 257233913951289344:
            if arg1 == 'playing':
                await self.bot.change_presence(activity=discord.Game(name=arg2))
                print(f"{ctx.message.author} changed bot presence to 'Playing {arg2}'")
            elif arg1 == 'listening':
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=arg2))
                print(f"{ctx.message.author} changed bot presence to 'Listening to {arg2}'")
            elif arg1 == 'watching':
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=arg2))
                print(f"{ctx.message.author} changed bot presence to 'Watching {arg2}'")
        else:
            await ctx.send("You can't do this!")

    @commands.command()
    async def shutdown(ctx):
        if self.ctx.author.id == 257233913951289344:
            await self.bot.change_presence(activity=discord.Game(name='Shutting down bot!'))
            await self.ctx.send(f'Goodbye ;-;')
            sys.exit()


def setup(bot):
    bot.add_cog(DeveloperCog(bot))
