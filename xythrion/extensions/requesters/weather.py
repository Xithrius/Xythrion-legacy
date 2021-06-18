from datetime import datetime, timedelta
import re

from discord.ext.commands import Cog, group
import pandas as pd

from xythrion import Context, Xythrion
from xythrion.utils import and_join, epoch_to_datetime, graph_2d
from xythrion.constants import WeatherAPIs

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?zip={},{}&units={}&appid={}"

ZIP_CODE_MATCH = re.compile(r"^\d{5}$")
ALLOWED_UNITS = {"standard": "K", "metric": "C", "imperial": "F"}


class Weather(Cog):
    """Weather for Earth."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    async def format_and_request(self, url: str, *url_format) -> dict:
        """Takes a url, formats the url, then requests from said url."""
        return await self.bot.request(url.format(*url_format, WeatherAPIs.EARTH))

    @group()
    async def weather(self, ctx: Context) -> None:
        """Group command for the weather."""
        await ctx.check_for_subcommands()

    @weather.command()
    async def week(
        self,
        ctx: Context,
        zip_code: str,
        units: str = "metric",
        country_code: str = "US"
    ) -> None:
        """Getting weather for the past week from a zip code."""
        if not re.search(ZIP_CODE_MATCH, zip_code):
            return await ctx.embed(desc=f"Illegal zip code '{zip_code}'. Only integers are allowed.")
        elif units not in ALLOWED_UNITS:
            return await ctx.embed(
                desc=f"Illegal unit '{units}'. Allowed units: {and_join(ALLOWED_UNITS.keys())}."
            )

        data = await self.format_and_request(BASE_URL, zip_code, country_code, units)

        city = data["city"]["name"]

        week_from_now = datetime.timestamp(datetime.now() + timedelta(days=7))

        df = pd.DataFrame(
            [[day["dt"], day["main"]["temp"]] for day in data["list"] if day["dt"] <= week_from_now],
            columns=("date", "day_temp")
        )

        df["date"] = df["date"].transform(lambda epoch: epoch_to_datetime(epoch))

        buffer = await graph_2d(
            *df.T.values,
            x_title="Dates",
            y_title=f"°{ALLOWED_UNITS[units]}",
            title=f"Weather from {df['date'][0]} to {df['date'][-1]}",
            graph_type="bar",
            grid=False
        )

        await ctx.embed(
            desc=f"Weather throughout the past week in {city}",
            buffer=buffer
        )
