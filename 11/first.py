from pprint import pprint


def expand(galaxies, empty_cols, empty_rows):
    out = []
    for galaxy in galaxies:
        x, y = galaxy
        x += len([i for i in range(x) if i in empty_cols])
        y += len([i for i in range(y) if i in empty_rows])
        out.append((x, y))
    return out


def diff(g1, g2):
    x1, y1 = g1
    x2, y2 = g2
    return abs(x1 - x2) + abs(y1 - y2)


def solve(input):
    galaxies, empty_cols, empty_rows = input
    galaxies = expand(galaxies, empty_cols, empty_rows)
    out = 0
    for i, g1 in enumerate(galaxies[:-1]):
        for g2 in galaxies[i + 1 :]:
            out += diff(g1, g2)
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        empty_cols = set([i for i in range(len(rows))])
        empty_rows = set([i for i in range(len(rows[0]))])
        galaxies = []
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == "#":
                    empty_cols.discard(x)
                    empty_rows.discard(y)
                    galaxies.append((x, y))
        return galaxies, empty_cols, empty_rows


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
