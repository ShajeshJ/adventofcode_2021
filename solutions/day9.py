import sys
from libraries.print_util import make_red
from libraries.questions import get_question_input


def __get_adjacent_indices(map: list[list[int]], row: int, col: int):
    """Retrieves all indices adjacent to the given `row`/`col`.
    This function assumes the inner lists all have the same length
    """
    adjacent_indices: list[tuple[int, int]] = []

    if row < 0 or row >= len(map) or col < 0 or col >= len(map[0]):
        # Coordinates that are off the map cannot be adjacent to anything
        return adjacent_indices

    if row - 1 >= 0:
        adjacent_indices.append((row - 1, col))
    if col - 1 >= 0:
        adjacent_indices.append((row, col - 1))
    if row + 1 < len(map):
        adjacent_indices.append((row + 1, col))
    if col + 1 < len(map[0]):
        adjacent_indices.append((row, col + 1))

    return adjacent_indices


def part_1():
    data = get_question_input(9)
    heightmap = [[int(h) for h in next(data)]]
    map_width = len(heightmap[0])

    for line in data:
        if len(line) != map_width:
            sys.exit(make_red("Heightmap data does not have constant width"))

        heightmap.append([int(h) for h in line])

    risk_sum = 0
    low_points: list[tuple[int, int]] = []

    for row, row_cols in enumerate(heightmap):
        for col, height in enumerate(row_cols):
            adjacent_indices = __get_adjacent_indices(heightmap, row, col)

            if not adjacent_indices:
                continue

            if height < min(heightmap[x][y] for x, y in adjacent_indices):
                risk_sum += height + 1
                low_points.append((row, col))

    print(risk_sum)

    return heightmap, low_points


def part_2():
    heightmap, low_points = part_1()

    basin_sizes = []

    for low_point in low_points:
        basin: set[tuple[int, int]] = set()
        unchecked_indices = set([low_point])

        while len(unchecked_indices) > 0:
            p_x, p_y = unchecked_indices.pop()

            if heightmap[p_x][p_y] < 9:
                basin.add((p_x, p_y))
                unchecked_indices |= (
                    set(__get_adjacent_indices(heightmap, p_x, p_y)) - basin
                )  # Make sure to skip points already in the basin

        basin_sizes.append(len(basin))

    basin_sizes.sort(reverse=True)
    print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])
