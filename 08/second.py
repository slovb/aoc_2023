import math
from pprint import pprint


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def solve(input):
    instructions, tree = input
    nodes = []
    for node in tree:
        if node[-1] == "A":
            nodes.append(node)
    length = len(nodes)

    i = 0
    mod = len(instructions)
    initials = {}
    steps = {}
    while len(steps) < length:
        instruction = instructions[i % mod]
        for key, node in enumerate(nodes):
            if key in steps:
                continue
            if node[-1] == "Z":
                if key in initials:
                    steps[key] = i - initials[key]
                else:
                    initials[key] = i

            if instruction == "L":
                nodes[key] = tree[node][0]
            else:
                nodes[key] = tree[node][1]
        i += 1

    i -= 1
    step = 1
    while True:
        at_goal = True
        for j in range(length):
            if 0 == (i - initials[j]) % steps[j]:
                step = lcm(step, steps[j])
            else:
                at_goal = False
        if at_goal:
            return i
        i += step


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
