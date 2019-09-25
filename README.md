<p align="center">
    <img src="images/icon.png"/>
</p>
<h1 align="center">Xythrion v1.2</h1>
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

### v1.0:
* Permission loading and service checks are now automated before bot is available for use.
* First real stable version with no major flaws (I haven't found any within testing yet).
