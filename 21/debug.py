def candidate_steps(x, y, u, v, max_x, max_y):
    for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if nx < 0:
            yield (max_x, ny, u - 1, v)
        elif nx > max_x:
            yield (0, ny, u + 1, v)
        elif ny < 0:
            yield (nx, max_y, u, v - 1)
        elif ny > max_y:
            yield (nx, 0, u, v + 1)
        else:
            yield (nx, ny, u, v)


def find_memories(start_x, start_y, rocks, max_x, max_y, steps):
    even_memory = set()
    odd_memory = set()
    positions = [(start_x, start_y, 0, 0)]
    for i in range(steps):
        step = i + 1
        new_positions = []
        for x, y, u, v in positions:
            for cx, cy, cu, cv in candidate_steps(x, y, u, v, max_x, max_y):
                if (cx, cy) in rocks:
                    continue
                if (cx, cy, cu, cv) in even_memory:
                    continue

                if step % 2 == 0:
                    even_memory.add((cx, cy, cu, cv))
                else:
                    if (cx, cy, cu, cv) in odd_memory:
                        continue
                    odd_memory.add((cx, cy, cu, cv))
                new_positions.append((cx, cy, cu, cv))
        positions = new_positions
    return even_memory


def solve(input):
    (start_x, start_y), rocks, max_x, max_y = input
    target = 49 + 22 + 11
    even_memory = find_memories(start_x, start_y, rocks, max_x, max_y, target)
    radius = (target + start_x) // (max_x + 1)
    count_even = 0
    count_odd = 0
    count_sides = 0
    count_odd_corners = 0
    count_even_corners = 0
    # halp = []
    for x, y, u, v in even_memory:
        if abs(u) + abs(v) <= radius - 1:
            if (abs(u) + abs(v)) % 2 == 0:
                count_even += 1
            else:
                count_odd += 1
        elif u == 0 or v == 0:
            count_sides += 1
            # if u == 4:
            #     halp.append((x, y))
        elif (abs(u) + abs(v)) % 2 == 0:
            count_even_corners += 1
        else:
            count_odd_corners += 1
    # print(sorted(halp))
    print(count_even, count_odd, count_sides, count_odd_corners, count_even_corners)
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
