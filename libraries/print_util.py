def make_red(text: str) -> str:
    return f"\033[91m{text}\033[0m"


def make_gray(text: str) -> str:
    return f"\033[90m{text}\033[0m"


def make_bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"
