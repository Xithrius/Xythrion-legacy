<p align="center">
    <img src="/images/icon.png"/>
</p>

<h1 align="center">Xythrion v2.0</h1>

<h3 align="center">Graphing information from APIs</h3>

<p align="center">
    <img src="https://img.shields.io/apm/l/vim-mode.svg"/>
    <img src="https://img.shields.io/badge/python-3.7.4-green.svg">
</p>

<p align="center">
    <a href="https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=335400150">Invite</a> -
    <a href="#commands">Commands</a> -
    <a href="#changelog">Changelog</a>
</p>


# Commands:

### Template table:
|  Command  |  Argument(s)  |  Output  |
| ------------- | ------------- | ------------- |
|  .  |  .  |  .  |


# Changelog

## v1.1 (unreleased):

### Added:
- Some motivation to actually do this project.
- API tracking such as how weather changes within an area, and how a certien Reddit post is doing over a couple days.
- Added `Added`, `Changed`, and `Removed` items to the tags of versions.
- Added the ability to graph math equations.

### Changed:
- Rewrote the readme file to use `-` instead of `*`.

### Removed:
- Building sourcing cogs. This will be moved to my other bot, [Demoness](!https://www.github.com/Xithrius/Demoness).


### [v1.01](!https://github.com/Xithrius/Xythrion/releases/tag/v1.0.1):
* Bot now uses asyncpg (asynchronous PortgreSQL) to access databases.
* `bot.py` now subclasses `comms.Bot`, while Main_Cog gets `comms.Cog`. 
* The extensions `etg.py` and `imgur.py` have been brought back from the dead.
* Parser and shortcut functions have now been removed from the subclass of `bot.py` and moved to their own place in `modules/`.
* The setup within this README has been given extra files for token generation. 


### [v1.0](!https://github.com/Xithrius/Xythrion/releases/tag/v1.0):
* Permission loading and service checks are now automated before bot is available for use.
* First real stable version with no major flaws (I haven't found any within testing yet).