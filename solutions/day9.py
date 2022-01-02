import sys
from libraries.print_util import make_red
from libraries.questions import get_question_input


def part_1():
    data = get_question_input(9)
    heightmap = [int(h) for h in next(data)]
    map_width = len(heightmap)

    for line in data:
        if len(line) != map_width:
            sys.exit(make_red("Heightmap data does not have constant width"))

        heightmap.extend(int(h) for h in line)

    risk_sum = 0

    for i, height in enumerate(heightmap):
        valid_adjacents = []

        if i % map_width != 0:
            # Target is not on the left-most side
            valid_adjacents.append(i - 1)
        if (i + 1) % map_width != 0:
            # Target is not on the right-most side
            valid_adjacents.append(i + 1)
        if i >= map_width:
            # Target is not on the top-most side
            valid_adjacents.append(i - map_width)
        if (i + map_width) < len(heightmap):
            # Target is not on the bottom-most side
            valid_adjacents.append(i + map_width)

        if height < min(heightmap[j] for j in valid_adjacents):
            risk_sum += height + 1

    print(risk_sum)
