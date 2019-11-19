## Changelog:

### v1.1:
##### Added:
##### Modified:
##### Removed:
* Bot now uses asyncpg (asynchronous PortgreSQL) to access databases.
* `bot.py` now subclasses `comms.Bot`, while Main_Cog gets `comms.Cog`. 
* The extensions `etg.py` and `imgur.py` have been brought back from the dead.
* Parser and shortcut functions have now been removed from the subclass of `bot.py` and moved to their own place in `modules/`.
* The setup within this README has been given extra files for token generation. 


### v1.0:
* Permission loading and service checks are now automated before bot is available for use.
* First real stable version with no major flaws (I haven't found any within testing yet).