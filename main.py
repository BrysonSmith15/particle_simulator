import math
import os
import random
import time

from typing_extensions import Self

os.system("clear")
debug_lines = 2
size = os.get_terminal_size()
rows = size.lines - 1 - debug_lines
cols = size.columns

color = "\u001b[38;2;255;255;255m"


class Particle:
    def __init__(self, x: float, y: float, vel: tuple[float, float] = (0, 0)):
        self.x = x
        self.y = y
        self.vel = vel
        self.forces = []

    def update(self, dt_s: float, max_row: int = rows, max_col: int = cols):
        # print(f"starting: {(self.y, self.x)}", end=" ")
        if self.x < 2 or self.x > max_col - 1:
            self.forces.append((-self.vel[0], self.vel[1]))
        if self.y < 2 or self.y > max_row - 1:
            self.forces.append((self.vel[0], -self.vel[1]))
        # can make a down force with (0, 10), for example
        out_force = (0, 0)
        for force in self.forces:
            out_force = ((out_force[0] + force[0]), (out_force[1] + force[1]))
        out_force = (out_force[0] / len(self.forces), out_force[1] / len(self.forces))
        self.vel = (self.vel[0] + out_force[0], self.vel[1] + out_force[1])
        self.x += self.vel[0] * dt_s
        self.y += self.vel[1] * dt_s
        if self.x > max_col:
            self.x = max_col
        elif self.x < 0:
            self.x = 0
        if self.y > max_row:
            self.y = max_row
        elif self.y < 0:
            self.y = 0
        self.forces = []
        # print(f"ending: {(self.y, self.x)}")
        # print(f"vel: {self.vel}")

    def get_x(self) -> int:
        return int(self.x)

    def get_y(self) -> int:
        return int(self.y)

    def collide_with(self, other: Self) -> None:
        if math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2) <= 3:
            self.forces.append((-other.vel[0], -other.vel[1]))
            other.forces.append((-self.vel[0], -self.vel[1]))

    def __repr__(self) -> str:
        return f"Particle @ ({self.y}, {self.x}) going {self.vel}"

    def __str__(self) -> str:
        return self.color_from_vel() + "*"

    def color_from_vel(self) -> str:
        start = "\u001b[38;2;"
        vel_mag = math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
        if vel_mag > 10:
            return start + "255;0;0m"
        elif vel_mag > 5:
            return start + "150;150;0m"
        elif vel_mag > 3:
            return start + "50;200;0m"
        elif vel_mag > 1.5:
            return start + "0;255;0m"
        elif vel_mag > 1:
            return start + "0;150;150m"
        else:
            return start + "0;0;255m"


def print_bools_2d(bools_2d: list[list[bool | Particle | None]]) -> None:
    out = color + "+" + "-" * len(bools_2d[0]) + "+"
    for idx, row in enumerate(bools_2d):
        out += color + "\n|"
        for idx2, col in enumerate(row):
            if col:
                out += str(col)
            else:
                out += f"{color} "
            # out += str(col) if col else " "
            # out += "*" if col else " "
        out += color + "|"
    out += color + "+" + "-" * len(bools_2d[-1]) + "+"
    print(out)


def get_vel_sum(particles: list[Particle]) -> float:
    out = 0.0
    for particle in particles:
        out += math.sqrt(particle.vel[0] ** 2 + particle.vel[1] ** 2)
    return out


board = [
    [
        (
            Particle(
                col,
                row,
                ((random.random() - 0.5) * 1000, (random.random() - 0.5) * 1000),
            )
            if random.random() > 0.9
            else None
        )
        for col in range(cols - 2)
    ]
    for row in range(rows - 2)
]

print_bools_2d(board)
prev = time.perf_counter()

parts = []
for row in board:
    for col in row:
        if col:
            parts.append(col)
while True:
    try:
        for part in parts:
            for part2 in parts:
                part.collide_with(part2)
        board = [[None for _col in range(cols - 2)] for _row in range(rows - 2)]
        for part in parts:
            part.update(
                time.perf_counter() - prev,
                max_row=len(board) - 1,
                max_col=len(board[0]) - 1,
            )
            try:
                board[part.get_y()][part.get_x()] = part
            except IndexError as ex:
                print(f"Row: {part.get_y()}, Col: {part.get_x()}")
                raise ex

        os.system("clear")
        print_bools_2d(board)
        # print(parts[0])
        # for part in parts:
        #     print(part)
        count = 0
        for row in board:
            for col in row:
                if col:
                    count += 1
        print(f"Total Particles: {len(parts)}, using {count} spaces")
        print(f"Sum of Velocities: {get_vel_sum(parts)}")
        # time.sleep(0.05)
        prev = time.perf_counter()
    except KeyboardInterrupt:
        print()
        exit(0)

    # except IndexError:
