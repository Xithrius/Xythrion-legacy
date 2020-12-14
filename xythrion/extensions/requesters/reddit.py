from discord import Message
from discord.ext.commands import Cog

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, markdown_link


class Reddit(Cog):
    """Gives information about posts from Reddit."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Scans for Reddit posts and provides information on them."""
        if "https://www.reddit.com/r/" in message.content:
            url = f'{message.content.rsplit("/", maxsplit=1)[0]}.json'
            async with self.bot.http_session.get(url) as resp:
                assert resp.status == 200
                d = await resp.json()
                d = d[0]["data"]["children"][0]["data"]

            if d["over_18"] and not message.channel.is_nsfw():
                return

            d = {
                "Title": d["title"],
                "Subreddit": markdown_link(d["subreddit"], f'https://www.reddit.com/r/{d["subreddit"]}'),
                "Upvotes": d["ups"],
                "Upvotes/downvotes": f'{d["upvote_ratio"] * 100}%',
                "Image url": markdown_link("Link", d["url"]),
            }
            formatted = "\n".join(f"**{k}**: {v}" for k, v in d.items())
            embed = DefaultEmbed(self.bot, description=formatted)

            await message.channel.send(embed=embed)
