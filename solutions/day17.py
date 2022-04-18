from dataclasses import dataclass
from typing import NamedTuple
from libraries.questions import get_question_input


def part_1():
    data = next(get_question_input(17))
    y_data = data.split()[-1]
    y_min, _ = (int(n) for n in y_data.replace("y=", "").split(".."))
    print(-y_min * (-y_min - 1) / 2)


class XY(NamedTuple):
    x: int
    y: int


@dataclass
class SimulationContext:
    position: XY
    velocity: XY
    target_area: tuple[XY, XY]


def move_probe(ctx: SimulationContext) -> SimulationContext:
    """Moves the probe to the next position using the current x,y `position` and `velocity`"""
    ctx.position = XY(
        ctx.position[0] + ctx.velocity[0],
        ctx.position[1] + ctx.velocity[1],
    )
    return ctx


def apply_drag(ctx: SimulationContext) -> SimulationContext:
    """Returns the new x,y velocity after drag for is applied for one step"""
    x, y = ctx.velocity
    y_drag = -1

    if x == 0:
        ctx.velocity = XY(0, y + y_drag)
    else:
        x_drag = -x // abs(x)  # normalized x vector in the opposite direction
        ctx.velocity = XY(x + x_drag, y + y_drag)

    return ctx


def in_target_area(ctx: SimulationContext) -> bool:
    """Returns a boolean indicating if the simulated position is in the target area"""
    x_min, y_min = ctx.target_area[0]
    x_max, y_max = ctx.target_area[1]

    return x_min <= ctx.position.x <= x_max and y_min <= ctx.position.y <= y_max


def is_simulation_done(ctx: SimulationContext) -> bool:
    """Returns a boolean indicating if the simulation is complete."""
    if in_target_area(ctx):
        # If we hit the target area, then there's no need to continue simulation
        return True

    # Match on cases where simulation has no chance to enter the target area from
    match ctx:
        case SimulationContext(
            position=XY(x=x_pos),
            velocity=XY(x=0),
            target_area=(XY(x=x_min), XY(x=x_max))
        ) if x_pos < x_min or x_pos > x_max:
            # No more horizontal velocity, but we're still not in target area's x range
            return True
        case SimulationContext(
            position=XY(y=y_pos),
            velocity=XY(y=y_vel),
            target_area=(XY(y=y_min), _),
        ) if y_vel < 0 and y_pos < y_min:
            # Went below the lowest y while the travelling downwards
            return True
        case SimulationContext(
            position=XY(x=x_pos),
            velocity=XY(x=x_vel),
            target_area=(XY(x=x_min), XY(x=x_max)),
        ) if (x_vel > 0 and x_pos > x_max) or (x_vel < 0 and x_pos < x_min):
            # Went past the furthest x-boundary in the direction of horizontal travel
            return True
        case _:
            # Otherwise we can still potentially reach the target area, so keep simulating
            return False


def lands_in_target_area(velocity: XY, target_area: tuple[XY, XY]) -> bool:
    """Simulates a launch given a `target_area` with the starting
    `velocity`. Returns a boolean indicating whether or not the launched probe will
    land within the target range.
    """
    ctx = SimulationContext(XY(0, 0), velocity, target_area)

    while not is_simulation_done(ctx):
        ctx = apply_drag(move_probe(ctx))

    return in_target_area(ctx)


def part_2():
    data = next(get_question_input(17))

    # Parse string data
    *_, x_data, y_data = data.split()
    x_data = x_data[:-1].replace("x=", "")
    y_data = y_data.replace("y=", "")

    x_min, x_max = (int(n) for n in x_data.split(".."))
    y_min, y_max = (int(n) for n in y_data.split(".."))

    # Figure out range of velocities to scan through
    if x_min >= 0:
        x_start, x_end = 0, x_max+1
    elif x_max <= 0:
        x_start, x_end = x_min, 0+1
    else:
        x_start, x_end = x_min, x_max+1

    if y_min == 0 or y_max == 0 or y_min < 0 < y_max:
        print("infinitely many possibilities")
        return
    elif y_min > 0:
        y_start, y_end = 0, y_max+1
    else:
        y_start, y_end = y_min, -y_min+1

    # Find viable velocities within bounded range
    target_area = (XY(x_min, y_min), XY(x_max, y_max))
    num_solutions = sum(
        1
        for x_vel in range(x_start, x_end)
        for y_vel in range(y_start, y_end)
        if lands_in_target_area(
            velocity=XY(x_vel, y_vel),
            target_area=target_area,
        )
    )

    print(num_solutions)


"""
Quick and dirty unit tests
"""

# in range
assert is_simulation_done(SimulationContext(
    position=XY(3, 3),
    velocity=XY(2, 2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is True
assert is_simulation_done(SimulationContext(
    position=XY(-1, -1),
    velocity=XY(2, 2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False

# stagnated
assert is_simulation_done(SimulationContext(
    position=XY(-1, 8),
    velocity=XY(0, 2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is True
assert is_simulation_done(SimulationContext(
    position=XY(3, 8),
    velocity=XY(0, 2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False
assert is_simulation_done(SimulationContext(
    position=XY(-1, 8),
    velocity=XY(2, 0),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False

# past lower y
assert is_simulation_done(SimulationContext(
    position=XY(-1, -1),
    velocity=XY(2, -2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is True
assert is_simulation_done(SimulationContext(
    position=XY(-1, 1),
    velocity=XY(2, -2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False
assert is_simulation_done(SimulationContext(
    position=XY(-1, -1),
    velocity=XY(2, 2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False
assert is_simulation_done(SimulationContext(
    position=XY(-1, 8),
    velocity=XY(2, 2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False

# going right past right x
assert is_simulation_done(SimulationContext(
    position=XY(8, 3),
    velocity=XY(2, -2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is True
assert is_simulation_done(SimulationContext(
    position=XY(3, 8),
    velocity=XY(2, -2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False
assert is_simulation_done(SimulationContext(
    position=XY(-1, 8),
    velocity=XY(2, -2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False

# going left past left x
assert is_simulation_done(SimulationContext(
    position=XY(-1, 3),
    velocity=XY(-2, -2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is True
assert is_simulation_done(SimulationContext(
    position=XY(3, 8),
    velocity=XY(-2, -2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False
assert is_simulation_done(SimulationContext(
    position=XY(8, 8),
    velocity=XY(-2, -2),
    target_area=(XY(0, 0), XY(5, 5)),
)) is False
