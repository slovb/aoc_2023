from pprint import pprint


def hash(text):
    out = 0
    for c in text:
        out += ord(c)
        out *= 17
        out %= 256
    return out


def solve(input):
    out = 0
    for step in input:
        out += hash(step)
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            row = row.split(",")
            for step in row:
                input.append(step)
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
