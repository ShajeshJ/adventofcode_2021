import sys
from typing import Callable
from libraries.questions import get_question_input
from libraries.print_util import make_red


def __update_map(update_func: Callable[[int], int], map: list[list[int]]):
    return [[update_func(o) for o in row] for row in map]


def __get_adjacent(x: int, y: int, map: list[list[int]]):
    """Retrieves all indices adjacent to the given `x`/`y`.
    This function assumes the inner lists all have the same length
    """
    adjacent_indices: list[tuple[int, int]] = []

    if x < 0 or x >= len(map) or y < 0 or y >= len(map[0]):
        # Coordinates that are off the map cannot be adjacent to anything
        return adjacent_indices

    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:
            if i == x and j == y:
                continue  # Don't add the point itself
            if i < 0 or i >= len(map) or j < 0 or j >= len(map[0]):
                continue  # Don't add points out of bounds
            adjacent_indices.append((i, j))

    return adjacent_indices


def part_1():
    data = get_question_input(11)
    octopuses: list[list[int]] = [[int(h) for h in next(data)]]
    map_w = len(octopuses[0])

    num_flashes = 0

    for line in data:
        if len(line) != map_w:
            sys.exit(make_red("Octopus map data does not have constant width"))
        octopuses.append([int(h) for h in line])

    # Simulating 100 steps
    for _ in range(100):
        # Increment flash counts
        octopuses = __update_map(lambda x: x + 1, octopuses)

        # Get seed flashers
        flashers: set[tuple[int, int]] = set()
        for x, row in enumerate(octopuses):
            for y, flash_amt in enumerate(row):
                if flash_amt > 9:
                    flashers.add((x, y))

        # Process flashes and chain flashes
        flashed: set[tuple[int, int]] = set()
        while len(flashers) > 0:
            flasher = flashers.pop()
            flashed.add(flasher)
            num_flashes += 1

            # Don't double count adjacents that flashed
            adjacent = set(__get_adjacent(*flasher, octopuses)) - flashed
            for a_x, a_y in adjacent:
                octopuses[a_x][a_y] += 1
                if octopuses[a_x][a_y] > 9:
                    flashers.add((a_x, a_y))

        # Reset all octopuses that flashed
        for x, y in flashed:
            octopuses[x][y] = 0

    print(num_flashes)
