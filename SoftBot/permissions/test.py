def my_custom_check():
    def predicate(ctx):
        # a function that takes ctx as it's only arg, that returns a truethy or falsey value, or raises an exception
    return commands.check(predicate)
