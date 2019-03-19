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
    CWHITE = '\33[37m'


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
