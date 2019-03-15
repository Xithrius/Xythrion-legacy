# Demonically
Operating on applications in a demon-like manner


# TODO

## NOW:
- [x] Use [discord.py rewrite with cogs](!https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be) to understand how discord.py rewrite update works
- [x] Learn what other changes happened to discord.py rewrite
- [ ] Start using doc-strings for descriptions of anything with .__doc__()
- [ ] Use dot importing with __future__


## FUTURE:
- [ ] Quality Of Life command creations
- [ ] Open Weather Maps API for weather
- [ ] Google Cloud Search, Drive, Calendar
- [ ] Notify user when there's changes to specific things
- [ ] Use shell file for optimization of starting bot during startup
- [ ] Customized commands through discord messages, will be put into separate folder
- [ ] Get ping to discord server when starting the bot
- [ ] Add permissions to the bot, so multiple people can have access (NOT TTS)
- [ ] Multithreading and using different programs for the same application running in unison

## POSSIBILITIES FOR THE FUTURE:
- [ ] 2FA - Quick Response codes through phone with website


# Links for information
* [Repository for Demonically](https://github.com/Xithrius/Demonically)
* [Discord.py rewrite with cogs](https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be)
* [Markdown for .md](https://guides.github.com/features/mastering-markdown/)
* [Example for organization of files](https://github.com/atom/atom)
* [PEP 328 -- Imports: Multi-Line and Absolute/Relative](https://www.python.org/dev/peps/pep-0328/)
* [system arguments in console](https://stackoverflow.com/questions/4117530/sys-argv1-meaning-in-script)
* [What is __future__ in Python?](https://stackoverflow.com/questions/7075082/what-is-future-in-python-used-for-and-how-when-to-use-it-and-how-it-works)


# Changelog

## v0.00.0004
### Changes:
* Changed bot startup, removed bot client class, put on ready event into the main cog
* Modified README for upcoming changes and updates
* Removed all legacy files
* Removed test bot, since main bot file works
* Changed JavaScript Object Notation file for owner ID and token to a text file just for the token
* Removed python "test" file
* Bot almost works

## v0.00.0003
### Changes:
* Removed currently testing folder
* Modified README changelog so people can read it easily
* Shell file now starts entire program
* Really modifying the bot for own use, added own command for testing
* Added credentials in JavaScript Object Notation in credentials folder
* Really smashing multiple files of bots together to see what happens with my own flair from the discord.py rewrite with cogs
* Added bot_test.py to test the bot on specific bugs before adding to bot.py
* Renamed folders and files
* Changed TODO

## v0.00.0002
### Changes:
* Added TODO to this README
* Added other files from old bot, removing old bot from existence

## v0.00.0001
### Changes:
* Changed name from operator to Demonically
* Moved chrome web driver into folder
* Created README.md for all the changelog needs
