from __future__ import annotations
from collections import namedtuple
from copy import deepcopy
from dataclasses import dataclass
from math import ceil, floor
from libraries.questions import get_question_input


_SPLIT_THRESHOLD = 10


def _tokenize(snailfish_str: str) -> list[str | int]:
    """Converts `snailfish_str` into a list of tokens"""
    tokens = []
    token_builder = ""

    def _flush_builder():
        nonlocal token_builder
        if token_builder.isdigit():
            tokens.append(int(token_builder))
            token_builder = ""

    for c in snailfish_str:
        if c in ["[", ",", "]"]:
            _flush_builder()
            tokens.append(c)
        elif c.isdigit():
            token_builder += c
        else:
            raise ValueError(f"Failed to tokenize: Invalid character '{c}' found")

    _flush_builder()
    return tokens


def _get_exploding(
    snailfish_num: SnailfishNumber, depth: int = 0
) -> SnailfishNumber | None:
    """Returns the SnailfishNumber object that should explode, if it exists"""
    if depth == 4:
        return snailfish_num

    for operand in (snailfish_num.left, snailfish_num.right):
        if not isinstance(operand, type(snailfish_num)):
            continue
        if exploder := _get_exploding(operand, depth + 1):
            return exploder

    return None


def _get_split_container(snailfish_num: SnailfishNumber) -> SnailfishNumber | None:
    """Returns the SnailfishNumber object containing
    a number which should split, if it exists
    """
    for operand in (snailfish_num.left, snailfish_num.right):
        if isinstance(operand, int) and operand >= _SPLIT_THRESHOLD:
            return snailfish_num
        if not isinstance(operand, type(snailfish_num)):
            continue
        if split_container := _get_split_container(operand):
            return split_container

    return None


@dataclass
class SnailfishNumber:
    left: int | SnailfishNumber
    right: int | SnailfishNumber
    parent: SnailfishNumber | None = None

    def explode(self):
        """Explodes self"""
        if not isinstance(self.left, int) or not isinstance(self.right, int):
            raise ArithmeticError("Cannot reduce snailfish # with depth > 4")

        self.add_to_left(self.left)
        self.add_to_right(self.right)

        if self.parent.left is self:
            self.parent.left = 0
        elif self.parent.right is self:
            self.parent.right = 0
        else:
            raise Exception(f"No explosion available in {self}")
        self.parent = None  # To avoid memory leaking

    def split_entry(self):
        """Splits the left most entry >= _SPLIT_THRESHOLD within self"""
        cls = type(self)
        if isinstance(self.left, int) and self.left >= _SPLIT_THRESHOLD:
            self.left = cls(floor(self.left / 2), ceil(self.left / 2))
        elif isinstance(self.right, int) and self.right >= _SPLIT_THRESHOLD:
            self.right = cls(floor(self.right / 2), ceil(self.right / 2))
        else:
            raise Exception(f"No split available in {self}")
        self.update_refs_in_children()

    def reduce(self):
        """Reduces self"""
        while True:
            if exploder := _get_exploding(self):
                exploder.explode()
                continue
            if split_container := _get_split_container(self):
                split_container.split_entry()
                continue
            break

    def magnitude(self) -> int:
        """Returns the magnitude of self"""
        left_magnitude = 3 * (
            self.left if isinstance(self.left, int) else self.left.magnitude()
        )
        right_magnitude = 2 * (
            self.right if isinstance(self.right, int) else self.right.magnitude()
        )
        return left_magnitude + right_magnitude

    def add_to_left(self, value: int):
        """Adds `value` to the next operand found traversing left"""
        if self.parent is None:
            # Structure: [self, ...]
            pass
        elif self.parent.left is self:
            # Structure: parent[self, ...]
            self.parent.add_to_left(value)
        elif isinstance(self.parent.left, int):
            # Structure: parent[int, self]
            self.parent.left += value
        else:
            # Structure: parent[left[...,int], self]
            next_left = self.parent.left
            while not isinstance(next_left.right, int):
                next_left = next_left.right
            next_left.right += value

    def add_to_right(self, value: int):
        """Adds `value` to the next operand found traversing right"""
        if self.parent is None:
            # Structure: [..., self]
            pass
        elif self.parent.right is self:
            # Structure: parent[..., self]
            self.parent.add_to_right(value)
        elif isinstance(self.parent.right, int):
            # Structure: parent[self, int]
            self.parent.right += value
        else:
            # Structure: parent[self, right[int, ...]]
            next_right = self.parent.right
            while not isinstance(next_right.left, int):
                next_right = next_right.left
            next_right.left += value

    def update_refs_in_children(self):
        """Updates operand's parent ref to self, where applicable"""
        if isinstance(self.left, type(self)):
            self.left.parent = self
        if isinstance(self.right, type(self)):
            self.right.parent = self

    @classmethod
    def from_tokens(cls, tokens: list[str | int]) -> SnailfishNumber:
        """Uses the given `tokens` to build a `SnailfishNumber` object"""

        def _pop_char(c: str):
            t = tokens.pop(0)
            if t != c:
                raise ValueError(f"Expected `{c}` token but found `{t}` instead")

        def _parse_expression() -> SnailfishNumber | int:
            if tokens[0] == "[":
                return cls.from_tokens(tokens)
            elif isinstance(tokens[0], int):
                return tokens.pop(0)
            else:
                raise ValueError(
                    f"Expected `[` or integer token but found `{tokens[0]}` instead"
                )

        # Parse tokens
        _pop_char("[")
        left = _parse_expression()
        _pop_char(",")
        right = _parse_expression()
        _pop_char("]")

        obj = cls(left, right)
        obj.update_refs_in_children()
        return obj

    @classmethod
    def load(cls, snailfish_str: str) -> SnailfishNumber:
        """Parses and creates a `SnailfishNumber` object from `snailfish_str`"""
        tokens = _tokenize(snailfish_str)
        orig_len = len(tokens)
        try:
            return cls.from_tokens(tokens)
        except Exception as e:
            raise ValueError(
                f"The snailfish_str {snailfish_str} has an invalid "
                f"token at around position {orig_len-len(tokens)}"
            ) from e

    def __add__(self, other: SnailfishNumber) -> SnailfishNumber:
        """Adds two SnailfishNumber objects together."""
        if not isinstance(other, type(self)):
            raise TypeError(f"Cannot add object of type {type(other)} to {type(self)}")

        sum = SnailfishNumber(deepcopy(self), deepcopy(other))
        sum.update_refs_in_children()
        sum.reduce()
        return sum

    def __repr__(self) -> str:
        return f"[{self.left},{self.right}]"


def part_1():
    data = get_question_input(18)
    snailfish_sum = sum(
        (SnailfishNumber.load(snailfish_str) for snailfish_str in data),
        start=SnailfishNumber.load(next(data)),
    )
    print(f"Sum: {snailfish_sum}")
    print(f"Magnitude: {snailfish_sum.magnitude()}")


def part_2():
    data = get_question_input(18)
    snailfish_nums = [SnailfishNumber.load(snailfish_str) for snailfish_str in data]

    largest = namedtuple("Largest", ["magnitude", "left", "right"])
    largest.magnitude = 0
    largest.left = None
    largest.right = None

    for left in snailfish_nums:
        for right in snailfish_nums:
            if left is right:
                continue
            current_magnitude = (left + right).magnitude()
            if current_magnitude > largest.magnitude:
                largest.magnitude = current_magnitude
                largest.left = left
                largest.right = right

    print(f"{largest.left} + {largest.right} = {largest.magnitude}")
