import json

import _error_prompt
import _input_loop
import _path


def main():
    try:
        with open(_path.main("InputCreds", "tokens.json"), "r") as f:
            login = json.load(f)
            return [login["discord"]["owner_id"], login["discord"]["bot_token"]]
    except (FileNotFoundError, ValueError) as e:
        error_prompt.main("The file login.json cannot be found or opened properly. Rewriting information...", e)
        with open(_path.main("InputCreds", "tokens.json"), "w") as f:
            owner_id = int(input("Input discord user owner for owner_id [int]: "))
            bot_token = input("Input discord bot token for bot_token: ")
            tokens = {"discord": {"owner_id": owner_id, "bot_token": bot_token}}
            json.dump(tokens, f)
            return [owner_id, bot_token]
            yn = input_loop.main("Is this bot in a Github repository? [y/n]:")
            if yn == 'y':
                with open(_path.main("InputCreds", ".gitignore"), "w") as f:
                    f.write("tokens.json")
            else:
                error_prompt.main("If you're unsure about this bot being in a Github repository,\ncheck README.txt for more information on security.")
    except IndexError as e:
        error_prompt.main("The file tokens.json has been modified and cannot be read.", e)
