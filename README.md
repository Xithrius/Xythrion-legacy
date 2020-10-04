<p align="center">
    <img src="/images/icon.jpg"/>
</p>
<h1 align="center">Xythrion v2.0</h1>
<h3 align="center">Graphing manipulated data through discord.py</h3>
<p align="center">
    <a href="https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=335400150">Invite</a> -
    <a href="#checklist">Checklist</a> -
    <a href="#commands">Commands</a> -
    <a href="#setup">Setup</a> -
    <a href="#changelog">Changelog</a>
</p>


# Setup:
*NOTE*:
- This guide assumes you've copied the template from `.env-example` to a file called `.env` that you've created yourself.

```sh
$ docker pull postgres
# "placeholder" in this command should replace the placeholder with the same name in the .env file.
$ docker run --name postgres -e POSTGRES_PASSWORD=placeholder -d postgres
$ docker-compose up --build
```

# Changelog

## [v2.0](!https://github.com/Xithrius/Xythrion/releases/tag/v2.0)
### Added:
- Motivation to actually do this project.
- Documentation that's actually useful.
- Graphing now works with single variable expressions (ex. only x or y, not both.), except factorials aren't available.
- Docker is now used for the use of environment variables.

### Changed:
- Renamed `modules/` to `utils/`.
- Embeds now have default values and are sometimes modified after initialization.
- Graphs have been changed to dark mode so your eyes aren't burned out by the sun that is the graph image.
- No longer using `.json` files for storing credentials, a singular `.env` file is now used.

### Removed:
- Too many things were removed, so I ended up losing track.
- All the useless stuff from previous versions. This is a graphing/utility bot, not a music bot.
- One thing that I can remember getting removed are the `imgur` and `etg` cogs, because they served no use.

## [v1.0](!https://github.com/Xithrius/Xythrion/releases/tag/v1.0)
- API tracking such as how weather changes within an area, and how a certain Reddit post is doing over a couple days.
- Bot now uses asyncpg (asynchronous Postgresql) for databasing.
- `bot.py` now subclasses `comms.Bot`, while Main_Cog gets `comms.Cog`.
- The extensions `etg.py` and `imgur.py` have been brought back from the dead.
- Parser and shortcut functions have now been removed from the subclass of `bot.py` and moved to their own place in `modules/`.
- Permission loading and service checks are now automated before bot is available for use.
