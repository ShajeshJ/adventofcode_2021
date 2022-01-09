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


def __print_dots(dots: set[tuple[int, int]]):
    x_size = max(d[0] for d in dots) + 1  # Size of x is 1 > than largest x point
    y_size = max(d[1] for d in dots) + 1  # Size of y is 1 > than largest y point

    # The outer list represents rows, while the inner list represents columns
    mapped_dots: list[list[str]] = [[" "] * (x_size) for _ in range(y_size)]
    for x, y in dots:
        mapped_dots[y][x] = "#"  # Indexes are [rows][cols]; hence the reversal

    output = "\n".join("".join(row) for row in mapped_dots)
    print(output)


def part_1():
    data = get_question_input(13)
    dots: set[tuple[int, int]] = set()

    while line := next(data):
        x, y = (int(n) for n in line.split(","))
        dots.add((x, y))

    fold_dir, fold_point = __parse_fold_data(next(data))

    folded_dots = __perform_fold(fold_dir, fold_point, dots)
    print(len(folded_dots))


def part_2():
    data = get_question_input(13)
    dots: set[tuple[int, int]] = set()

    while line := next(data):
        x, y = (int(n) for n in line.split(","))
        dots.add((x, y))

    while (line := next(data, None)) is not None:
        fold_dir, fold_point = __parse_fold_data(line)
        dots = __perform_fold(fold_dir, fold_point, dots)

    __print_dots(dots)
