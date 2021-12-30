from libraries.questions import get_question_input


def part_1():
    data = get_question_input(5)
    unpaired_points: set[tuple[int, int]] = set()
    paired_points: set[tuple[int, int]] = set()

    for line in data:
        coords1, coords2 = line.split(" -> ")
        x1, y1 = [int(n) for n in coords1.split(",")]
        x2, y2 = [int(n) for n in coords2.split(",")]

        if x1 == x2:
            y_gen = range(y1, y2 + 1) if y1 <= y2 else range(y2, y1 + 1)
            point_generator = ((x1, yn) for yn in y_gen)
        elif y1 == y2:
            x_gen = range(x1, x2 + 1) if x1 <= x2 else range(x2, x1 + 1)
            point_generator = ((xn, y1) for xn in x_gen)
        else:
            continue  # Only consider horizontal / vertical lines

        for point in point_generator:
            if point in paired_points:
                continue
            elif point in unpaired_points:
                unpaired_points.remove(point)
                paired_points.add(point)
            else:
                unpaired_points.add(point)

    print(len(paired_points))
