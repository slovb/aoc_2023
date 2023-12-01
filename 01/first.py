def solve(input):
    out = 0
    for row in input:
        a = 0
        b = 0
        in_number = False
        for c in row:
            if in_number and not c.isdigit():
                break
            elif c.isdigit():
                a = a * 10 + int(c)
                in_number = True
                break
        in_number = False
        n = 1
        for c in row[::-1]:
            if in_number and not c.isdigit():
                break
            elif c.isdigit():
                b = b * n + int(c)
                n *= 10
                in_number = True
                break
        out += 10 * a + b
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            # row = row.split(",")
            # row = map(str.strip, row)
            # row = map(int, row)
            input.append(row)
            # input.append(int(row))
            # input.append(list(row))
        return input


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("\n{}".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
