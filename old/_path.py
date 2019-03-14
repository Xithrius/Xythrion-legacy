import os
import platform
import sys

import _error_prompt


def main(*objects):
    if platform.system() == "Windows":
        print(os.path.dirname(os.path.realpath(__file__)))
        return "{}\\{}".format(os.path.dirname(os.path.realpath(__file__)), '\\'.join(str(y) for y in objects))
    elif platform.system() == "Linux":
        return "{}/{}".format(os.path.dirname(os.path.realpath(__file__)), '/'.join(str(y) for y in objects))
    else:
        error_prompt.main(f"Platform {platform.system()} is not supported. Contact my creator.")
