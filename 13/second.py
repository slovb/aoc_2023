from pprint import pprint


def has_vertical(pattern, xref, xmax, smudge):
    # xref 1 means before 1
    smudge_in_pattern = smudge in pattern
    for x, y in pattern:
        if smudge_in_pattern and (x, y) == smudge:
            continue
        x = 2 * xref - 1 - x
        if x < 0 or x > xmax:
            continue
        if (x, y) not in pattern or (smudge_in_pattern and (x, y) == smudge):
            return False
    if not smudge_in_pattern:
        x, y = smudge
        x = 2 * xref - 1 - x
        if x < 0 or x > xmax:
            pass
        elif (x, y) not in pattern:
            return False
    return True


def has_horizontal(pattern, yref, ymax, smudge):
    # yref 1 means before 1
    smudge_in_pattern = smudge in pattern
    for x, y in pattern:
        if smudge_in_pattern and (x, y) == smudge:
            continue
        y = 2 * yref - 1 - y
        if y < 0 or y > ymax:
            continue
        if (x, y) not in pattern or (smudge_in_pattern and (x, y) == smudge):
            return False
    if not smudge_in_pattern:
        x, y = smudge
        y = 2 * yref - 1 - y
        if y < 0 or y > ymax:
            pass
        elif (x, y) not in pattern:
            return False
    return True


def search(xmax, ymax, pattern):
    counts = {}
    for xs in range(xmax + 1):
        for ys in range(ymax + 1):
            smudge = (xs, ys)
            for y in range(1, ymax + 1):
                if has_horizontal(pattern, y, ymax, smudge):
                    # print(smudge, "y", y)
                    if 100 * y not in counts:
                        counts[100 * y] = 0
                    counts[100 * y] += 1
            for x in range(1, xmax + 1):
                if has_vertical(pattern, x, xmax, smudge):
                    # print(smudge, "x", x)
                    if x not in counts:
                        counts[x] = 0
                    counts[x] += 1
    for key, value in counts.items():
        if value == 1:
            print(key)
            return key


def solve(input):
    out = 0
    for xmax, ymax, pattern in input:
        print("-" * 40)
        out += search(xmax, ymax, pattern)
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
