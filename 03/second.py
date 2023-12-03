def solve(input):
    parts, symbols = input
    # print(symbols)
    # print(parts)
    positions_of_parts = {}
    for p, v in parts.items():
        i, j = p
        positions_of_parts[p] = p
        if v >= 10:
            positions_of_parts[(i - 1, j)] = p
        if v >= 100:
            positions_of_parts[(i - 2, j)] = p
    out = 0
    for p in symbols:
        taken = set()
        gearscore = 1
        i, j = p
        for dy in [-1, 0, 1]:
            jdy = j + dy
            for dx in [-1, 0, 1]:
                idx = i + dx
                if (idx, jdy) in positions_of_parts:
                    part_pos = positions_of_parts[(idx, jdy)]
                    if part_pos not in taken:
                        taken.add(part_pos)
                        v = parts[part_pos]
                        gearscore *= v
        if len(taken) == 2:
            out += gearscore
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        parts = {}
        symbols = {}
        for j, row in enumerate(rows):
            n = 0
            for i, c in enumerate(row):
                if c == ".":
                    if n > 0:
                        parts[(i - 1, j)] = n
                        n = 0
                elif c.isdigit():
                    n = n * 10 + int(c)
                else:
                    symbols[(i, j)] = c
                    if n > 0:
                        parts[(i - 1, j)] = n
                        n = 0
            if n > 0:
                parts[(i, j)] = n
        return parts, symbols


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
