<p align="center">
    <img src="/images/icon.jpg"/>
</p>
<h1 align="center">Xythrion v2.0</h1>
<h3 align="center">Graphing manipulated data through discord.py</h3>
<p align="center">
    <img src="https://img.shields.io/apm/l/vim-mode.svg"/>
    <img src="https://img.shields.io/badge/python-3.7.4-green.svg">
</p>
<p align="center">
    <a href="https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=335400150">Invite</a> -
    <a href="#commands">Commands</a> -
    <a href="#setup">Setup</a>
    <a href="#changelog">Changelog</a>
</p>


## Checklist:
- [ ] Extensions:
    - [ ] Administration:
        - [x] API_usage
        - [x] Development
        - [x] Warnings
        - [ ] Source
        - [ ] Documentation/help
    - [ ] Generation:
        - [x] Graphing
        - [ ] Math
        - [x] QRCodes
        - [x] Randoms
        - [ ] Images
    - [ ] Meta:
        - [x] Dates
        - [x] Guilds
        - [ ] Links
    - [ ] Requesters
        - [x] Reddit
        - [ ] Weather
        - [ ] Youtube


## Setup:
*NOTES*:
> - The following steps below assume that you have Python 3.8.x installed.
> - They also assume you know what to replace `python3` with on your OS, such as if on Windows, replacing `python3` with `py -3.8`, `python`, or `py`.
> - Alternatives #1 and #2 assume that you've inserted your credentials into the `.env` file that you have to create manually for the environment variables. You can copy the contents of the `.env-example` file into the `.env` and configure to your liking.
> - DO NOT UPGRADE `pip` YOU'RE RUNNING THIS ON UBUNTU.

#### Creating the virtual environment and running the bot (3 ways):

1. virtualenv/venv:
```sh
$ python3 -m pip install --U pip virtualenv
$ python3 -m virtualenv venv
$ source venv/Scripts/activate
$ python3 -m xythrion
```

2. pipenv:
```sh
$ python3 -m pip install --U pip pipenv
$ pipenv install --dev
$ pipenv shell
$ pipenv start run
```

3. Docker:
```sh
$ docker pull postgres
# "placeholder" in this command should replace the placeholder with the same name in the .env file.
$ docker run --name postgres -e POSTGRES_PASSWORD=placeholder -d postgres
$ docker-compose up --build
```

## Changelog

### [v2.0](!https://github.com/Xithrius/Xythrion/releases/tag/v2.0)
#### Added:
- Motivation to actually do this project.
- Documentation that's actually useful.
- Tables instead of weird broken graphs, and replaced the void with more graphs.
-

#### Changed:
- Importing from `modules/`.
- The way embeds are formatted.
- Configuration of the bot, and the different options at launch.
- Everything to dark mode so your eyes don't get burned by the light.

#### Removed:
- No longer recording specific messages and their content sent by users, only adding it to the count of messages/commands.
- Enter The Gungeon wiki and imgur cogs. These might be added again in the future.
- The youtube to mp3 command since it's against YouTube's TOS.
- Embed tables that no one liked.
- The TTS command (I really wonder why I implemented it in the first place).
- The fancy status, since it has been moved to its own package: [hyper-status](!https://pypi.org/project/hyper-status/).

### v0-v1.1 (Development of the project, I wouldn't look too close at these versions)
- API tracking such as how weather changes within an area, and how a certain Reddit post is doing over a couple days.
- Added the ability to graph math equations.
- Building sourcing cogs. This will be moved to my other bot, [Demoness](!https://www.github.com/Xithrius/Demoness).
- Bot now uses asyncpg (asynchronous Postgresql) to access databases.
- `bot.py` now subclasses `comms.Bot`, while Main_Cog gets `comms.Cog`.
- The extensions `etg.py` and `imgur.py` have been brought back from the dead.
- Parser and shortcut functions have now been removed from the subclass of `bot.py` and moved to their own place in `modules/`.
- The setup within this README has been given extra files for token generation.
- Permission loading and service checks are now automated before bot is available for use.
- First real stable version with no major flaws (I haven't found any within testing yet).
