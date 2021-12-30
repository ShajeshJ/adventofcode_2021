import math
from libraries.questions import get_question_input


def part_1():
    data = get_question_input(7)
    crab_positions = [int(p) for p in next(data).split(",")]

    # The ideal position is just the median of all the positions in this case
    num_crabs = len(crab_positions)
    crab_positions.sort()
    if num_crabs % 2 != 0:
        # For odd length lists, the median is the middle number
        ideal_position = crab_positions[num_crabs // 2]
    else:
        # For even length lists, the median is the average of the middle numbers
        ideal_position = (
            crab_positions[num_crabs // 2] + crab_positions[num_crabs // 2 - 1]
        ) // 2

    ideal_usage = sum(abs(p - ideal_position) for p in crab_positions)
    print(ideal_usage)


def part_2():
    data = get_question_input(7)
    crab_positions = [int(p) for p in next(data).split(",")]

    def _calculate_usage(t: int):
        """Calculates usage using sum of arithmetic series formula, (n+1)*n/2"""
        return int(sum((abs(p - t) + 1) * abs(p - t) / 2 for p in crab_positions))

    # The ideal position is just the mean of all positions in this case
    ideal_position = sum(crab_positions) / len(crab_positions)

    if ideal_position.is_integer():
        ideal_position = int(ideal_position)
        ideal_usage = _calculate_usage(ideal_position)
    else:
        # Target cannot be decimal so we'll test both integers around the target
        ideal_position = int(ideal_position)
        ideal_usage = _calculate_usage(ideal_position)

        contest_usage = _calculate_usage(ideal_position + 1)
        if contest_usage < ideal_usage:
            ideal_position += 1
            ideal_usage = contest_usage

    print(ideal_usage)


"""
Original attempts at parts 1&2:

def part_1():
    data = get_question_input(7)
    crab_positions = [int(p) for p in next(data).split(",")]

    _get_usage = lambda i: sum(abs(p - i) for p in crab_positions)

    ideal_position = min(crab_positions)
    ideal_usage = _get_usage(ideal_position)

    for candidate_pos in range(min(crab_positions) + 1, max(crab_positions) + 1):
        candidate_usage = _get_usage(candidate_pos)
        if candidate_usage < ideal_usage:
            ideal_position = candidate_pos
            ideal_usage = candidate_usage

    print(ideal_usage)


def part_2():
    data = get_question_input(7)
    crab_positions = [int(p) for p in next(data).split(",")]

    def _get_usage(target_pos: int):
        _num_steps = lambda p: abs(p - target_pos)

        # Usage is just the sum of the arithmetic series 1..n (steps)
        # This is calculated with the formula: (n+1)*n/2
        _individual_usage = lambda p: int((_num_steps(p) + 1) * _num_steps(p) / 2)

        return sum(_individual_usage(p) for p in crab_positions)

    ideal_position = min(crab_positions)
    ideal_usage = _get_usage(ideal_position)

    for candidate_pos in range(min(crab_positions) + 1, max(crab_positions) + 1):
        candidate_usage = _get_usage(candidate_pos)
        if candidate_usage < ideal_usage:
            ideal_position = candidate_pos
            ideal_usage = candidate_usage

    print(ideal_usage)
 """
