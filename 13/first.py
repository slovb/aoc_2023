from pprint import pprint


def has_vertical(pattern, xref, xmax):
    # xref 1 means before 1
    for x, y in pattern:
        x = 2 * xref - 1 - x
        if x < 0 or x > xmax:
            continue
        if (x, y) not in pattern:
            return False
    return True


def has_horizontal(pattern, yref, ymax):
    # yref 1 means before 1
    for x, y in pattern:
        y = 2 * yref - 1 - y
        if y < 0 or y > ymax:
            continue
        if (x, y) not in pattern:
            return False
    return True


def solve(input):
    out = 0
    for xmax, ymax, pattern in input:
        print("-" * 40)
        for y in range(1, ymax + 1):
            if has_horizontal(pattern, y, ymax):
                print("y", y)
                out += 100 * y
                break
        for x in range(1, xmax + 1):
            if has_vertical(pattern, x, xmax):
                print("x", x)
                out += x
                break
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        pattern = []
        ybase = 0
        xmax = 0
        ymax = 0
        for y, row in enumerate(rows):
            if row == "":
                input.append((xmax, ymax, pattern))
                pattern = []
                ybase = y + 1
                xmax = 0
                ymax = 0
            else:
                ymax = max(ymax, y - ybase)
            for x, c in enumerate(row):
                xmax = max(xmax, x)
                if c == "#":
                    pattern.append((x, y - ybase))
        if len(pattern) > 0:
            input.append((xmax, ymax, pattern))
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
