from libraries.questions import get_answer_module, run_answer
import argparse

parser = argparse.ArgumentParser(description="Run Advent of Code 2021")
parser.add_argument(
    "--day",
    help="The day of code to run; will be prompted if not specified",
    type=int,
    default=None,
)
parser.add_argument(
    "--part",
    help="Which part in the day to run; will be prompted if not specified",
    type=int,
    default=None,
)

args = parser.parse_args()

if __name__ == "__main__":
    day = args.day or input("Enter the day # to run code for: ")
    answer_mod = get_answer_module(day)

    part = args.part or input("Enter the question part # to execute: ")
    run_answer(answer_mod, part)
