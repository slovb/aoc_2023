from pprint import pprint


def solve(input):
    instructions, tree = input
    goal = "ZZZ"
    node = "AAA"
    i = 0
    mod = len(instructions)
    while node != goal:
        instruction = instructions[i % mod]
        if instruction == "L":
            node = tree[node][0]
        else:
            node = tree[node][1]
        i += 1
    out = i
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        instructions = rows[0]
        tree = {}
        for row in rows[2:]:
            base, _, left, right = row.split(" ")
            left = left[1:4]
            right = right[0:3]
            tree[base] = (left, right)
        return instructions, tree


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
