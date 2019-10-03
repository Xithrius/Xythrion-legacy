<p align="center">
    <img src="/images/icon.png"/>
</p>

<h1 align="center">Xythrion v1.2</h1>

<h3 align="center">Databasing information from APIs</h3>

<p align="center">
    <img src="https://img.shields.io/apm/l/vim-mode.svg"/>
    <img src="https://img.shields.io/badge/python-3.7.4-green.svg">
    <img src="https://img.shields.io/badge/discord-Xithrius%231318-green.svg">
</p>

<p align="center">
    <a href="https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=335400150">Invite</a> -
    <a href="#setup">Setup</a> -
    <a href="#commands">Commands</a> -
    <a href="#changelog">Changelog</a>
</p>


## Requestables:
- [x] Reddit
- [x] Weather
- [ ] Imgur
- [ ] Github
- [ ] Twitter
- [ ] Open Movie Database (OMDb)


## Setup:
### Preface: 
* Digital Ocean or AWS will be running this bot in the future, so there should be no need to create your own instance of the bot unless you're testing it. You can invite the bot [here](https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=335400150)
* If you want to test the bot, the instructions below will guide your way.

#### Getting packages:
* Run the command `py -3 -m pip install --user -r requirements.txt` to install packages that are required to run the bot.
* Go to the [PortgreSQL](https://www.postgresql.org/) website, and install the latest version. 
    * When selecting components, just select all of them.
    * `WARNING`: If you decide to use a different locale, it will be up to you to find out what the host is, which will most likely not be `localhost` or `127.0.0.1`.
    * After setup, open the pgadmin application. You will be able to create a password for the databse. This will be the password that you will use in `config.json`.
* After setting up these items.


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


## Changelog:

### v1.2
* Bot now uses asyncpg (asynchronous PortgreSQL) to access the database without having to hold everything up after a command is ran. This is what sqlite3 would do, since it is synchronous. 

### v1.1:
* Reddit command is finally stable, with some changes to how commands interact with users

### v1.0:
* Permission loading and service checks are now automated before bot is available for use.
* First real stable version with no major flaws (I haven't found any within testing yet).
