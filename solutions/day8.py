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
    DIGIT_SEGMENT_COUPLING: list[tuple[int, set[str]]] = [
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
        try:
            self.reset_translations()
            self.build_translations(wirings)
        except:
            sys.exit(make_red(f"Failed setting up translations for wirings: {wirings}"))

    def reset_translations(self):
        """Reset translation lookups"""
        self.seg_translation: dict[str, str] = {}
        self.digit_translations: list[tuple[int, set[str]]] = []

    def build_translations(self, wirings: list[str]):
        """Build the segment translation table given the current wirings for the 10 digits

        Must ensure translations are reset before calling (via `reset_translation`)
        """
        if len(wirings) != 10:
            raise Exception()

        wiring_sets = [{c for c in w} for w in wirings]

        # Determine `a` using segments of 7 and 1:
        one_segments = next(w for w in wiring_sets if len(w) == 2)
        seven_segments = next(w for w in wiring_sets if len(w) == 3)
        self.seg_translation["a"] = (seven_segments - one_segments).pop()

        # Determine `c` using segments of 6
        six_seg_digits = [w for w in wiring_sets if len(w) == 6]  # Contains 0, 6, 9
        # Only 6 does not contain both segments in 1
        six_segments = next(s for s in six_seg_digits if not s.issuperset(one_segments))
        self.seg_translation["c"] = (DigitTranslator.ALL_SEGMENTS - six_segments).pop()

        # Determine segments of 9 using segments of 4; then determine `e` using segments of 9
        six_seg_digits.remove(six_segments)  # Now contains 0, 9
        four_segments = next(w for w in wiring_sets if len(w) == 4)
        nine_segments = next(s for s in six_seg_digits if s.issuperset(four_segments))
        self.seg_translation["e"] = (DigitTranslator.ALL_SEGMENTS - nine_segments).pop()

        # Determine `d` using segments of 0
        six_seg_digits.remove(nine_segments)  # Now contains 0
        zero_segments = six_seg_digits[0]
        self.seg_translation["d"] = (DigitTranslator.ALL_SEGMENTS - zero_segments).pop()

        # Determine `f` using `c` and segments of 1
        self.seg_translation["f"] = (one_segments - {self.seg_translation["c"]}).pop()

        # Determine `b` using `c`, `d`, `f` and segments of 4
        temp_set_for_b = four_segments - {
            self.seg_translation["c"],
            self.seg_translation["d"],
            self.seg_translation["f"],
        }
        self.seg_translation["b"] = temp_set_for_b.pop()

        # Determine `g` using all other known segments
        self.seg_translation["g"] = next(
            s
            for s in DigitTranslator.ALL_SEGMENTS
            if s not in self.seg_translation.values()
        )

        # Finally build digit <-> translated segment map for convenience
        self.digit_translations = [
            (d, {self.seg_translation[s] for s in sm})
            for d, sm in DigitTranslator.DIGIT_SEGMENT_COUPLING
        ]

    def translate(self, powered_segments: str):
        """Translate a given wiring into a digit"""
        powered_set = {c for c in powered_segments}

        return next(
            digit
            for digit, translation in self.digit_translations
            if translation == powered_set
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
