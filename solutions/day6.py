from libraries.questions import get_question_input


def part_1(num_days=80):
    data = get_question_input(6)
    lanternfish_age_groups = [0] * 9

    for age in next(data).split(","):
        lanternfish_age_groups[int(age)] += 1

    for _ in range(num_days):
        # Temp track lanternfishes giving birth
        lanternfish_births = lanternfish_age_groups[0]

        # Age all other lanternfish by 1
        for i in range(1, 9):
            lanternfish_age_groups[i - 1] = lanternfish_age_groups[i]

        lanternfish_age_groups[6] += lanternfish_births  # Resetting parents
        lanternfish_age_groups[8] = lanternfish_births  # Adding babies

    print(sum(lanternfish_age_groups))


def part_2():
    part_1(num_days=256)
