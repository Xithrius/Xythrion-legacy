    @comms.command()
    async def news(self, ctx):
        embed = discord.Embed(title='News Role', description='To get News role press on ✅ reaction', color=0x00ffff)
        thing = await ctx.send(embed=embed)
        await thing.add_reaction(emoji="✅")

    async def on_raw_reaction_add(self, ctx, reaction, user):
        embed = discord.Embed(title='News Role', description='The bot added role News', color=0x00ffff)
        await ctx.send(embed=embed)
