# Demonically
Operating on applications in a demon-like manner
https://github.com/Xithrius/Demonically


# TODO
- [x] Use [discord.py rewrite with cogs](!https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be) to understand how discord.py rewrite update works
- [x] Learn what other changes happened to discord.py rewrite
- [x] Open Weather Maps API for weather
- [ ] Recreate the help command
- [ ] Quality Of Life command creations
- [ ] Get ping to discord server when starting the bot
- [ ] Customized commands through discord messages, will be put into separate folder
- [ ] Add permissions to the bot, so multiple people can have access to high-level commands
- [ ] Google Cloud Search, Drive, Calendar
- [ ] Multithreading and using different programs for the same application running in unison
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

# v0.00.0009, pushed
### Changes:
* All commands now trigger typing until message is sent, or after 10 seconds
* Wrote out the logo-type-thing for the bot for welcome in essentials, and started using it on startup
* Added events to directives cog that returns and catches exceptions
### Bugfixes:
*

## v0.00.0008, pushed 03/25/2019, 2:27pm PDT
### Changes:
* Command added to see creator of bot
* SSL added to bot object initiation so it won't give error when attempting to come online
* Modified the TODO
* Removed all Python cache files from GitHub, but they're still stored locally
* Preparing for bot to become public repository
* Preparing for encrypted password storage
* Discord help command removed, replaced with currently-developing custom help commands
* Removed credentials directory files, moved information to config file within same directory
* Google text-to-speech has been added, still testing, only available for bot owner
* Open Weather Maps added, returns embed of weather for user input location
* Added another example to examples
* Added logger, off by default
* Discord bot token can be inputted as first argument in console
* Added logging option as the second system argument in console, so it's enabled from there if need be
* Renamed text to speech cog
* Help cog is named "guidance"
### Bugfixes:
* Anaconda navigator will screw up everything, so the fix for this is to not install it
 * If installed, go to roaming, app data, then delete the anaconda folder

## v0.00.0007, pushed 03/18/2019 9:48pm PDT
### Changes:
* The essentials directory is now a custom package full of error checking and path giving
* Removed description from bot, it doesn't do anything useful at the moment
* Path module within the essentials package has been minimized and now can be used in relative to the caller path
* Pushes will now have exact times of when I clicked the "Commit to master" button
### Bugfixes:
* Bot comes online properly and activates on ready event

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
