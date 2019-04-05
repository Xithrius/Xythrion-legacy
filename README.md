# Demonically
Operating on applications in a demon-like manner
Oriented toward application and specific group interaction
https://github.com/Xithrius/Demonically


# Links for information:
* [Discord.py rewrite with cogs](https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be)
* [Markdown](https://guides.github.com/features/mastering-markdown/)
* [System arguments in console](https://stackoverflow.com/questions/4117530/sys-argv1-meaning-in-script)
* [Install FFmpeg](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg)


# Main objects to install:
* Discord.py rewrite with voice
```
pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]
```
* Virtual environment
```
py -3 -m venv venv
source venv/Scripts/activate
```


# Changelog

## At the end of version numbers, there will be a 'd' or a 'r'. 'd' is for development and 'r' is for release.

### v0.01.0000d, pushed
#### Main changes:
* Yahoo finance stock summary requesting
* 
#### Modifications:
*
#### Bugfixes:
*

### v0.00.0009r, pushed 04/04/2019, 2:11am PDT
#### Main changes:
* Added events to directives cog that returns and catches exceptions
* Started learning machine learning to apply to this bot
* Created the MIT license so people don't go running off with what I created
* Almost ready to make this a public repository
* Started working on the female version of this bot, that is more focused on machine learning and user-oriented interaction
* Broke the virtual environment multiple times but finally fixed it, and it is now working
* Added comments to nearly everything
* Added meme cog for user generated meme input and output
* Put TODO in its own file, since it's going to constantly change
* Plans for the next version, v0.01.0000 (this section will be removed once it comes out):
  * Playback cog will have Spotify to You Tube
  * Reminder cog will remind people with stuff
  * Meme cog will input and output memes from self and users
  * Identity cog will contain more things about the bot and the creator
  * Directives cog will contain more logging info, when the bot starts up with it
  * Setup Python file will be used for people who first use the bot
  * Ease of access to setting up the bot with clear instructions
#### Modifications:
* Moved things around again
* On ready event now prints out in something a quite quaint message
* Playback cog downloads YouTube to mp3 and then plays it through it's own mic
* Passwords are stored by using hashes
* Began testing with setup so other users can use the bot with ease
* Figured out how to use the virtual environment, by the following steps:
  * In git bash, activate the virtual environment by doing `source .\venv\Scripts\activate`
  * The bot can now be ran with the virtual environment in the same console, run with `py -3 .\bot.py`

### v0.00.0008r, pushed 03/25/2019, 2:27pm PDT
#### Main changes:
* Command added to see creator of bot
* Added logging option as the second system argument in console, so it's enabled from there if need be
* Preparing for bot to become public repository
* Discord help command removed, replaced with currently-developing custom help commands
* Google text-to-speech has been added, still testing, only available for bot owner
* Open Weather Maps added, returns embed of weather for user input location
#### Modifications:
* Modified the TODO
* Removed all Python cache files from GitHub, but they're still stored locally
* Preparing for encrypted password storage
* Removed credentials directory files, moved information to config file within same directory
* Added another example to examples
* Renamed text to speech cog
* Help cog is named "guidance"
#### Bugfixes:
* Anaconda navigator will screw up everything, so the fix for this is to not install it
 * If installed, go to roaming, app data, then delete the anaconda folder

### v0.00.0007r, pushed 03/18/2019 9:48pm PDT
#### Main changes:
* Pushes will now have exact times of when I clicked the "Commit to master" button
* The essentials directory is now a custom package full of error checking and path giving
#### Modifications:
* Removed description from bot, it doesn't do anything useful at the moment
* Path module within the essentials package has been minimized and now can be used in relative to the caller path
#### Bugfixes:
* Bot comes online properly and activates on ready event

### v0.00.0006r
#### Main changes:
* Added essentials directory to act as a package for upcoming separated files
#### Modifications:
* Examples from said repository have been removed and put into the examples python file in the cogs directory
* Removed unhelpful links from links for information
* Changed TODO to fit removed links in links for information

### v0.00.0005r
#### Main changes:
* First version with the bot coming online
* Bot's main cog now has decorators for renaming how, where, and who can call the command
* "if \_\_name\_\_ == '\_\_main\_\_'" within main bot file now takes token from console or credentials directory, and then adds the main cog, along with the directives and examples cog
#### Modifications:
* Markdown in ".\_\_doc\_\_()" and "\_\_future\_\_" in the TODO README of section \#\#NOW are no longer bold
* Path in separate functions python file no longer has random print statement
* Renamed separate functions file to be understandable
* Removed bot example in examples directory since all needed information was consumed
* Credentials directory got the files README and git ignore
* Modified main in bot to take 2 arguments then run the bot
#### Bugfixes:
* Bot is able to come online
* cogs are now able to be automatically detected and dot imported from the cogs directory

### v0.00.0004r
#### Main changes:
* Removed all legacy files
* Changed bot startup
* Removed bot client class
* The on ready event is now in the main cog
#### Modifications:
* Modified README for upcoming changes and updates
* Removed test bot, since main bot file works
* Changed JavaScript Object Notation file for owner ID and token to a text file just for the token
* Removed python "test" file
* Bot almost works

### v0.00.0003r
#### Main changes:
* Really modifying the bot for own use
* Added own commands for testing
* Modified README changelog so people can read it easily
#### Modifications:
* Removed currently testing folder
* Shell file now starts entire program
* Added credentials in JavaScript Object Notation in credentials folder
* Really smashing multiple files of bots together to see what happens with my own flair from the discord.py rewrite with cogs
* Added bot_test.py to test the bot on specific bugs before adding to bot.py
* Renamed folders and files
* Changed TODO

### v0.00.0002r
#### Main changes:
* Added other files from old bots
#### Modifications:
* Added TODO to this README

### v0.00.0001r
#### Main changes:
* Created README for updated information on bot
#### Modifications:
* Changed name from Operator to Demonically
* Moved chrome web driver into folder
