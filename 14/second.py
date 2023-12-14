def tilt_north(stops, rocks, x_max, y_max):
    for x in range(x_max + 1):
        move_to = None
        for y in range(y_max + 1):
            if (x, y) in stops:
                move_to = None
            elif (x, y) in rocks:
                if move_to is not None:
                    i = rocks.index((x, y))
                    rocks[i] = move_to
                    move_to = (move_to[0], move_to[1] + 1)
            elif move_to is None:
                move_to = (x, y)


def tilt_west(stops, rocks, x_max, y_max):
    for y in range(y_max + 1):
        move_to = None
        for x in range(x_max + 1):
            if (x, y) in stops:
                move_to = None
            elif (x, y) in rocks:
                if move_to is not None:
                    i = rocks.index((x, y))
                    rocks[i] = move_to
                    move_to = (move_to[0] + 1, move_to[1])
            elif move_to is None:
                move_to = (x, y)


def tilt_south(stops, rocks, x_max, y_max):
    for x in range(x_max + 1):
        move_to = None
        for y in reversed(range(y_max + 1)):
            if (x, y) in stops:
                move_to = None
            elif (x, y) in rocks:
                if move_to is not None:
                    i = rocks.index((x, y))
                    rocks[i] = move_to
                    move_to = (move_to[0], move_to[1] - 1)
            elif move_to is None:
                move_to = (x, y)


def tilt_east(stops, rocks, x_max, y_max):
    for y in range(y_max + 1):
        move_to = None
        for x in reversed(range(x_max + 1)):
            if (x, y) in stops:
                move_to = None
            elif (x, y) in rocks:
                if move_to is not None:
                    i = rocks.index((x, y))
                    rocks[i] = move_to
                    move_to = (move_to[0] - 1, move_to[1])
            elif move_to is None:
                move_to = (x, y)


def display(stops, rocks, x_max, y_max):
    rows = []
    for y in range(y_max + 1):
        row = []
        for x in range(x_max + 1):
            if (x, y) in stops:
                row.append("#")
            elif (x, y) in rocks:
                row.append("O")
            else:
                row.append(".")
        rows.append("".join(row))
    return "\n".join(rows)


def score(rocks, y_max):
    out = 0
    for _, y in rocks:
        out += 1 + y_max - y
    return out


def rocks_to_key(rocks):
    return tuple(rocks)


def solve(input):
    stops, rocks, x_max, y_max = input
    stops = set(stops)
    cycle = 0
    stop_at = 1000000000
    memory = {}
    while cycle < stop_at:
        tilt_north(stops, rocks, x_max, y_max)
        tilt_west(stops, rocks, x_max, y_max)
        tilt_south(stops, rocks, x_max, y_max)
        tilt_east(stops, rocks, x_max, y_max)
        rocks.sort()
        # print(display(stops, rocks, x_max, y_max))
        # print("-" * 40)
        cycle += 1
        key = rocks_to_key(rocks)
        if key in memory:
            step = cycle - memory[key]
            steps_needed = (stop_at - cycle) // step
            cycle = cycle + steps_needed * step
        else:
            memory[key] = cycle
    return score(rocks, y_max)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        rocks = []
        stops = []
        x_max = 0
        y_max = 0
        for y, row in enumerate(rows):
            y_max = max(y_max, y)
            for x, c in enumerate(row):
                x_max = max(x_max, x)
                if c == "#":
                    stops.append((x, y))
                elif c == "O":
                    rocks.append((x, y))
        return stops, rocks, x_max, y_max


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
