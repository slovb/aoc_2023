def candidate_steps(x, y, u, v, max_x, max_y):
    for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if nx < 0:
            yield (max_x, ny, (u - 1) % 2, v)
        elif nx > max_x:
            yield (0, ny, (u + 1) % 2, v)
        elif ny < 0:
            yield (nx, max_y, u, (v - 1) % 2)
        elif ny > max_y:
            yield (nx, 0, u, (v + 1) % 2)
        else:
            yield (nx, ny, u, v)


def find_memories(start_x, start_y, rocks, max_x, max_y, steps, return_odd=False):
    even_memory = set()
    even_memory.add((start_x, start_y, 0, 0))
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
    if return_odd:
        return odd_memory
    return even_memory


def solve(input):
    (start_x, start_y), rocks, max_x, max_y = input
    even_memory = find_memories(
        start_x, start_y, rocks, max_x, max_y, 2 + max_x + max_y
    )
    from_even, from_odd = 0, 0
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if (x, y, 0, 0) in even_memory:
                from_even += 1
            if (x, y, 0, 1) in even_memory:
                from_odd += 1
    # S is on a row and column that are open, the rim is open
    # S is right in the middle
    # THIS IS NOT THE CASE FOR TEST INPUT
    # max_x == max_y
    # 26501365 % 131 = 65
    target = 26501365
    # target = 49 + 22 + 11
    sides_odd = (target // (max_x + 1)) % 2 == 1  # TODO CALCULATE

    radius = (target + start_x) // (max_x + 1)

    num_even = (radius - 1) ** 2  # -m + 2 * (m + m-1 + m-2 +...)
    num_odd = (radius) ** 2
    if not sides_odd:
        num_even, num_odd = num_odd, num_even

    num_sides = 1  # all 4 are summed together
    num_short_corners = radius
    num_long_corners = num_short_corners - 1

    # kinda hacky, just works when all things are aligned
    steps_from_side = max_x
    steps_from_short = start_x - 1
    steps_from_long = max_x + start_x

    # halp = [
    #     (x, y)
    #     for x, y, u, v in find_memories(
    #         0, start_y, rocks, max_x, max_y, steps_from_side, not sides_are_odd
    #     )
    #     if u == v == 0
    # ]
    # print(sorted(halp))

    def count_from(x, y, steps, odd):
        out = 0
        for _, _, u, v in find_memories(x, y, rocks, max_x, max_y, steps, odd):
            if u == v == 0:
                out += 1
        return out

    odd_sides = sides_odd
    from_left = count_from(0, start_y, steps_from_side, odd_sides)
    from_right = count_from(max_x, start_y, steps_from_side, odd_sides)
    from_top = count_from(start_x, 0, steps_from_side, odd_sides)
    from_bottom = count_from(start_x, max_y, steps_from_side, odd_sides)
    from_sides = sum([from_left, from_top, from_right, from_bottom])

    odd_short = sides_odd
    short_from_top_left = count_from(0, 0, steps_from_short, odd_short)
    short_from_top_right = count_from(max_x, 0, steps_from_short, odd_short)
    short_from_bottom_right = count_from(max_x, max_y, steps_from_short, odd_short)
    short_from_bottom_left = count_from(0, max_y, steps_from_short, odd_short)
    short_from_corners = sum(
        [
            short_from_top_left,
            short_from_top_right,
            short_from_bottom_left,
            short_from_bottom_right,
        ]
    )

    odd_long = not sides_odd
    long_from_top_left = count_from(0, 0, steps_from_long, odd_long)
    long_from_top_right = count_from(max_x, 0, steps_from_long, odd_long)
    long_from_bottom_right = count_from(max_x, max_y, steps_from_long, odd_long)
    long_from_bottom_left = count_from(0, max_y, steps_from_long, odd_long)
    long_from_corners = sum(
        [
            long_from_top_left,
            long_from_top_right,
            long_from_bottom_left,
            long_from_bottom_right,
        ]
    )
    print(
        num_even * from_even,
        num_odd * from_odd,
        num_sides * from_sides,
        num_short_corners * short_from_corners,
        num_long_corners * long_from_corners,
    )
    # 618255384853487 too low
    # 618261391140643 too low
    # 618261424520143 too low
    # 618261433219061 too low
    # 618261433219147 correct
    return (
        num_even * from_even
        + num_odd * from_odd
        + num_sides * from_sides
        + num_short_corners * short_from_corners
        + num_long_corners * long_from_corners
    )


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
