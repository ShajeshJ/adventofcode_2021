import itertools
from typing import Generator
from libraries.questions import get_question_input


def part_1():
    data = get_question_input(5)
    unpaired_points: set[tuple[int, int]] = set()
    paired_points: set[tuple[int, int]] = set()

    for line in data:
        coords1, coords2 = line.split(" -> ")
        x1, y1 = [int(n) for n in coords1.split(",")]
        x2, y2 = [int(n) for n in coords2.split(",")]

        if x1 != x2 and y1 != y2:
            continue  # Only consider horizontal / vertical lines

        for point in __get_point_generator(x1, y1, x2, y2):
            if point in paired_points:
                continue
            elif point in unpaired_points:
                unpaired_points.remove(point)
                paired_points.add(point)
            else:
                unpaired_points.add(point)

    print(len(paired_points))


def part_2():
    data = get_question_input(5)
    unpaired_points: set[tuple[int, int]] = set()
    paired_points: set[tuple[int, int]] = set()

    for line in data:
        coords1, coords2 = line.split(" -> ")
        x1, y1 = [int(n) for n in coords1.split(",")]
        x2, y2 = [int(n) for n in coords2.split(",")]

        if x1 != x2 and y1 != y2 and abs(x1 - x2) != abs(y1 - y2):
            continue  # Only consider horizontal / vertical / 45 degree lines

        for point in __get_point_generator(x1, y1, x2, y2):
            if point in paired_points:
                continue
            elif point in unpaired_points:
                unpaired_points.remove(point)
                paired_points.add(point)
            else:
                unpaired_points.add(point)

    print(len(paired_points))


def __get_point_generator(
    x1: int, y1: int, x2: int, y2: int
) -> Generator[tuple[int, int], None, None]:
    """Returns a generator which will list all points between the given coordinates"""

    def _get_axis_generator(axis_start: int, axis_end: int):
        if axis_start == axis_end:
            return itertools.repeat(axis_start)
        elif axis_start < axis_end:
            return range(axis_start, axis_end + 1)
        else:
            return range(axis_start, axis_end - 1, -1)

    x_gen = _get_axis_generator(x1, x2)
    y_gen = _get_axis_generator(y1, y2)

    return ((xn, yn) for xn, yn in zip(x_gen, y_gen))
