import os
import platform

def pathing(object):
    if platform.system() == "Windows":
        return f"{os.path.dirname(os.path.realpath(__file__))}\\{object}"
    elif platform.system() == "Linux":
        return f"{os.path.dirname(os.path.realpath(__file__))}/{object}"
