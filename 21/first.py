def candidate_steps(x, y):
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def solve(input):
    start, rocks, max_x, max_y = input
    even_memory = set()
    odd_memory = set()
    positions = [start]
    for i in range(64):
        step = i + 1
        new_positions = []
        for x, y in positions:
            for cx, cy in candidate_steps(x, y):
                if (cx, cy) in rocks:
                    continue
                if cx < 0 or cx > max_x or cy < 0 or cy > max_y:
                    continue
                if (cx, cy) in even_memory:
                    continue

                if step % 2 == 0:
                    even_memory.add((cx, cy))
                else:
                    if (cx, cy) in odd_memory:
                        continue
                    odd_memory.add((cx, cy))
                new_positions.append((cx, cy))
        positions = new_positions
    return len(even_memory)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        rocks = set()
        start = None
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == "S":
                    start = (x, y)
                elif c == "#":
                    rocks.add((x, y))
            max_x = x
        max_y = y
        return start, rocks, max_x, max_y


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
