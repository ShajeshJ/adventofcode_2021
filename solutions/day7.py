from libraries.questions import get_question_input


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
