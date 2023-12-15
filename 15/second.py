def score(memory):
    out = 0
    for nr, box in memory.items():
        for i, lens in enumerate(box):
            _, focal = lens
            out += (nr + 1) * (i + 1) * focal
    return out


def hash(text):
    out = 0
    for c in text:
        out += ord(c)
        out *= 17
        out %= 256
    return out


def solve(input):
    memory = {i: [] for i in range(256)}
    for step in input:
        left, right = step
        box = hash(left)
        if right is None:
            for i, lens in enumerate(memory[box]):
                if lens[0] == left:
                    del memory[box][i]
                    break
        else:
            changed = False
            for i, lens in enumerate(memory[box]):
                if lens[0] == left:
                    changed = True
                    memory[box][i] = step
                    break
            if not changed:
                memory[box].append(step)
    return score(memory)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            row = row.split(",")
            for step in row:
                parts = step.split("=")
                if len(parts) == 1:
                    input.append((parts[0][:-1], None))
                else:
                    input.append((parts[0], int(parts[1])))
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
