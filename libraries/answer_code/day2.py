from libraries.questions import get_question_input


def part_1():
    inputs = get_question_input(2)
    position = 0
    depth = 0

    for cmd in inputs:
        dir, amt, *_ = cmd.split()
        if dir == "forward":
            position += int(amt)
        elif dir == "up":
            depth -= int(amt)
        elif dir == "down":
            depth += int(amt)

    print(position * depth)


def part_2():
    inputs = get_question_input(2)
    depth = 0
    position = 0
    aim = 0

    for cmd in inputs:
        dir, amt, *_ = cmd.split()
        if dir == "forward":
            position += int(amt)
            depth += aim * int(amt)
        elif dir == "down":
            aim += int(amt)
        elif dir == "up":
            aim -= int(amt)

    print(depth * position)
