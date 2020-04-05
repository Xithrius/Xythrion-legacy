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


## Commands:
(insert gif here)

## Changelog

### [v2.0](!https://github.com/Xithrius/Xythrion/releases/tag/v2.0)
#### Added:
- Motivation to actually do this project.
- Documentation that's actually useful
- Tables instead of weird broken graphs, and replaced the void with more graphs.
- 

#### Changed:
- Importing from `modules/`.
- The way embeds are formatted.
- Configuration of the bot, and the different options at launch.

#### Removed:
- No longer recording specific messages and their content sent by users, only adding it to the count of messages/commands.
- Enter The Gungeon wiki and imgur cogs. These may be put back in the future.
- The youtube to mp3 command since it's against YouTube's TOS.
- Really bad embed tables that no one liked.
- The TTS command (I really wonder why I implimented it in the first place).

### v0-v1.1 (Development of the project, I wouldn't look too close at these versions)
- API tracking such as how weather changes within an area, and how a certien Reddit post is doing over a couple days.
- Added the ability to graph math equations.
- Building sourcing cogs. This will be moved to my other bot, [Demoness](!https://www.github.com/Xithrius/Demoness).
- Bot now uses asyncpg (asynchronous PortgreSQL) to access databases.
- `bot.py` now subclasses `comms.Bot`, while Main_Cog gets `comms.Cog`. 
- The extensions `etg.py` and `imgur.py` have been brought back from the dead.
- Parser and shortcut functions have now been removed from the subclass of `bot.py` and moved to their own place in `modules/`.
- The setup within this README has been given extra files for token generation.
- Permission loading and service checks are now automated before bot is available for use.
- First real stable version with no major flaws (I haven't found any within testing yet).
