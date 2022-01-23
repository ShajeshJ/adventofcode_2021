from copy import deepcopy
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


def __find_min_risk_total(risk_map: list[list[int]]):
    """Given a square `risk_map`, uses Dijkstra's algorithm to find the total of the
    minimum risk path from the top left node, to the bottom right node.
    """
    map_h = len(risk_map)
    map_w = len(risk_map[0])
    start = (0, 0)
    target = (map_h - 1, map_w - 1)

    visited_nodes: set[tuple[int, int]] = set()  # Set of nodes that have been visited
    candidates: dict[tuple[int, int], int] = {}  # Nodes to check and their risk totals

    # Initialize starting node with total risk of 0
    candidates[start] = 0

    while candidates:
        cur_node: tuple[int, int] = min(candidates, key=candidates.get)
        cur_risk = candidates.pop(cur_node)
        visited_nodes.add(cur_node)

        if cur_node == target:
            # Smallest risk path found; return total risk of that path
            return cur_risk

        for neighbour in __get_neighbours(cur_node, map_h, map_w):
            if neighbour in visited_nodes:
                continue

            n_y, n_x = neighbour
            risk_via_cur = cur_risk + risk_map[n_y][n_x]

            if neighbour not in candidates:
                candidates[neighbour] = risk_via_cur
                continue
            elif candidates[neighbour] > risk_via_cur:
                candidates[neighbour] = risk_via_cur

    sys.exit(make_red(f"Failed to find a path from {start} to the {target} nodes"))


def part_1():
    data = get_question_input(15)
    risk_map: list[list[int]] = []

    # Assumes map has uniform width (i.e. map is a rectangle)
    for line in data:
        risk_map.append([int(r) for r in line])

    print(__find_min_risk_total(risk_map))


def part_2():
    data = get_question_input(15)
    risk_map: list[list[int]] = []

    # Assumes map has uniform width (i.e. map is a rectangle)
    for line in data:
        risk_map.append([int(r) for r in line])

    def _wrap_inc(risk: int, inc: int):
        return (risk - 1 + inc) % 9 + 1

    # Extend across columns
    template_w = len(risk_map[0])
    for row in risk_map:
        for i in range(1, 5):
            row.extend([_wrap_inc(risk, i) for risk in row[0:template_w]])

    # Extend across rows
    template_h = len(risk_map)
    for i in range(1, 5):
        risk_map.extend(
            [[_wrap_inc(risk, i) for risk in row] for row in risk_map[0:template_h]]
        )

    print(__find_min_risk_total(risk_map))
