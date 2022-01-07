from libraries.questions import get_question_input

__CHUNK_CHARS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

__ERROR_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def part_1():
    error_score = 0

    for seq in get_question_input(10):
        parse_stack = []
        for c in seq:
            # Start of new chunk
            if c in __CHUNK_CHARS.keys():
                parse_stack.append(c)
                continue

            # Corrupted chunk found
            if __CHUNK_CHARS[parse_stack.pop()] != c:
                error_score += __ERROR_SCORE[c]
                break
    print(error_score)
