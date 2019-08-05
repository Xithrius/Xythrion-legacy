<p align="center">
    <img src="repository/images/icon.png"/>
</p>
<h1 align="center">1Xq4417 v0.0.1</h1>
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
  - [x] Weather
  - [ ] Github
  - [ ] Imgur
  - [ ] Twitter
  - [ ] Open Movie Database (OMDb)


## Setup:
### Preface: 
* This bot is currently not meant for anyone to run, as it has specific requirements. The ones listed below are the best I could do, but they may not be completely complete. If you want my bot on your server, it can be [invited](https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=1664470208).
* I am a Windows 10 user. If you submit an [issue](https://github.com/Demonically/1Xq4417/issues) I'll do my best to help you, but there are no gaurantees that I will be able to figure out the problem. 

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

### Setting up configuration:
* Create a new file called `config.json` within the directory of `handlers/configuration`.
* Copy the contents of `config.txt` into `config.json`, then conduct the following:

|  Item  |  Instructions  |  Link  |
| ------------- | ------------- | ------------- |
| Discord  |  `New application > bot > add bot > copy token` this token will be given to `discord` in the config. The bot's ID in `General Information` will be used later in [the invite portion](#invite-the-bot), so be sure to keep that in mind. |  [Discord Developer Portal](https://discordapp.com/developers/applications/)  |
| Owners  |  A list of integers that are linked to user IDs. These user IDs can be obtained by right-clicking on a user's profile, and going all the way down to `Copy ID`. If this does not appear, turn on `Developer Mode`, hidden in `Settings > Appearence`  |  None  |
|  Reddit  |  Give `username` and `password` your username and password. `ID` and `secret` are self-explanitory after setting up the personal-use script. Use `http://127.0.0.1:65010/authorize_callback` for the `redirect uri`  |  [Reddit user preferences](https://old.reddit.com/prefs/apps/)  |
|  Weather  | `weather` will be given the API key that you're emailed after signing up for one.  |  [WeatherBit dashbord](https://www.weatherbit.io/account/dashboard)  |

#### Reference for what to replace items with:
```JSON
{
    "discord": "",
    "owners": [],
    "services": {
        "reddit": {
            "username": "",
            "password": "",
            "ID": "",
            "secret": ""
        },
        "weather": ""
    },
    "There should be no need to modify": "anything below this line in config.json"
}
```

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
</p>

### Reddit:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  r/search  |  `<query>`  |  Top 5 subreddits that contain this query  |
|  r/preview  |  `<subreddit>`  |  A sneak peak of a subreddit  |
|  r/hot  |  `<subreddit>`  |  See a singular post from what's hot in a subreddit  |
|  r/top  |  `<subreddit>`  |  See a singular post from the top of a subreddit  |

### Weather:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  weather  |  `zip <zip code> <country>`  |  A direct message with weather information  |


## Changelog:

### v0.0.1:
#### Main changes:
* All other bots that I own have been either deleted completely from existance or parts have been removed from them and were put into this one.
#### Modifications:
* Everything, literally.
