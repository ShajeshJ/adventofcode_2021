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


def __simulate_step(octo_map: list[list[int]]):
    """Given an octopus map, will simulate the next step of flashes.

    Returns the octopus map with the new flash values, as well as
    a list of coordinates for all the octopuses who flashed during the step.
    """
    # Increment flash charges of all octopus
    octo_map = __update_map(lambda x: x + 1, octo_map)

    # Get seed flashers
    flashers: set[tuple[int, int]] = set()
    for x, row in enumerate(octo_map):
        for y, flash_amt in enumerate(row):
            if flash_amt > 9:
                flashers.add((x, y))

    # Process flashes and chain flashes
    flashed: set[tuple[int, int]] = set()
    while len(flashers) > 0:
        flasher = flashers.pop()
        flashed.add(flasher)

        # Don't double count adjacents that already flashed
        adjacent = set(__get_adjacent(*flasher, octo_map)) - flashed
        for a_x, a_y in adjacent:
            octo_map[a_x][a_y] += 1
            if octo_map[a_x][a_y] > 9:
                flashers.add((a_x, a_y))

    # Reset flash charge for the octopuses that flashed
    for x, y in flashed:
        octo_map[x][y] = 0

    return octo_map, flashed


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
        octopuses, flashed_octopuses = __simulate_step(octopuses)
        num_flashes += len(flashed_octopuses)

    print(num_flashes)


def part_2():
    data = get_question_input(11)
    octopuses: list[list[int]] = [[int(h) for h in next(data)]]
    map_w = len(octopuses[0])

    for line in data:
        if len(line) != map_w:
            sys.exit(make_red("Octopus map data does not have constant width"))
        octopuses.append([int(h) for h in line])

    num_octopuses = map_w * len(octopuses)
    flashed_octopuses: set[tuple[int, int]] = set()
    step = 0

    while len(flashed_octopuses) != num_octopuses:
        step += 1
        octopuses, flashed_octopuses = __simulate_step(octopuses)

    print(step)
