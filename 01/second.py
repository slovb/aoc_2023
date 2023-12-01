def solve(input):
    out = 0
    for row in input:
        a = row[0]
        b = row[-1]
        out += 10 * a + b
        # print(a, b, 10 * a + b)
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        numbers = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
        for row in rows:
            # row = row.split(",")
            # row = map(str.strip, row)
            # row = map(int, row)
            digits = []
            for i, c in enumerate(row):
                if c.isdigit():
                    digits.append(int(c))
                for n, name in enumerate(numbers):
                    if row[i + 1 - len(name) : i + 1] == name:
                        digits.append(n + 1)
            input.append(digits)
            # input.append(row)
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
            print("{}:\n{}\n".format(f, main(f)))
