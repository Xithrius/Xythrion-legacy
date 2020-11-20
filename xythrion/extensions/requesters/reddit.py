from random import randint

from discord import Embed, Message
from discord.ext.commands import CheckFailure, Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, http_get, markdown_link, shorten


class Reddit(Cog):
    """The Reddit cog that sends Reddit information in the form of an embed."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Scans for Reddit posts and provides info on them."""
        if "https://www.reddit.com/r/" in message.content:
            url = f'{message.content.rsplit("/", maxsplit=1)[0]}.json'
            async with self.bot.http_session.get(url) as resp:
                assert resp.status == 200
                _json = await resp.json()
                _json = _json[0]["data"]["children"][0]["data"]

            if _json["over_18"] and not message.channel.is_nsfw():
                return

            d = {
                "Title": _json["title"],
                "Subreddit": markdown_link(
                    _json["subreddit"], f'https://www.reddit.com/r/{_json["subreddit"]}'
                ),
                "Upvotes": _json["ups"],
                "Upvotes/downvotes": f'{_json["upvote_ratio"] * 100}%',
                "Image url": markdown_link("Link", _json["url"]),
            }
            formatted = "\n".join(f"**{k}**: {v}" for k, v in d.items())
            embed = DefaultEmbed(self.bot, description=formatted)

            await message.channel.send(embed=embed)

    @command(aliases=["sub", "subreddit"])
    async def reddit(self, ctx: Context, subreddit: str, status: str = "hot", timeframe: str = "day") -> None:
        """Requesting from the Reddit service to give a random post from a status within a timeframe."""
        status, timeframe = status.lower(), timeframe.lower()
        statuses = ["top", "hot", "controversial", "new", "gilded"]
        timeframes = ["hour", "day", "week", "month", "year", "all"]

        if status not in statuses:
            await ctx.send(f'Please pick a status within `{", ".join(str(y) for y in statuses)}`')

        if timeframe not in timeframes:
            await ctx.send(f'Please pick a timeframe within `{", ".join(str(y) for y in timeframes)}`')

        url = f"https://reddit.com/r/{subreddit}/{status}.json?limit=100&t={timeframe}"

        _json = await http_get(ctx, url)

        _json = _json["data"]["children"]
        p = _json[randint(0, len(_json) - 1)]["data"]

        fail = False

        try:
            if p["over_18"] and not ctx.message.channel.is_nsfw():
                fail = True

        except AttributeError:
            fail = True

        if fail:
            raise CheckFailure(message="NSFW")

        image = False

        if p["url"][-4:] in (".jpg", "jpeg", ".png"):
            image = p["url"]

        desc = f'[`{shorten(p["title"])}`](https://reddit.com{p["permalink"]})'
        embed = Embed(title=f"*r/{subreddit}*", description=desc)

        embed.set_footer(text=f'Upvotes: {p["ups"]}\nAuthor: u/{p["author"]}')
        embed.set_image(url=image if image else "")

        await ctx.send(embed=embed)
