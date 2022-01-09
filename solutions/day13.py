from libraries.questions import get_question_input


def __parse_fold_data(line: str):
    fold_dir, fold_point = line.split()[2].split("=")
    fold_point = int(fold_point)
    return fold_dir, fold_point


def __perform_fold(fold_dir: str, fold_point: int, dots: set[tuple[int, int]]):
    new_dots: set[tuple[int, int]] = set()

    for x, y in dots:
        if fold_dir == "x" and x > fold_point:
            x = fold_point - (x - fold_point)  # Mirror across X-axis
        elif fold_dir == "y" and y > fold_point:
            y = fold_point - (y - fold_point)  # Mirror across Y-axis
        new_dots.add((x, y))

    return new_dots


def part_1():
    data = get_question_input(13)
    dots: set[tuple[int, int]] = set()

    while line := next(data):
        x, y = (int(n) for n in line.split(","))
        dots.add((x, y))

    fold_dir, fold_point = __parse_fold_data(next(data))

    folded_dots = __perform_fold(fold_dir, fold_point, dots)
    print(len(folded_dots))
