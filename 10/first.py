from dataclasses import dataclass
from pprint import pprint


@dataclass
class Direction:
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


def solve(input):
    length_x = len(input[0])
    length_y = len(input)
    memory = {}
    nodes = []
    for y, row in enumerate(input):
        if len(nodes) > 0:
            break
        for x, c in enumerate(row):
            if c == "S":
                nodes.append((x, y, 0, None))
    while len(nodes) > 0:
        x, y, cost, direction = nodes.pop(0)
        if y < 0 or y >= length_y:
            continue
        if x < 0 or x >= length_x:
            continue
        c = input[y][x]
        if c == ".":
            continue
        if (x, y) in memory and memory[(x, y)] <= cost:
            continue
        if c == "|":
            if direction == Direction.NORTH:
                nodes.append((x, y - 1, cost + 1, Direction.NORTH))
            elif direction == Direction.SOUTH:
                nodes.append((x, y + 1, cost + 1, Direction.SOUTH))
            else:
                continue
        elif c == "-":
            if direction == Direction.WEST:
                nodes.append((x - 1, y, cost + 1, Direction.WEST))
            elif direction == Direction.EAST:
                nodes.append((x + 1, y, cost + 1, Direction.EAST))
            else:
                continue
        elif c == "L":
            if direction == Direction.SOUTH:
                nodes.append((x + 1, y, cost + 1, Direction.EAST))
            elif direction == Direction.WEST:
                nodes.append((x, y - 1, cost + 1, Direction.NORTH))
            else:
                continue
        elif c == "J":
            if direction == Direction.SOUTH:
                nodes.append((x - 1, y, cost + 1, Direction.WEST))
            elif direction == Direction.EAST:
                nodes.append((x, y - 1, cost + 1, Direction.NORTH))
            else:
                continue
        elif c == "7":
            if direction == Direction.NORTH:
                nodes.append((x - 1, y, cost + 1, Direction.WEST))
            elif direction == Direction.EAST:
                nodes.append((x, y + 1, cost + 1, Direction.SOUTH))
            else:
                continue
        elif c == "F":
            if direction == Direction.NORTH:
                nodes.append((x + 1, y, cost + 1, Direction.EAST))
            elif direction == Direction.WEST:
                nodes.append((x, y + 1, cost + 1, Direction.SOUTH))
            else:
                continue
        elif c == "S":
            if direction == None:
                nodes.append((x - 1, y, cost + 1, Direction.WEST))
                nodes.append((x + 1, y, cost + 1, Direction.EAST))
                nodes.append((x, y - 1, cost + 1, Direction.NORTH))
                nodes.append((x, y + 1, cost + 1, Direction.SOUTH))
            else:
                continue
        else:
            raise SystemError("???")
        memory[(x, y)] = cost
    for y, row in enumerate(input):
        line = []
        for x, c in enumerate(row):
            if (x, y) in memory:
                line.append(str(memory[(x, y)]))
            else:
                line.append(c)
        print("".join(line))
    out = max(memory.values())
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
