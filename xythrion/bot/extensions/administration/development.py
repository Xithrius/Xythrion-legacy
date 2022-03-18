from disnake.ext.commands import Cog, ExtensionNotLoaded, command, is_owner
from loguru import logger as log

from bot import Context, Xythrion
from bot.extensions import EXTENSIONS


class Development(Cog, command_attrs=dict(hidden=True)):
    """Cog required for development of this bot."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(name="reload", aliases=("refresh", "r"))
    @is_owner()
    async def reload(self, ctx: Context) -> None:
        """Reloads all extensions."""
        for extension in EXTENSIONS:
            try:
                self.bot.reload_extension(extension)
            except ExtensionNotLoaded:
                self.bot.load_extension(extension)
            except Exception as e:
                return log.error(f"Failed reloading {extension}.", exc_info=(type(e), e, e.__traceback__))

        msg = f"Reloaded {len(EXTENSIONS)} extension(s)."

        log.info(msg)

        await ctx.embed(desc=msg)

    @command(name="ping", aliases=("ping_bot", "p",))
    @is_owner()
    async def ping_bot(self, ctx: Context) -> None:
        """Responds to a user with 'Pong!' to check the response time"""
        await ctx.send(":ping_pong: Pong!")

    @command(aliases=("ping_web", "pw"))
    @is_owner()
    async def ping_webserver(self, ctx: Context) -> None:
        """Pings the webserver to see if it's online and functioning"""
        async with self.bot.http_session.get(f"{self.bot.webserver_url}/ping") as response:
            if response.status == 200:
                await ctx.send(f":ping_pong: Pong! Status: {response.status}")
            else:
                await ctx.send(f"Ping failed with status code {response.status}")
