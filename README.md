<p align="center">
    <img src="repository/images/icon.png"/>
</p>
<h1 align="center">Xylene v0.0.1</h1>
<h3 align="center">Databasing information from APIs</h3>
<p align="center">
    <img src="https://img.shields.io/apm/l/vim-mode.svg"/>
    <img src="https://img.shields.io/badge/python-3.7.4-green.svg">
    <img src="https://img.shields.io/badge/discord-Xithrius%231318-green.svg">
</p>

<p align="center">
    <a href="#setup">Setup</a> -
    <a href="#commands">Commands</a> -
    <a href="#changelog">Changelog</a>
</p>


## Requestables:
- [ ] Games:
  - [ ] Osu!
  - [ ] Warframe
  - [ ] League of Legends
  - [ ] Destiny 2
  - [ ] Enter the Gungeon
- [ ] Websites:
  - [x] Reddit
  - [x] Weather*
  - [ ] Github
  - [ ] Imgur
  - [ ] Twitter
  - [ ] Open Movie Database (OMDb)

> *currently contains databasing capabilities


## Setup:
### Preface: 
* This bot is currently not meant for anyone to run, as it has specific requirements. The ones listed below are listed to the best of my ability, but they may not be completely complete. 
* I will be setting up a DigitalOcean instance of the bot soon, so as of now, the bot is still in experimental mode, and is __unstable__
* If you want my bot on your server, it can be [invited](https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=1664470208).
* I am a Windows 10 user. If you submit an [issue](https://github.com/Xithrius/Xylene/issues) regarding Linux, I'll do my best to help you, but there are no gaurantees that I will be able to figure out the problem. 
* Cog files have categories in this order: `Background tasks`, `Commands`, and `Events`. Anything that doesn't go into these categories are placed before these and are not labeled.
* Doc strings should always be formatted as such: `short desc`, `Args`, `Raises`, and `Returns`.

### Requirements:
#### [Install python](https://www.python.org/downloads/)
* Python 3.7.3+ must be installed for this bot to run. Which ever one gives a version that is Python 3.7.3 or higher, replace `py`, which I use in the following commands, with the prefix (ex. `python`). 
* To check your current Python version, execute one of these commands in your favorite terminal:

|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `python -V`, `py -V`, or `py -3 -V`  |
|  Linux  |  `python3 -V`  |

#### Install package requirements:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py -m pip install --user -r requirements.txt`  |
|  Linux  | `python3 -m pip install --user -r requirements.txt`  |

### Setting up configuration for supported cogs:
* Create a new file called `config.json` within the directory of `handlers/configuration`.
* Copy the contents of `config.txt` into `config.json`, then conduct the following:

|  Item  |  Instructions  |  Link  |
| ------------- | ------------- | ------------- |
| Discord  |  `New application > bot > add bot > copy token` this token will be given to `discord` in the config. The bot's ID in `General Information` will be used later in [the invite portion](#invite-the-bot), so be sure to keep that in mind. |  [Discord Developer Portal](https://discordapp.com/developers/applications/)  |
| Owners  |  A list of integers that are linked to user IDs. These user IDs can be obtained by right-clicking on a user's profile, and going all the way down to `Copy ID`. If this does not appear, turn on `Developer Mode`, hidden in `Settings > Appearence`  |  None  |
|  Reddit  |  Give `username` and `password` your username and password. `ID` and `secret` are self-explanitory after setting up the personal-use script. Use `http://127.0.0.1:65010/authorize_callback` for the `redirect uri`  |  [Reddit user preferences](https://old.reddit.com/prefs/apps/)  |
|  Weather  | `weather` will be given the API key that you're emailed after signing up for one.  |  [WeatherBit dashbord](https://www.weatherbit.io/account/dashboard)  |
|  Osu!  |  Give `osu` the API key that you'll recieve when registering for a token.  |  [Osu API Registration](https://osu.ppy.sh/p/api/)  |

### Invite the bot:
* Remember the ID that you were given while creating the bot? Well here's where you use it. Take the ID, and replace IDENTIFICATION within the link below. Click on the link when you're done with this process.
* https://discordapp.com/oauth2/authorize?client_id=IDENTIFICATION&scope=bot&permissions=1664470208

### Running the bot:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py bot.py`  |
|  Linux  |  `python3 bot.py`  |


## Commands rules:
* Commands and arguments are always seperated by space
* Output is usually a fancy embed message
* Command prefix: "." or mention
* Command prefix and command are not seperated by anything

## Commands:
<p align="left">
    <a href="#reddit">Reddit</a> -
    <a href="#weather">Weather</a> -
    <a href="#miscellaneous">Miscellaneous</a>
</p>

### Reddit:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  r/search  |  `<query>`  |  Top 5 subreddits that contain this query  |
|  r/preview  |  `<subreddit>`  |  A sneak peak of a subreddit  |
|  r/hot  |  `<subreddit>`  |  See a singular post from what's hot in a subreddit  |
|  r/top  |  `<subreddit>`  |  See a singular post from the top of a subreddit  |

Example: `.r/hot python`

### Weather:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  weather  |  `zip <zip code> <country>`  |  A direct message with weather information  |

Example: `weather zip 12345 US`

### Miscellaneous:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  creator  |  None  |  The creator of the bot  |
|  icon  |  None  |  Gets the icon of the bot  |
|  from_timestamp  |  Datetime integer timestamp  |  Readable date format  |
|  time  |  None  |  Get the current time  |
|  members  |  None  |  Get a list of all members within the server  |
|  rstring  |  Length (defaults to 14)  |  A string of random letters and numbers  |
|  invite  |  None  |  Link to invite the bot to a server  |
|  ping_vc  |  None  |  Pings everyone in the current voice chat that you are in  |
|  user_icon  |  Mention  |  The icon of a user  |
|  emojis  |  None  |  Emojis 0-10  |

### Owner-only:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  tts  |  A string  |  When in a voice chat, the bot will use text to speech to speak through it's own mic  |
|  purge  |  integer (max 100, default 10) |  Deletes the number of messages specified  |
|  exec  |  `"```py"` followed by a python script, then another `"```"` on the last line  |  The output of the python script in the terminal to the owner, and a message to say if the execution was successful to everyone else.  |
|  r  |  None  |  Reload all cog files  |
|  l  |  Cog path seperated by "."  |  Load the specific cog  |
|  u  |  Cog path seperated by "."  |  unload the specific cog  |
|  exit  |  None  |  Makes the bot go offline, unloading all cogs, disconnecting from all databases, and cancelling all background tasks.  |

Example: `.l cogs.directives.simples`

## Changelog:

### v0.0.1:
#### Main changes:
* All other bots that I own have been either deleted completely from existance or parts have been removed from them and were put into this one.
#### Modifications:
* Everything, literally.
