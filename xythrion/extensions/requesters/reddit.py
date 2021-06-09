from datetime import datetime as dt
from typing import Optional

from discord.ext.commands import Cog, group
import pandas as pd

from xythrion import Context, Xythrion
from xythrion.utils import graph_2d

BASE_URL = "https://www.reddit.com/r/{}/top/.json?t={}&limit={}"
TIME_FORMAT = "%b %m %H:%M"


class Reddit(Cog):
    """Gives information about posts from Reddit."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    async def get_reddit_information(self, *args, key: str = None) -> pd.DataFrame:
        """Parses only the needed data for graphing."""
        data = await self.bot.request(BASE_URL.format(*args))

        df = pd.DataFrame(
            [[p["created"], p[key]] for p in [d["data"] for d in data["data"]["children"]]],
            columns=("date", key)
        ).sort_values(by="date")

        df["date"] = df["date"].transform(
            lambda epoch: dt.strftime(dt.fromtimestamp(epoch), TIME_FORMAT)
        )

        if not df:
            raise ValueError("Cannot generate graph with no data.")

        return df

    @group()
    async def reddit(self, ctx: Context) -> None:
        """The group command for Reddit information."""
        await ctx.check_for_subcommands()

    @reddit.command(aliases=("ups",))
    async def upvotes(self, ctx: Context, subreddit: str, timeframe: str, limit: Optional[int] = 10) -> None:
        """Gives a graph of upvotes over time."""
        df = await self.get_reddit_information(subreddit, timeframe, limit, key="ups")

        buffer = await graph_2d(*df.T.values, graph_type="bar")

        await ctx.embed(desc="Graph of upvotes", buffer=buffer)
