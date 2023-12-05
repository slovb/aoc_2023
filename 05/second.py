def convert(start, stop, ranges):
    mapped = []
    unmapped = [(start, stop)]
    for range_ in ranges:
        destination, source, length = range_
        source_start = source
        source_stop = source + length - 1
        new_unmapped = []
        for u_start, u_stop in unmapped:
            if u_start <= source_stop and source_start <= u_stop:
                # intersection!
                if u_start < source_start:
                    new_unmapped.append((u_start, source_start - 1))
                    u_start = source_start
                if u_stop > source_stop:
                    new_unmapped.append((source_stop + 1, u_stop))
                    u_stop = source_stop
                adjustment = u_start - source_start
                difference = u_stop - u_start
                mapped.append(
                    (destination + adjustment, destination + adjustment + difference)
                )
            else:
                new_unmapped.append((u_start, u_stop))
        unmapped = new_unmapped
    return mapped + unmapped


def reformat(seeds):
    new_seeds = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        stop = start + seeds[i + 1] - 1
        new_seeds.append((start, stop))
    return new_seeds


def solve(input):
    seeds, maps = input
    seeds = reformat(seeds)
    out = 0
    category = "seed"
    while category in maps:
        print(category)
        category, ranges = maps[category]
        new_seeds = []
        for i in range(len(seeds)):
            start, stop = seeds[i]
            for seed in convert(start, stop, ranges):
                new_seeds.append(seed)
        seeds = new_seeds
    out = min(seeds)[0]
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
