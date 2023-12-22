from __future__ import annotations
from typing import List, Set, Tuple


class Brick:
    def __init__(
        self, min_corner: Tuple[int, int, int], max_corner: Tuple[int, int, int]
    ) -> None:
        self.min_corner = min_corner
        self.max_corner = max_corner
        self.size = tuple([max_corner[i] + 1 - min_corner[i] for i in range(3)])
        self.bricks_above: Set[Brick] = set()
        self.bricks_below: Set[Brick] = set()

    def inside(self, x: int, y: int, z: int) -> bool:
        return (
            (self.min_corner[0] <= x <= self.max_corner[0])
            and (self.min_corner[1] <= y <= self.max_corner[1])
            and (self.min_corner[2] <= z <= self.max_corner[2])
        )

    def fall_one(self) -> None:
        self.min_corner = (
            self.min_corner[0],
            self.min_corner[1],
            self.min_corner[2] - 1,
        )
        self.max_corner = (
            self.max_corner[0],
            self.max_corner[1],
            self.max_corner[2] - 1,
        )


def display(bricks: List[Brick]) -> str:
    x_max, y_max, z_max = 0, 0, 0
    for brick in bricks:
        x_max = max(x_max, brick.max_corner[0])
        y_max = max(y_max, brick.max_corner[1])
        z_max = max(z_max, brick.max_corner[2])
    x_lines = []
    # x_lines.append("{}{}".format(" " * (x_max // 2), "x"))

    y_lines = []
    # y_lines.append("{}{}".format(" " * (y_max // 2), "y"))

    for z in reversed(range(1, z_max + 1)):
        x_line = []
        for x in range(x_max + 1):
            at = []
            for i, brick in enumerate(bricks):
                if brick.inside(x, brick.min_corner[1], z):
                    at.append(i)
            if len(at) == 0:
                x_line.append(".")
            elif len(at) == 1:
                x_line.append(chr(ord("A") + at[0]))
            else:
                x_line.append("?")
        x_lines.append("".join(x_line))

        y_line = []
        for y in range(y_max + 1):
            at = []
            for i, brick in enumerate(bricks):
                if brick.inside(brick.min_corner[0], y, z):
                    at.append(i)
            if len(at) == 0:
                y_line.append(".")
            elif len(at) == 1:
                y_line.append(chr(ord("A") + at[0]))
            else:
                y_line.append("?")
        y_lines.append("".join(y_line))

    x_lines.append("-" * (x_max + 1))
    y_lines.append("-" * (y_max + 1))

    output = []
    for i in range(len(x_lines)):
        output.append("{}    {}".format(x_lines[i], y_lines[i]))

    # return "{}\n{}".format("\n".join(x_lines), "\n".join(y_lines))
    return "\n".join(output)


def is_supporting(above: Brick, below: Brick) -> bool:
    if above == below:
        return False
    if above.min_corner[2] - 1 != below.max_corner[2]:
        return False
    if (
        above.max_corner[0] < below.min_corner[0]
        or below.max_corner[0] < above.min_corner[0]
        or above.max_corner[1] < below.min_corner[1]
        or below.max_corner[1] < above.min_corner[1]
    ):
        return False
    return True


def link_supports(above: Brick, bricks: List[Brick]) -> None:
    for below in bricks:
        if is_supporting(above, below):
            above.bricks_below.add(below)
            below.bricks_above.add(above)


def link_up_all(bricks: List[Brick]) -> None:
    for above in bricks:
        link_supports(above, bricks)


def gravity(bricks: List[Brick]) -> None:
    falling = True
    while falling:
        falling = False
        for brick in bricks:
            if brick.min_corner[2] == 1:  # on ground
                continue
            if len(brick.bricks_below) > 0:  # on brick
                continue
            falling = True
            pulling = [(brick, b) for b in brick.bricks_above]
            brick.fall_one()
            link_supports(brick, bricks)
            while len(pulling) > 0:
                puller, pulled = pulling.pop(0)
                if len(pulled.bricks_below) == 1:
                    pulled.fall_one()
                    link_supports(pulled, bricks)
                    for b in pulled.bricks_above:
                        pulling.append((pulled, b))
                else:
                    pulled.bricks_below.remove(puller)
                    puller.bricks_above.remove(pulled)


def solve(bricks: List[Brick]) -> int:
    def handle_unsupported(brick: Brick, removed: Set[Brick]) -> None:
        if all([b in removed for b in brick.bricks_below]):
            removed.add(brick)
            for b in brick.bricks_above:
                handle_unsupported(b, removed)

    # print(display(bricks))
    link_up_all(bricks)
    gravity(bricks)
    print(" ")
    # print(display(bricks))
    out = 0
    for brick in bricks:
        removed = set()
        removed.add(brick)
        for b in brick.bricks_above:
            # I thought I would need to redo this if changed... but doens't seem that way, curious
            handle_unsupported(b, removed)
        out += len(removed) - 1
    return out


def read(filename: str) -> List[Brick]:
    def parse(text: str) -> Tuple[int, int, int]:
        ta, tb, tc = text.split(",")
        return (int(ta), int(tb), int(tc))

    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        bricks = []
        for row in rows:
            text_left, text_right = row.split("~")
            bricks.append(Brick(parse(text_left), parse(text_right)))
        return bricks


def main(filename: str) -> int:
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
