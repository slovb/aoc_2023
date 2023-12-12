def reformat_group(group):
    options = []
    count = 0
    for c in group:
        if c == "#":
            count += 1
        else:
            if count > 0:
                options.append(count)
                count = 0
            options.append(None)
    if count > 0:
        options.append(count)
    return options


def reformat(record):
    return list(map(reformat_group, record))


def count(groups, check, memory, g_ix, gs_ix, ch_ix):
    # the subindex advancing simplifies end of group situations
    if gs_ix >= len(groups[g_ix]):
        g_ix += 1
        gs_ix = 0
    if (g_ix, gs_ix, ch_ix) in memory:
        return memory[(g_ix, gs_ix, ch_ix)]
    if ch_ix >= len(check):
        target = 0
    else:
        target = check[ch_ix]

    # if we are at the end, have we finished checking?
    if g_ix >= len(groups):
        if target == 0:
            memory[(g_ix, gs_ix, ch_ix)] = 1
            return 1
        memory[(g_ix, gs_ix, ch_ix)] = 0
        return 0

    # solve a bit
    out = 0
    group = groups[g_ix]
    if target > 0:
        length = len(group)
        n = 0
        step = 0
        while n < target and gs_ix + step < length:
            at = group[gs_ix + step]
            n += 1 if at is None else at
            step += 1
        # if the next is a group of # then they need to be added into the whole
        if gs_ix + step < length:
            at = group[gs_ix + step]
            if at is not None:
                n += at
                step += 1

        # sum up solutions
        if n == target:
            # cleared a check
            out += count(groups, check, memory, g_ix, gs_ix + step + 1, ch_ix + 1)

    # try dot if option
    if group[gs_ix] is None:
        out += count(groups, check, memory, g_ix, gs_ix + 1, ch_ix)
    memory[(g_ix, gs_ix, ch_ix)] = out

    return out


def arrangements(record, check):
    groups = reformat(record)
    memory = {}
    c = count(groups, check, memory, 0, 0, 0)
    return c


def solve(input):
    out = []
    for row in input:
        record, check = row
        out.append(arrangements(record, check))
        print(out[-1])
        print("-" * 40)
    return sum(out)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        multiplier = 5
        for row in rows:
            left, right = row.split(" ")
            left = "?".join(multiplier * [left])
            left = left.split(".")
            left = list(filter(lambda x: x != "", left))
            right = tuple(multiplier * list(map(int, right.split(","))))
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
