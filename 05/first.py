def convert(n, ranges):
    for r in ranges:
        a, b, c = r
        if n >= b and n <= b + c:
            return a + n - b
    return n


def solve(input):
    seeds, maps = input
    out = 0
    category = "seed"
    while category in maps:
        category, ranges = maps[category]
        for i in range(len(seeds)):
            seeds[i] = convert(seeds[i], ranges)
    out = min(seeds)
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        seeds = []
        maps = {}
        seeds = [int(s) for s in rows[0].split(":")[1][1:].split(" ")]
        category = None
        collected = []
        for row in rows[2:]:
            if row == "":
                maps[category[0]] = (category[1], collected)
                category = None
                collected = []
            elif row[-1] == ":":
                focus = row.split(" ")[0]
                a, _, b = focus.split("-")
                category = (a, b)
            else:
                collected.append(list(map(int, row.split(" "))))
        maps[category[0]] = (category[1], collected)
        return seeds, maps


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
