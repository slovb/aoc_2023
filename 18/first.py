from pprint import pprint


def position_after_dir(x, y, dir):
    if dir == "U":
        return (x, y - 1)
    elif dir == "R":
        return (x + 1, y)
    elif dir == "D":
        return (x, y + 1)
    elif dir == "L":
        return (x - 1, y)
    raise Exception("!!")


def solve(input):
    x, y = 0, 0
    trench = {}
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0

    # draw the exterior
    for row in input:
        dir, num, color = row
        for i in range(num):
            x, y = position_after_dir(x, y, dir)
            trench[(x, y)] = color
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)

    # fill out the interior
    tried = set()
    for y in range(y_min + 1, y_max):
        for x in range(x_min + 1, x_max):
            if (x, y) in tried or (x, y) in trench:
                continue
            positions = [(x, y)]
            tried.add((x, y))
            dead = False
            i = 0
            while i < len(positions):
                px, py = positions[i]
                candidates = [(px - 1, py), (px, py - 1), (px + 1, py), (px, py + 1)]
                for candidate in candidates:
                    if candidate in tried or candidate in trench:
                        continue
                    tried.add(candidate)
                    cx, cy = candidate
                    if cx <= x_min or cx >= x_max or cy <= y_min or cy >= y_max:
                        dead = True
                        continue
                    positions.append(candidate)
                i += 1
            if not dead:
                for p in positions:
                    trench[p] = None
    return len(trench)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            dir, num, color = row.split(" ")
            num = int(num)
            color = color[2:-1]
            input.append((dir, num, color))
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
