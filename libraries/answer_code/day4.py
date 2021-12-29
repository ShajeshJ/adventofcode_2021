from __future__ import annotations
import sys
from libraries.print_util import make_red, make_bold
from libraries.questions import get_question_input


class BingoBoard:
    def __init__(self) -> None:
        self.board_state: list[int] = []
        self.marked_state: list[bool] = []

    def is_invalid(self) -> bool:
        """Determine if the created board is valid"""
        return len(self.board_state) != 25

    def reset(self):
        """Reset the marked state of the board"""
        self.marked_state = [False] * 25

    def get_unmarked_sum(self) -> int:
        """Returns the sum of all unmarked numbers on the board"""
        return sum(
            n
            for n, is_marked in zip(self.board_state, self.marked_state)
            if not is_marked
        )

    def has_win(self) -> bool:
        """Returns a boolean indicating if there is a winning
        horizontal/vertical match on the board.
        """
        is_winner = False

        # Check horizontals
        for i in range(0, 25, 5):
            if all(self.marked_state[i + j] for j in range(5)):
                is_winner = True
                break

        # Check verticals
        for i in range(5):
            if all(self.marked_state[i + j] for j in range(0, 25, 5)):
                is_winner = True
                break

        return is_winner

    def input_draw(self, draw: int):
        """Marks off the next draw value on the board if found"""
        try:
            found_index = self.board_state.index(draw)
        except ValueError:
            return

        self.marked_state[found_index] = True

    @classmethod
    def from_file_data(cls, file_lines: list[str]) -> BingoBoard:
        """Create a bingo board using data from files (expects 5 lines with 5 numbers)"""
        obj = cls()
        for line in file_lines:
            obj.board_state.extend(int(n) for n in line.split(" ") if n)

        if obj.is_invalid():
            sys.exit(make_red(f"Invalid bingo board data:\n{file_lines}"))

        obj.reset()

        return obj

    def __repr__(self) -> str:
        if self.is_invalid():
            return f"Invalid board: {self.board_state}"

        text = "-" * 5 + "BINGO BOARD" + "-" * 6 + "\n"
        for i in range(0, 25, 5):
            for j in range(5):
                entry = f"{self.board_state[i + j]:2}"
                if self.marked_state[i + j]:
                    entry = make_bold(entry)
                text += f"{entry} | "
            text = text[:-3] + "\n"
        text += "-" * 22
        return text


def part_1():
    inputs = get_question_input(4)
    draw_order = [int(d) for d in next(inputs).split(",")]

    boards: list[BingoBoard] = []

    while next(inputs, None) is not None:  # Skip empty lines separating boards
        boards.append(BingoBoard.from_file_data([next(inputs) for _ in range(5)]))

    winning_board = None
    winning_draw = None

    # Cannot win with <5 draws, so input the first draws 4 blind
    for draw in draw_order[:4]:
        for board in boards:
            board.input_draw(draw)
    draw_order = draw_order[4:]

    for next_draw in draw_order:
        for board in boards:
            board.input_draw(next_draw)

            if board.has_win():
                winning_board = board
                break

        if winning_board:
            winning_draw = next_draw
            break  # Can stop drawing once someone has one

    print(winning_board)
    if winning_board is None:
        print(winning_draw)
        sys.exit(make_red("Didn't find a winning board"))

    print(f"Score: {winning_board.get_unmarked_sum() * winning_draw}")


def part_2():
    inputs = get_question_input(4)
    draw_order = [int(d) for d in next(inputs).split(",")]

    boards: list[BingoBoard] = []

    while next(inputs, None) is not None:  # Skip empty lines separating boards
        boards.append(BingoBoard.from_file_data([next(inputs) for _ in range(5)]))

    final_board = None
    final_draw = None

    # Cannot win with <5 draws, so input the first draws 4 blind
    for draw in draw_order[:4]:
        for board in boards:
            board.input_draw(draw)
    draw_order = draw_order[4:]

    for next_draw in draw_order:
        remaining_boards = []

        for board in boards:
            board.input_draw(next_draw)

            if board.has_win():
                final_board = board  # `final_board` keeps updating until last one wins
            else:
                remaining_boards.append(board)

        if not remaining_boards:
            final_draw = next_draw
            break  # All boards have won; can stop drawing

        boards = remaining_boards  # Otherwise, transfer remaining boards to continue checking

    print(final_board)
    if final_draw is None:
        print(final_draw)
        sys.exit(make_red("Still some boards remainining..."))

    print(f"Score: {final_board.get_unmarked_sum() * final_draw}")
