import time


def dot_until_done(line):
    for i in "---> ":
        print(i, end='', flush=True)
        time.sleep(0.1)


dot_until_done("Booting cogs")