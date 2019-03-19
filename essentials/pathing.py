import __main__


def path(*objects):
    newPath = ((__main__.__file__).split("\\"))[:-1]
    for i in objects:
        newPath.append(i)
    return '\\'.join(str(y) for y in newPath)
