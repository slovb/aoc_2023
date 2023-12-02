def maxes(game):
    r = g = b = 0
    for subset in game:
        for count, color in subset:
            if color == "red":
                r = max(r, count)
            elif color == "green":
                g = max(g, count)
            elif color == "blue":
                b = max(b, count)
            else:
                raise SystemError("COLOR")
    return (r, g, b)


def solve(input):
    out = 0
    for id, row in input.items():
        needed = maxes(row)
        pow = needed[0] * needed[1] * needed[2]
        print(id, needed, pow)
        out += pow
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = {}
        for id, row in enumerate(rows):
            row = row.split(":")[1][1:]
            row = row.split(";")
            out = []
            for subset in row:
                pairs = []
                for pair in subset.split(","):
                    pair = pair.strip()
                    l, r = pair.split(" ")
                    pairs.append((int(l), r))
                out.append(pairs)
            # row = map(str.strip, row)
            # row = map(int, row)

            input[id + 1] = out
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
