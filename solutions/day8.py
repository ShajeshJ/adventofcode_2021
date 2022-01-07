import sys
from libraries.print_util import make_red
from libraries.questions import get_question_input


def part_1():
    data = get_question_input(8)
    # 1, 4, 7, 8 use 2, 4, 3, 7 segments respectively
    SPECIAL_SEGMENT_COUNTS = [2, 4, 3, 7]
    simple_numbers_count = 0

    for line in data:
        output = line.split(" | ")[1]
        simple_numbers_count += sum(
            1
            for out_digit in output.split()
            if len(out_digit) in SPECIAL_SEGMENT_COUNTS
        )

    print(simple_numbers_count)


class DigitTranslator:
    """
    Visual Diagram:
     aaaaa
    b     c
    b     c
     ddddd
    e     f
    e     f
     ggggg
    """

    # Set of all segments
    ALL_SEGMENTS = {"a", "b", "c", "d", "e", "f", "g"}

    # A tupling of the base translation of digit to segments powered
    DIGIT_AND_SEGMENT_MAPS: list[tuple[int, set[str]]] = [
        (0, {"a", "b", "c", "e", "f", "g"}),
        (1, {"c", "f"}),
        (2, {"a", "c", "d", "e", "g"}),
        (3, {"a", "c", "d", "f", "g"}),
        (4, {"b", "c", "d", "f"}),
        (5, {"a", "b", "d", "f", "g"}),
        (6, {"a", "b", "d", "e", "f", "g"}),
        (7, {"a", "c", "f"}),
        (8, {"a", "b", "c", "d", "e", "f", "g"}),
        (9, {"a", "b", "c", "d", "f", "g"}),
    ]

    def __init__(self, wirings: list[str]) -> None:
        # Translations for individual segments
        self.segment_map: dict[str, str]
        # Digit + translated segment map pair
        self.digit_translations: list[tuple[int, set[str]]]

        try:
            self.build_translations(wirings)
        except:
            sys.exit(make_red(f"Failed setting up translations for wirings: {wirings}"))

    def build_translations(self, wirings: list[str]):
        """Build the segment translation table given the current wirings for the 10 digits"""
        if len(wirings) != 10:
            raise Exception()

        wiring_sets = [{c for c in w} for w in wirings]
        self.segment_map = {}

        # Determine `a` using wirings of 7 and 1:
        one_wiring = next(w for w in wiring_sets if len(w) == 2)
        seven_wiring = next(w for w in wiring_sets if len(w) == 3)
        self.segment_map["a"] = (seven_wiring - one_wiring).pop()

        # Determine `c` using wiring of 6
        six_seg_wirings = [w for w in wiring_sets if len(w) == 6]  # Contains 0, 6, 9
        # Only 6 does not contain both segments in 1
        six_wiring = next(s for s in six_seg_wirings if not s.issuperset(one_wiring))
        self.segment_map["c"] = (DigitTranslator.ALL_SEGMENTS - six_wiring).pop()

        # Determine wiring of 9 using wiring of 4; then determine `e` using wiring of 9
        six_seg_wirings.remove(six_wiring)  # Now contains 0, 9
        four_wiring = next(w for w in wiring_sets if len(w) == 4)
        nine_wiring = next(s for s in six_seg_wirings if s.issuperset(four_wiring))
        self.segment_map["e"] = (DigitTranslator.ALL_SEGMENTS - nine_wiring).pop()

        # Determine `d` using wiring of 0
        six_seg_wirings.remove(nine_wiring)  # Now contains 0
        zero_wiring = six_seg_wirings[0]
        self.segment_map["d"] = (DigitTranslator.ALL_SEGMENTS - zero_wiring).pop()

        # Determine `f` using `c` and wiring of 1
        self.segment_map["f"] = (one_wiring - {self.segment_map["c"]}).pop()

        # Determine `b` using `c`, `d`, `f` and wiring of 4
        temp_set_for_b = four_wiring - {
            self.segment_map["c"],
            self.segment_map["d"],
            self.segment_map["f"],
        }
        self.segment_map["b"] = temp_set_for_b.pop()

        # Determine `g` using all other known segments
        self.segment_map["g"] = next(
            s
            for s in DigitTranslator.ALL_SEGMENTS
            if s not in self.segment_map.values()
        )

        # Finally we convert the basic (digit, normal segment map) pairs into
        # (digit, translated segment map) pairs using the translations from `self.segment_map`
        self.digit_translations = [
            (d, {self.segment_map[s] for s in sm})
            for d, sm in DigitTranslator.DIGIT_AND_SEGMENT_MAPS
        ]

    def translate(self, powered_segments: str):
        """Translate a given wiring into a digit"""
        powered_set = {c for c in powered_segments}

        return next(
            digit
            for digit, translation in self.digit_translations
            if powered_set == translation
        )


def part_2():
    data = get_question_input(8)
    output_total = 0

    for line in data:
        wirings, outputs = [s.split() for s in line.split(" | ")]
        translator = DigitTranslator(wirings)

        human_digit_str = "".join(
            str(translator.translate(output)) for output in outputs
        )
        output_total += int(human_digit_str)

    print(output_total)
