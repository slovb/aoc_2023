from pprint import pprint


def groups(arrangement):
    gs = []
    count = 0
    for c in arrangement:
        if c == "#":
            count += 1
        elif count > 0:
            gs.append(count)
            count = 0
    if count > 0:
        gs.append(count)
    return tuple(gs)


def matches(arrangement, check):
    return groups(arrangement) == check


def can_skip(arrangment, check):
    gs = groups(arrangment)
    if gs > check:
        return True
    if len(gs) > len(check):
        return True
    for i in range(len(gs) - 1):
        if gs[i] < check[i]:
            return True
    return False


def search(arrangement, remaining, check):
    if len(remaining) == 0:
        if matches(arrangement, check):
            return 1
        return 0
    if can_skip(arrangement, check):
        return 0
    c = remaining[0]
    if c == "?":
        return search(arrangement + ["."], remaining[1:], check) + search(
            arrangement + ["#"], remaining[1:], check
        )
    return search(arrangement + [c], remaining[1:], check)


def arrangements(record, check):
    return search([], list(record), check)


def solve(input):
    out = 0
    for row in input:
        record, check = row
        out += arrangements(record, check)
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            left, right = row.split(" ")
            right = tuple(map(int, right.split(",")))
            input.append((left, right))
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
