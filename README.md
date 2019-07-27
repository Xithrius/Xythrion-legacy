<p align="center">
    <img src="repository/images/icon.png"/>
</p>
<h1 align="center">1Xq4417 v0.0.1</h1>
<h3 align="center">Databasing information from APIs</h3>
<p align="center">
    <img src="https://img.shields.io/apm/l/vim-mode.svg"/>
    <img src="https://img.shields.io/badge/python-3.7.3-green.svg">
    <img src="https://img.shields.io/badge/discord-Xithrius%231318-green.svg">
</p>


|  [Components](#components)  |  [Setup](#setup)  |  [Commands](#commands)  |  [Changelog](#changelog)  |
| ------------- | ------------- | ------------- | ------------- |


<h5 align="center">[Components](#components)</h5>


## Components
* I'll do this when v1.0 is released.


## Setup:

### Installing requirements:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py -3 -m pip install -r requirements.txt`  |
|  Linux  | `python3 -m pip install -r requirements.txt`  |

If running the bot gives errors, run the following commands in a console:
* `pip install --upgrade --user google-cloud-texttospeech`,
* `pip install discord.py[voice]`,
* `pip install datetime`

### Setting up configuration:
* Copy the contents of `template_config.json` into a file named `config.json` in the same directory, then replace "Discord token" with your bot token that you get from [Here](https://discordapp.com/developers/applications/), after you create your bot.

### Invite the bot:
* After inviting the bot to your server with [this link](https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=1664470208), run the following command, depending on your operating system:

### Running the bot:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py -3 bot.py`  |
|  Linux  |  `python3 bot.py`  |


## Commands:
* Commands and arguments are always seperated by space
* Output is usually a fancy embed message
* Command prefix: `.` (goes before all commands, no space)
- [Reddit](#reddit)
- [Weather](#weather)

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
