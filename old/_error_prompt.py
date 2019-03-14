def main(string, option=None):
    if option is not None:
        x = f"#{'/' * len(string)}#"
        print(f"{x}\n{option}:\n{string}\n{x}")
    else:
        x = f"#{'/' * len(string)}#"
        print(f"{x}\n{string}\n{x}")
