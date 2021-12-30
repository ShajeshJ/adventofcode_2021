from pathlib import Path
from collections.abc import Generator
import sys
from types import ModuleType
import importlib
import inspect
from libraries.print_util import make_red


def get_question_input(day: int) -> Generator[str, None, None]:
    """Get the input data for the given advent `day`"""

    filename = (
        Path(__file__).resolve().parents[1].joinpath(f"data/day{day}.txt").resolve()
    )
    with open(filename) as fp:
        for line in fp:
            yield line.strip()


def get_answer_module(day: int) -> ModuleType:
    try:
        return importlib.import_module(f"solutions.day{day}")
    except ImportError:
        sys.exit(make_red(f"No module `solutions.day{day}.py` found"))


def run_answer(answer_module: ModuleType, part: int):
    funcs = inspect.getmembers(answer_module, inspect.isfunction)

    try:
        target_func = next(f for name, f in funcs if name == f"part_{part}")
    except StopIteration:
        sys.exit(make_red(f"No function `part_{part}` defined in target module"))

    target_func()
