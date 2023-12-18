from functools import reduce
from math import gcd
from pprint import pprint


def position_after_dir(x, y, dir, step=1):
    if dir == "U":
        return (x, y - step)
    elif dir == "R":
        return (x + step, y)
    elif dir == "D":
        return (x, y + step)
    elif dir == "L":
        return (x - step, y)
    raise Exception("!!")


def solve(input):
    x, y = 0, 0
    trench = [(x, y)]

    # draw the exterior
    for row in input:
        dir, num = row
        x, y = position_after_dir(x, y, dir, num)
        trench.append((x, y))

    return len(trench)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            _, _, color = row.split(" ")
            color = color[2:-1]
            num = color[:-1]
            num = int("0x" + num, 0)
            dir = color[-1]
            if dir == "0":
                dir = "R"
            elif dir == "1":
                dir = "D"
            elif dir == "2":
                dir = "L"
            elif dir == "3":
                dir = "U"
            input.append((dir, num))
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
