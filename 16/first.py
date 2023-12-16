from dataclasses import dataclass
from pprint import pprint


@dataclass
class Direction:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def step(x, y, dir):
    if dir == Direction.NORTH:
        return (x, y - 1, dir)
    elif dir == Direction.EAST:
        return (x + 1, y, dir)
    elif dir == Direction.SOUTH:
        return (x, y + 1, dir)
    elif dir == Direction.WEST:
        return (x - 1, y, dir)
    raise Exception("!!!")


def solve(input):
    out = 0
    memory = set()
    energized = set()
    length_x = len(input[0])
    length_y = len(input)
    lasers = [(0, 0, Direction.EAST)]
    while len(lasers) > 0:
        pews = []
        for laser in lasers:
            if laser in memory:
                continue
            x, y, dir = laser
            if x < 0 or x >= length_x:
                continue
            if y < 0 or y >= length_y:
                continue
            memory.add(laser)
            energized.add((x, y))

            at = input[y][x]
            if at == ".":
                pews.append(step(x, y, dir))
            elif at == "/":
                if dir == Direction.NORTH:
                    dir = Direction.EAST
                elif dir == Direction.EAST:
                    dir = Direction.NORTH
                elif dir == Direction.SOUTH:
                    dir = Direction.WEST
                else:
                    dir = Direction.SOUTH
                pews.append(step(x, y, dir))
            elif at == "\\":
                if dir == Direction.NORTH:
                    dir = Direction.WEST
                elif dir == Direction.WEST:
                    dir = Direction.NORTH
                elif dir == Direction.SOUTH:
                    dir = Direction.EAST
                else:
                    dir = Direction.SOUTH
                pews.append(step(x, y, dir))
            elif at == "|":
                if dir == Direction.NORTH or dir == Direction.SOUTH:
                    pews.append(step(x, y, dir))
                else:
                    pews.append(step(x, y, Direction.NORTH))
                    pews.append(step(x, y, Direction.SOUTH))
            elif at == "-":
                if dir == Direction.EAST or dir == Direction.WEST:
                    pews.append(step(x, y, dir))
                else:
                    pews.append(step(x, y, Direction.EAST))
                    pews.append(step(x, y, Direction.WEST))
            else:
                raise Exception("!!")
        lasers = pews
    out = len(energized)
    lines = []
    for y in range(length_y):
        line = []
        for x in range(length_x):
            if (x, y, Direction.EAST) in memory:
                line.append(">")
                # line.append("#")
            elif (x, y, Direction.SOUTH) in memory:
                line.append("V")
                # line.append("#")
            elif (x, y, Direction.WEST) in memory:
                line.append("<")
                # line.append("#")
            elif (x, y, Direction.NORTH) in memory:
                line.append("^")
                # line.append("#")
            else:
                line.append(input[y][x])
        lines.append("".join(line))
    print("\n".join(lines))
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            # row = row.split(",")
            # row = map(str.strip, row)
            # row = map(int, row)

            input.append(row)
            # input.append(int(row))
            # input.append(list(row))
        return input


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
