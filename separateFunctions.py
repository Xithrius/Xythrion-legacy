import os
import platform
import sys


class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   CWHITE  = '\33[37m'


def path(*objects):
    if platform.system() == "Windows":
        return "{}\\{}".format(os.path.dirname(os.path.realpath(__file__)), '\\'.join(str(y) for y in objects))
    elif platform.system() == "Linux":
        return "{}/{}".format(os.path.dirname(os.path.realpath(__file__)), '/'.join(str(y) for y in objects))


def error_prompt(string, option=None):
    if option is not None:
        x = f"#{'/' * len(string)}#"
        print(f"{x}\n{option}:\n{string}\n{x}")
    else:
        x = f"#{'/' * len(string)}#"
        print(f"{x}\n{string}\n{x}")


def input_loop(string):
    check = True
    while check:
        for i in range(len(string)):
            if string[i] == '[':
                forwardBracket = i + 1
            elif string[i] == ']':
                backwardBracket = i
    stringOptions = string[forwardBracket:backwardBracket]
    if "/" in stringOptions:
        options = (stringOptions).split("/")
        inCheck = True
        while inCheck:
            print(string, end='', flush=True)
            In = input(" ")
            if In in options:
                return In
                inCheck = False
            else:
                print(f"Input does not match options of {', '.join(str(y) for y in options)}")
    elif "/" not in stringOptions:
        inCheck = True
        while inCheck:
            print(string, end='', flush=True)
            In = input(" ")
            if stringOptions == "int":
                try:
                    In = int(In)
                    return In
                    inCheck = False
                except ValueError:
                    print("Input does match type {stringOptions}")


def welcome_prompt():
    title = '''
    █ █ █
    █    █
    █    █
    █    █
    █ █ █
    '''
    print(title)
    print('{0}[{1}-{2}]{3}--> {4}'.format(Color.PURPLE, Color.RED, Color.PURPLE, Color.RED, Color.GREEN),
          'Built by: Xithrius')
