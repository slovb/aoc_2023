from dataclasses import dataclass
from pprint import pprint


@dataclass
class Direction:
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


def find_dead(length_x, length_y, memory):
    dead = set()
    nodes = []
    for x in range(length_x):
        if (x, 0) not in memory:
            nodes.append((x, 0))
            dead.add((x, 0))
        if (x, length_y - 1) not in memory:
            nodes.append((x, length_y - 1))
            dead.add((x, length_y - 1))
    for y in range(length_y):
        if (0, y) not in memory:
            nodes.append((0, y))
            dead.add((0, y))
        if (length_x - 1, y) not in memory:
            nodes.append((length_x - 1, y))
            dead.add((length_x - 1, y))
    while len(nodes) > 0:
        x, y = nodes.pop(0)
        to_consider = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for node in to_consider:
            x, y = node
            if x < 0 or x >= length_x:
                continue
            if y < 0 or y >= length_y:
                continue
            if (x, y) in memory:
                continue
            if (x, y) in dead:
                continue
            dead.add(node)
            nodes.append(node)
    return dead


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
    dead = find_dead(length_x, length_y, memory)
    # out = length_x * length_y - len(memory) - len(dead)
    # print(length_x * length_y, len(memory), len(dead))
    out = 0
    for y, row in enumerate(input):
        line = []
        for x, c in enumerate(row):
            if (x, y) in dead:
                line.append(" ")
            elif (x, y) in memory:
                line.append(c)
            elif x % 3 == 1 and y % 3 == 1:
                out += 1
                line.append("o")
            else:
                line.append(".")
        print("".join(line))
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            row_0 = []
            row_1 = []
            row_2 = []
            for c in row:
                if c == ".":
                    row_0.append("...")
                    row_1.append("...")
                    row_2.append("...")
                elif c == "-":
                    row_0.append("...")
                    row_1.append("---")
                    row_2.append("...")
                elif c == "|":
                    row_0.append(".|.")
                    row_1.append(".|.")
                    row_2.append(".|.")
                elif c == "L":
                    row_0.append(".|.")
                    row_1.append(".L-")
                    row_2.append("...")
                elif c == "J":
                    row_0.append(".|.")
                    row_1.append("-J.")
                    row_2.append("...")
                elif c == "7":
                    row_0.append("...")
                    row_1.append("-7.")
                    row_2.append(".|.")
                elif c == "F":
                    row_0.append("...")
                    row_1.append(".F-")
                    row_2.append(".|.")
                elif c == "S":
                    row_0.append(".|.")
                    row_1.append("-S-")
                    row_2.append(".|.")
                else:
                    raise SystemError("????")
            input.append("".join(row_0))
            input.append("".join(row_1))
            input.append("".join(row_2))
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
