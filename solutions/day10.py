from libraries.questions import get_question_input

__CHUNK_CHARS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def part_1():
    score_lookup = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
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
                error_score += score_lookup[c]
                break

    print(error_score)


def part_2():
    score_lookup = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    incomplete_scores = []

    for seq in get_question_input(10):
        parse_stack = []
        is_corrupted = False

        for c in seq:
            # Start of new chunk
            if c in __CHUNK_CHARS.keys():
                parse_stack.append(c)
                continue

            # Corrupted chunk found
            if __CHUNK_CHARS[parse_stack.pop()] != c:
                is_corrupted = True
                break

        if not is_corrupted:
            score = 0
            while len(parse_stack) > 0:
                score *= 5
                score += score_lookup[__CHUNK_CHARS[parse_stack.pop()]]

            # Score of 0 is a complete and correct chunk
            if score > 0:
                incomplete_scores.append(score)

    incomplete_scores.sort()
    print(incomplete_scores[len(incomplete_scores) // 2])
