from __future__ import annotations
from functools import reduce
from typing import Literal
from libraries.questions import get_question_input


class Packet:
    version: int
    type: int
    plen_type: Literal["packet_len", "num_packets"]
    plen: int
    value: int | list[Packet]

    def parse_version(self, bin_str: str):
        """Parses and saves `version` from the start of `bin_str`,
        and returns the same `bin_str` without the version
        """
        self.version = int(bin_str[:3], 2)
        return bin_str[3:]

    def parse_type(self, bin_str: str):
        """Parses and saves `type` from the start of `bin_str`,
        and returns the same `bin_str` without the type
        """
        self.type = int(bin_str[:3], 2)
        return bin_str[3:]

    def parse_literal(self, bin_str: str):
        """Parses and saves a literal from the start of `bin_str`
        into `value`, and returns the same `bin_str` without the
        literal
        """
        literal = ""  # Wil contain the literal in binary

        while True:
            is_last = bin_str[0] == "0"
            literal += bin_str[1:5]
            bin_str = bin_str[5:]

            if is_last:
                break

        self.value = int(literal, 2)
        return bin_str

    def parse_packet_len(self, bin_str: str):
        """Parses and saves the packet length type, and the
        packet length value from the start of `bin_str`. Returns
        the same `bin_str` without these two values
        """
        if bin_str[0] == "0":
            self.plen_type = "packet_len"
            self.plen = int(bin_str[1:16], 2)
            bin_str = bin_str[16:]
        else:
            self.plen_type = "num_packets"
            self.plen = int(bin_str[1:12], 2)
            bin_str = bin_str[12:]
        return bin_str


def _build_packet(bin_str: str):
    """Given a `bin_str`, this function will build
    packets, recursively as needed. It will return
    the created Packet, as well as any remaining
    `bin_str` leftover.
    """
    packet = Packet()
    bin_str = packet.parse_version(bin_str)
    bin_str = packet.parse_type(bin_str)

    if packet.type == 4:
        bin_str = packet.parse_literal(bin_str)
    else:
        bin_str = packet.parse_packet_len(bin_str)
        packet.value = []

        if packet.plen_type == "packet_len":
            bits_remaining = packet.plen
            while bits_remaining > 0:
                next_p, leftover_bstr = _build_packet(bin_str)
                packet.value.append(next_p)
                bits_remaining -= len(bin_str) - len(leftover_bstr)
                bin_str = leftover_bstr

        elif packet.plen_type == "num_packets":
            for _ in range(packet.plen):
                next_p, bin_str = _build_packet(bin_str)
                packet.value.append(next_p)

    return packet, bin_str


def _sum_version(packet: Packet) -> int:
    """Given a packet, will return the sum of the versions for this packet
    and any nested packets recursively.
    """
    if isinstance(packet.value, int):
        # This is a literal packet, so there are no nested packets
        return packet.version
    else:
        # This is an operator packet, so sum the nested versions
        return sum(_sum_version(p) for p in packet.value) + packet.version


def _parse_bstr(hex_str: str):
    """Converts `hex_str` to the corresponding binary string, ensuring
    0s are padded appropriately to match the length of `hex_str`"""
    # Explaination of this code:
    # 1. Convert hex_str to an integer
    # 2. Use `bin` to convert integer into a raw binary string
    # 3. Remove the leading `0b` on the raw binary string
    # 4. Use `zfill` to pad leading 0s to align the binary string
    #    to the hexstring
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str * 4))


def part_1():
    hex_str = next(get_question_input(16))
    bin_str = _parse_bstr(hex_str)
    packet, _ = _build_packet(bin_str)
    print(_sum_version(packet))


def _evaluate_packet(packet: Packet) -> int:
    """Returns the evaluated result of this packet"""
    if packet.type == 4:
        # Literal packet
        return packet.value

    # All other types are operators which use evaluated sub-packet values
    sub_packet_values = [_evaluate_packet(p) for p in packet.value]

    if packet.type == 0:
        # Sum packet
        return sum(sub_packet_values)
    elif packet.type == 1:
        # Product packet
        return reduce(lambda x, y: x * y, sub_packet_values, 1)
    elif packet.type == 2:
        # Minimum packet
        return min(sub_packet_values)
    elif packet.type == 3:
        # Maximum packet
        return max(sub_packet_values)
    elif packet.type == 5:
        # Greater than packet
        p1, p2 = sub_packet_values
        return 1 if p1 > p2 else 0
    elif packet.type == 6:
        # Less than packet
        p1, p2 = sub_packet_values
        return 1 if p1 < p2 else 0
    elif packet.type == 7:
        # Equal to packet
        p1, p2 = sub_packet_values
        return 1 if p1 == p2 else 0


def part_2():
    hex_str = next(get_question_input(16))
    bin_str = _parse_bstr(hex_str)
    packet, _ = _build_packet(bin_str)
    print(_evaluate_packet(packet))
