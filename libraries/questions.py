from pathlib import Path
from collections.abc import Generator
import sys
from types import ModuleType
import importlib
import inspect
import time
from libraries.print_util import make_gray, make_red


def get_question_input(day: int) -> Generator[str, None, None]:
    """Get the input data for the given advent `day`"""

    filename = (
        Path(__file__).resolve().parents[1].joinpath(f"data/day{day}.txt").resolve()
    )
    with open(filename) as fp:
        for line in fp:
            yield line.strip()


def get_answer_module(day: str) -> ModuleType:
    try:
        return importlib.import_module(f"solutions.day{day}")
    except ImportError:
        sys.exit(make_red(f"No module `solutions.day{day}.py` found"))


def run_answer(answer_module: ModuleType, part: str):
    funcs = inspect.getmembers(answer_module, inspect.isfunction)

    try:
        target_func = next(f for name, f in funcs if name == f"part_{part}")
    except StopIteration:
        sys.exit(make_red(f"No function `part_{part}` defined in target module"))

    print(make_gray("-" * 6 + " SOLUTION OUTPUT " + "-" * 6 + "\033[0m"))

    start = time.perf_counter()
    target_func()
    end = time.perf_counter()

    print(make_gray("-" * 29))
    print(make_gray(f"Execution time: {(end - start)*1000:3f} ms"))
    print(make_gray("-" * 29))
