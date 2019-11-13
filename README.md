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
    <a href="#commands">Commands</a> -
    <a href="#setup">Setup</a> -
    <a href="#changelog">Changelog</a>
</p>


### Preface: 
* AWS will be running this bot in the near future, so you don't need to create your own instance of the bot. You are physically able to [invite the bot](https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=335400150).
* If you still want to set the bot up for yourself, the [setup](#setup) section will lead you.


## Commands:

### Template table:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  .  |  .  |  .  |


## Changelog:

### v1.1:
* Bot now uses asyncpg (asynchronous PortgreSQL) to access databases.
* `bot.py` now subclasses `comms.Bot`, while Main_Cog gets `comms.Cog`. 
* The extensions `etg.py` and `imgur.py` have been brought back from the dead.
* Parser and shortcut functions have now been removed from the subclass of `bot.py` and moved to their own place in `modules/`.
* The setup within this README has been given extra files for token generation. 


### v1.0:
* Permission loading and service checks are now automated before bot is available for use.
* First real stable version with no major flaws (I haven't found any within testing yet).


## Setup:

### Items that require configuration:

|  Item  |  Link to instructions  |
| ------------- | ------------- |
| Python  |  .  |
| Config file  |  .  |
| Discord  |  .  |
| Weather  |  .  |
| TTS  |  .  |

