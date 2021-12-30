from libraries.questions import get_question_input


def part_1():
    inputs = get_question_input(1)
    prev = int(next(inputs))
    num_increases = 0
    for depth in inputs:
        if int(depth) > prev:
            num_increases += 1
        prev = int(depth)
    print(num_increases)


def part_2():
    inputs = get_question_input(1)
    window = [int(next(inputs)) for i in range(3)]
    num_increases = 0

    for depth in inputs:
        window.append(int(depth))
        if window[-1] > window[0]:
            num_increases += 1
        window.pop(0)

    print(num_increases)
