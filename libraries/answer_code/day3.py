from typing import Iterable
from libraries.questions import get_question_input


def part_1():
    inputs = get_question_input(3)
    bit_set_count = [int(bit) for bit in next(inputs) if bit.isdigit()]
    total_lines = 1
    for binary_num in inputs:
        bit_set_count = [
            count + int(bit) for count, bit in zip(bit_set_count, binary_num)
        ]
        total_lines += 1

    gamma_rate = "".join(
        "1" if count > total_lines / 2 else "0" for count in bit_set_count
    )
    gamma_rate = int(gamma_rate, 2)
    epsilon_rate = gamma_rate ^ int("".join("1" * len(bit_set_count)), 2)

    print(gamma_rate * epsilon_rate)


def part_2():
    o2_gen_candidates, co2_scrub_candidates = __get_candidates(get_question_input(3), 0)

    idx = 1
    while len(o2_gen_candidates) > 1:
        o2_gen_candidates, _ = __get_candidates(o2_gen_candidates, idx)
        idx += 1

    o2_generator = int(o2_gen_candidates[0], 2)

    idx = 1
    while len(co2_scrub_candidates) > 1:
        _, co2_scrub_candidates = __get_candidates(co2_scrub_candidates, idx)
        idx += 1

    co2_scrubber = int(co2_scrub_candidates[0], 2)

    print(o2_generator * co2_scrubber)


def __get_candidates(
    bit_strs: Iterable[str], index: int
) -> tuple[list[str], list[str]]:
    """Sort bit strings into ones that are appropriate for oxygen generator vs
    CO2 scrubbers based on the `index` to examine

    Will return a tuple of two lists, the first being the oxygen generator candidates,
    and the second being the CO2 scrubber candidates
    """
    bit_set_list = []
    bit_unset_list = []

    for bit_str in bit_strs:
        if bit_str[index] == "1":
            bit_set_list.append(bit_str)
        elif bit_str[index] == "0":
            bit_unset_list.append(bit_str)

    # return o2_gen_candidates, co2_scrub_candidates
    if len(bit_set_list) >= len(bit_unset_list):
        return bit_set_list, bit_unset_list
    else:
        return bit_unset_list, bit_set_list
