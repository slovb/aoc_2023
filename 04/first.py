def matches(left, right):
    return len([r for r in right if r in left])


def solve(input):
    out = 0
    for id, val in input.items():
        left, right = val
        m = matches(left, right)
        if m > 0:
            out += 2 ** (m - 1)
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = {}
        for row in rows:
            # row = row.split(",")
            # row = map(str.strip, row)
            # row = map(int, row)
            id_part, rest = row.split(":")
            id_part = id_part.split(" ")[-1]
            id = int(id_part)

            left_part, right_part = rest.split("|")
            lefts = []
            rights = []

            for s in left_part.split(" "):
                if s != "":
                    lefts.append(int(s))
            for s in right_part.split(" "):
                if s != "":
                    rights.append(int(s))
            input[id] = (lefts, rights)
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
