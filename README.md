<p align="center">
    <img src="repository/images/icon.png"/>
</p>
<h1 align="center">Xythrion v0.0.1</h1>
<h3 align="center">Databasing information from APIs</h3>
<p align="center">
    <img src="https://img.shields.io/apm/l/vim-mode.svg"/>
    <img src="https://img.shields.io/badge/python-3.7.4-green.svg">
    <img src="https://img.shields.io/badge/discord-Xithrius%231318-green.svg">
</p>

<p align="center">
    <a href="https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=53992512">Invite</a> -
    <a href="#setup">Setup</a> -
    <a href="#commands">Commands</a> -
    <a href="#changelog">Changelog</a>
</p>


## Requestables:
- [x] Reddit
- [x] Weather*
- [ ] Imgur
- [ ] Github
- [ ] Twitter
- [ ] Open Movie Database (OMDb)

> *currently contains databasing capabilities


## Setup:
### Preface: 
* Digital Ocean or AWS will be running this bot in the future, so there should be no need to create your own instance of the bot unless you're testing it. If you happen not to be testing it, you can invite the bot [here](https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=53992512)
* If you want to test the bot, the instructions below will guide your way.

### Requirements:
#### [Install python](https://www.python.org/downloads/)
* Python 3.7.x must be installed for this bot to run.

#### Install package requirements:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py -3 -m pip install --user -r requirements.txt`  |
|  Linux  | `python3 -m pip install --user -r requirements.txt`  |

### Services that require tokens:

|  Item  |  Instructions  |  Link  |
| ------------- | ------------- | ------------- |
| Discord  |  `New application > bot > add bot > copy token` this token will be given to `discord` in the config. The bot's ID in `General Information` will be used later in [the invite portion](#invite-the-bot), so be sure to keep that in mind. |  [Discord Developer Portal](https://discordapp.com/developers/applications/)  |
|  Weather  | `weather` will be given the API key that you're emailed after signing up for one.  |  [WeatherBit dashbord](https://www.weatherbit.io/account/dashboard)  |
|  TTS  |  This will be included later, but a VERY long amount of instructions are needed. A different README will be supplied at a later date  |  Something something Google Cloud Text-To-Speech API  |

### Running the bot:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py -3 bot.py`  |
|  Linux  |  `python3 bot.py`  |


## Commands:

### Reddit:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  hot  |  `<subreddit>`  |  See a singular post from what's hot in a subreddit  |
|  top  |  `<subreddit>`  |  See a singular post from the top of a subreddit  |

Example: `.reddit hot python`

### Weather:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  daily  |  `<zip code> <amount> <country (default US)>`  |  A graph with high and low temperatures for today and the next amount of days  |
|  init  |  `<zip code> <country (default US)>`  |  Records weather information in a database once a day, forever.  |

Example: `weather zip 12345 US`

### Owner-only: (only allowed for users with IDs in config.json 'owners')
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  tts  |  A string  |  When in a voice chat, the bot will use text to speech to speak through it's own mic  |
|  r  |  None  |  Reload all cog files  |
|  exit  |  None  |  Makes the bot go offline, unloading all cogs, disconnecting from all databases, and cancelling all background tasks.  |

Example: `.tts Bagles with cream cheese`


## Changelog:

### v0.0.1:
* Permission loading and service checks are now automated before bot is available for use.
* First real stable version with no major flaws (I haven't found any within testing yet).
