<p align="center">
    <img src="/images/icon.png"/>
</p>

<h1 align="center">Xythrion v1.1</h1>

<h3 align="center">Databasing information from APIs</h3>

<p align="center">
    <img src="https://img.shields.io/apm/l/vim-mode.svg"/>
    <img src="https://img.shields.io/badge/python-3.7.4-green.svg">
</p>

<p align="center">
    <a href="https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=335400150">Invite</a> -
    <a href="#setup">Setup</a> -
    <a href="#commands">Commands</a> -
    <a href="#changelog">Changelog</a>
</p>


## Setup:
### Preface: 
* AWS will be running this bot in the future, so there should be no need to create your own instance of this bot. You are physically able to [invite the bot](https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=335400150)


## Commands:

### Voice interactions:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  .  |  .  |  .  |




## Changelog:

### v1.1:
* Bot now uses asyncpg (asynchronous PortgreSQL) to access databases.
* `bot.py` only includes the `comms.Bot` subclass. Extensions are handeled elsewhere.
* Text to speech interactions with people connecting and disconnecting from channels. More to come in future updates.


### v1.0:
* Permission loading and service checks are now automated before bot is available for use.
* First real stable version with no major flaws (I haven't found any within testing yet).
