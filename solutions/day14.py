from libraries.questions import get_question_input
from itertools import pairwise
from collections import Counter


def __perform_mutation_step(polymer: list[str], insertion_rules: dict[str, str]):
    """Function which performs the next polymer mutation step
    given the polymer, and the pair insertion rules the mutations follow.
    """
    new_polymer: list[str] = []

    # Loop from start to 1 before the end of the polymer
    for left_e, right_e in pairwise(polymer):
        middle_e = insertion_rules[f"{left_e}{right_e}"]
        # To avoid dupes, `right_e` is added as `left_e` in the next iteration
        new_polymer.extend([left_e, middle_e])

    # Manually append the last polymer element since it was not added in the loop
    new_polymer.append(polymer[-1])

    return new_polymer


def part_1():
    data = get_question_input(14)
    polymer = [c for c in next(data)]
    next(data)  # Skip empty line

    insertion_rules = {}
    for rule in data:
        pair, value = rule.split(" -> ")
        insertion_rules[pair] = value

    for i in range(10):
        polymer = __perform_mutation_step(polymer, insertion_rules)

    # A list of element+count tuples in descending order of count
    element_counts = Counter(polymer).most_common()

    print(element_counts[0][1] - element_counts[-1][1])
