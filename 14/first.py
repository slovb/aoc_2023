from pprint import pprint


def tilt_north(squares, rounds, x_max, y_max):
    old_rocks = [rock for rock in rounds]
    changes = True
    while changes:
        changes = False
        new_rocks = []
        for x, y in old_rocks:
            if y > 0 and (x, y - 1) not in squares and (x, y - 1) not in old_rocks:
                new_rocks.append((x, y - 1))
                changes = True
            else:
                new_rocks.append((x, y))
        old_rocks = new_rocks
    return old_rocks


def display(squares, rounds, x_max, y_max):
    rows = []
    for y in range(y_max + 1):
        row = []
        for x in range(x_max + 1):
            if (x, y) in squares:
                row.append("#")
            elif (x, y) in rounds:
                row.append("O")
            else:
                row.append(".")
        rows.append("".join(row))
    return "\n".join(rows)


def score(rounds, y_max):
    out = 0
    for _, y in rounds:
        out += 1 + y_max - y
    return out


def solve(input):
    squares, rounds, x_max, y_max = input
    squares = set(squares)
    rounds = tilt_north(squares, rounds, x_max, y_max)
    print(display(squares, rounds, x_max, y_max))
    return score(rounds, y_max)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        rounds = []
        squares = []
        x_max = 0
        y_max = 0
        for y, row in enumerate(rows):
            y_max = max(y_max, y)
            for x, c in enumerate(row):
                x_max = max(x_max, x)
                if c == "#":
                    squares.append((x, y))
                elif c == "O":
                    rounds.append((x, y))
        return squares, rounds, x_max, y_max


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
