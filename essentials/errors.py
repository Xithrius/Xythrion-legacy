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
