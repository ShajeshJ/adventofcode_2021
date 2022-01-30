from libraries.questions import get_question_input


def part_1():
    data = next(get_question_input(17))
    y_data = data.split()[-1]
    y_min, _ = (int(n) for n in y_data.replace("y=", "").split(".."))
    print(-y_min * (-y_min - 1) / 2)
