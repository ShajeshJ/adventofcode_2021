from collections import Counter
from itertools import pairwise
from libraries.questions import get_question_input


def __get_mutation_step_outcome(
    element_pairs: dict[str, int], insertion_rules: dict[str, str]
):
    """Function which takes the number of occurrences of element pairs in an initial polymer, and
    determines the number of occurrences of element pairs in the polymer after 1 insertion step.

    This function is created for performance, to avoid having to calculate the actual polymer.
    """

    new_pairs: dict[str, int] = {}

    for pair, count in element_pairs.items():
        # Every element pair creates two new pairs in the next step
        left_pair = f"{pair[0]}{insertion_rules[pair]}"
        new_pairs[left_pair] = new_pairs.setdefault(left_pair, 0) + count

        right_pair = f"{insertion_rules[pair]}{pair[1]}"
        new_pairs[right_pair] = new_pairs.setdefault(right_pair, 0) + count

    return new_pairs


def part_1(num_steps=10):
    data = get_question_input(14)
    init_polymer = [c for c in next(data)]
    next(data)  # Skip empty line

    insertion_rules = {}
    for rule in data:
        pair, value = rule.split(" -> ")
        insertion_rules[pair] = value

    # Will track the count of paired elements in a polymer
    # Using `Counter` here to properly count occurrences of each pair in the initial polymer
    polymer_pairs = dict(
        Counter(f"{left}{right}" for left, right in pairwise(init_polymer))
    )

    for _ in range(num_steps):
        polymer_pairs = __get_mutation_step_outcome(polymer_pairs, insertion_rules)

    """
    Element Counting Explaination:

    Each element of the final polymer will be included in the counts for two
    element pairs, with the exception of the first and last elements of the polymer.

    So to compute, we first increase the counts for each element in the pair
    by its count. Then we temporarily subtract 1 for the first/last element counts
    to ensure they don't get adjusted. Then we fix all counts by halving them, and
    finally we re-add 1 for the first/last element counts.

    The first and last elements in a polymer are unchanged after each polymer step, so
    we can just look at the initial polymer to see what they will be in the final polymer.
    """

    element_counts: dict[str, int] = {}

    for pair, count in polymer_pairs.items():
        # Add `count` to the counts for each element in the pair
        element_counts[pair[0]] = element_counts.setdefault(pair[0], 0) + count
        element_counts[pair[1]] = element_counts.setdefault(pair[1], 0) + count

    element_counts[init_polymer[0]] -= 1
    element_counts[init_polymer[-1]] -= 1
    element_counts = {element: count // 2 for element, count in element_counts.items()}
    element_counts[init_polymer[0]] += 1
    element_counts[init_polymer[-1]] += 1

    print(max(element_counts.values()) - min(element_counts.values()))


def part_2():
    part_1(40)


"""
Part 1 Original Implementation

def __simulate_mutation_step(polymer: list[str], insertion_rules: dict[str, str]):
    \"""Function which simulates the next polymer mutation step and returns
    the resulting polymer, given the initial polymer and the pair insertion rules.
    \"""
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

    for _ in range(10):
        # Note this can be refactored to use `__get_mutation_outcome_step` for performance
        # But for part 1 with only 10 steps, this is performant enough
        polymer = __simulate_mutation_step(polymer, insertion_rules)

    # A list of element+count tuples in descending order of count
    element_counts = Counter(polymer).most_common()

    print(element_counts[0][1] - element_counts[-1][1])
"""
