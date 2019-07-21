<img align="middle" src="repository/images/icon.png">


# 1Xq4417 v0.0.1
Requesting information from the internet's REST APIs.


[![License](https://img.shields.io/apm/l/vim-mode.svg)](https://img.shields.io/apm/l/vim-mode.svg) [![Python Version](https://img.shields.io/badge/python-3.7.3-green.svg)](https://www.python.org/downloads/release/python-373/) [![discord](https://img.shields.io/badge/discord-Xithrius%231318-green.svg)](https://img.shields.io/badge/discord-Xithrius%231318-green.svg)


# Setup:

### Installing requirements:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py -3 -m pip install -r requirements.txt`  |
|  Linux  | `python3 -m pip install -r requirements.txt`  |

### Setting up configuration:
* Copy the contents of `template_config.json` into a file named `config.json` in the same directory, then replace "Discord token" with your bot token that you get from [Here](https://discordapp.com/developers/applications/), after you create your bot.

### Invite the bot:
* After inviting the bot to your server with [this link](https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=1664470208), run the following command, depending on your operating system:

### Running the bot:
|  Operating system  |  Command  |
| ------------- | ------------- |
|  Windows  |  `py -3 bot.py`  |
|  Linux  |  `python3 bot.py`  |

---

# Commands:
* Commands and arguments are always seperated by space
* Output is usually a fancy embed message
* Command prefix: `.` (goes before all commands, no space)

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

[Image examples of all commands](https://github.com/Xithrius/1Xq4417/blob/master/documentation)
---

# Changelog: 

## v1.0:
*

## The rest of the changelog is [here](https://github.com/Xithrius/1Xq4417/blob/master/CHANGELOG.md)
