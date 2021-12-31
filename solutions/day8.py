from libraries.questions import get_question_input


def part_1():
    data = get_question_input(8)
    # 1, 4, 7, 8 use 2, 4, 3, 7 segments respectively
    SPECIAL_SEGMENT_COUNTS = [2, 4, 3, 7]
    simple_numbers_count = 0

    for line in data:
        output = line.split(" | ")[1]
        simple_numbers_count += sum(
            1
            for out_digit in output.split()
            if len(out_digit) in SPECIAL_SEGMENT_COUNTS
        )

    print(simple_numbers_count)
