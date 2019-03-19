# Demonically
Operating on applications in a demon-like manner
https://github.com/Xithrius/Demonically
# TODO

## Now:
- [x] Use [discord.py rewrite with cogs](!https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be) to understand how discord.py rewrite update works
- [x] Learn what other changes happened to discord.py rewrite
- [ ] Start using doc-strings for descriptions of anything with .\_\_doc\_\_()


## For the future:
- [ ] Quality Of Life command creations
- [ ] Open Weather Maps API for weather
- [ ] Google Cloud Search, Drive, Calendar
- [ ] Notify user when there's changes to specific things
- [ ] Use shell file for optimization of starting bot during startup
- [ ] Customized commands through discord messages, will be put into separate folder
- [ ] Get ping to discord server when starting the bot
- [ ] Add permissions to the bot, so multiple people can have access (NOT TTS)
- [ ] Multithreading and using different programs for the same application running in unison

## Possibilities for the future:
- [ ] 2FA - Quick Response codes through phone with website


# Links for information:
* [Discord.py rewrite with cogs](https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be)
* [Markdown](https://guides.github.com/features/mastering-markdown/)
* [system arguments in console](https://stackoverflow.com/questions/4117530/sys-argv1-meaning-in-script)

# Main packages:
* Discord.py rewrite with voice
```
pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]
```

# Changelog

## v0.00.0007, pushed 03/18/2019 9:48pm PDT
### Changes:
* The essentials directory is now a custom package full of error checking and path giving
* Removed description from bot, it doesn't do anything useful at the moment
* Path module within the essentials package has been minimized and now can be used in relative to the caller path
* Pushes will now have exact times of when I clicked the "Commit to master" button
### Bugfixes:
* Bot doesn't change presence when coming online and doesn't print ready message to console

## v0.00.0006
### Changes:
* Previous version shouldn't have been named v0.01.0004, changed it to v0.00.0005
* Examples cog in the cogs directory now has examples for testing, all credit to [Discord.py rewrite with cogs](https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be)
* Examples from said repository have been removed and put into the examples python file in the cogs directory
* Removed unhelpful links from links for information
* Changed TODO to fit removed links in links for information
* Added essentials directory to act as a package for upcoming separated files

## v0.00.0005
### Changes:
* First version with the bot coming online
* Markdown in ".\_\_doc\_\_()" and "\_\_future\_\_" in the TODO README of section \#\#NOW are no longer bold
* Path in separate functions python file no longer has random print statement
* Renamed separate functions file to be understandable
* Removed bot example in examples directory since all needed information was consumed
* Credentials directory got the files README and git ignore
* Bot's main cog now has decorators for renaming how, where, and who can call the command
* Modified main in bot to take 2 arguments then run the bot
* "if \_\_name\_\_ == '\_\_main\_\_'" within main bot file now takes token from console or credentials directory, and then adds the main cog, along with the directives and examples cog
### Bugfixes:
* Bot is able to come online
* cogs are now able to be automatically detected and dot imported from the cogs directory

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
* Added other files from old bots

## v0.00.0001
### Changes:
* Changed name from Operator to Demonically
* Moved chrome web driver into folder
* Created README for updated information on bot
