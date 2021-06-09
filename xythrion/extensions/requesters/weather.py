from discord.ext.commands import Cog, group

from xythrion import Context, Xythrion
from xythrion.constants import WeatherAPIs

EARTH_URL = "https://api.openweathermap.org/data/2.5/forecast?zip={0},{1}&appid={2}"
MARS_URL = f"https://api.nasa.gov/insight_weather/?api_key={WeatherAPIs.MARS}&feedtype=json&ver=1.0"


class Weather(Cog):
    """Weather for different planets."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    async def weather(self, ctx: Context) -> None:
        """Getting Weather for different planets."""
        await ctx.check_for_subcommands()

    @weather.command()
    async def earth(self, ctx: Context, zip_code: str, country_code: str = "US") -> None:
        """Getting weather for the planet of Earth."""
        ...

    @weather.command()
    async def mars(self, ctx: Context) -> None:
        """Getting weather for the planet of Mars."""
        ...
