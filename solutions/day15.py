import sys
from libraries.questions import get_question_input
from libraries.print_util import make_red


def __get_neighbours(node: tuple[int, int], map_h: int, map_w: int):
    """Helper function to get all valid neighbours of `node`, given the map dimensions"""
    y, x = node
    neighbours: list[tuple[int, int]] = []
    if y > 0:
        neighbours.append((y - 1, x))
    if y < map_h - 1:
        neighbours.append((y + 1, x))
    if x > 0:
        neighbours.append((y, x - 1))
    if x < map_w - 1:
        neighbours.append((y, x + 1))
    return neighbours


def part_1():
    """Solved using Dijkstra's algorithm"""

    data = get_question_input(15)
    risk_map: list[list[int]] = []

    # First iteration to get `map_w`
    line = next(data)
    map_w = len(line)
    risk_map.append([int(r) for r in line])

    for line in data:
        if map_w != len(line):
            sys.exit(make_red(f"Disproportionate map width at line {len(risk_map)}"))
        risk_map.append([int(r) for r in line])

    map_h = len(risk_map)
    target = (map_h - 1, map_w - 1)  # Destination node is bottom right of the map
    target_risk = None

    # The set of nodes that are already visited
    visited_nodes: set[tuple[int, int]] = set()
    # Set of candidates with their risk totals from the start
    candidates: dict[tuple[int, int], int] = {(0, 0): 0}

    while candidates:
        cur_node: tuple[int, int] = min(candidates, key=candidates.get)
        cur_risk = candidates.pop(cur_node)

        if cur_node == target:
            # Found smallest risk path
            target_risk = cur_risk
            break

        for y, x in __get_neighbours(cur_node, map_h, map_w):
            if (y, x) in visited_nodes:
                continue
            visited_nodes.add((y, x))

            risk_via_cur = cur_risk + risk_map[y][x]
            if (y, x) not in candidates or candidates[(y, x)] > risk_via_cur:
                candidates[(y, x)] = risk_via_cur

    print(target_risk)
