from pprint import pprint
from typing import List


def all_zeroes(row):
    return all([r == 0 for r in row])


def extrapolate(row):
    rows = [row]
    while not all_zeroes(rows[-1]):
        rows.append(pairwise_diff(rows[-1]))
    length = len(rows)
    rows[-1].append(0)
    for i in reversed(range(length - 1)):
        rows[i].append(rows[i + 1][-1] + rows[i][-1])
    return rows[0][-1]


def pairwise_diff(row) -> List:
    length = len(row)
    return [row[i + 1] - row[i] for i in range(length - 1)]


def solve(input):
    out = 0
    for row in input:
        out += extrapolate(row)
        # pprint(extrapolate(row))
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            row = row.split(" ")
            # row = map(str.strip, row)
            row = list(map(int, row))

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
