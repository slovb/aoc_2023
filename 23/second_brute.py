class Node:
    def __init__(self, position, previous):
        self.position = position
        self.previous = previous

    def has_been_at(self, position):
        node = self
        while node is not None:
            if node.position == position:
                return True
            node = node.previous
        return False

    def length(self):
        node = self
        output = 0
        while node is not None:
            output += 1
            node = node.previous
        return output - 1


def solve(input):
    paths, start, end = input
    out = []
    leafs = [Node(start, None)]
    while len(leafs) > 0:
        leaf = leafs.pop()
        if leaf.position == end:
            out.append(leaf.length())
            continue
        alternatives = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in alternatives:
            pos = (leaf.position[0] + dx, leaf.position[1] + dy)
            if pos in paths and not leaf.has_been_at(pos):
                leafs.append(Node(pos, leaf))
    return max(out)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        paths = set()
        start = (1, 0)
        end = (len(rows) - 2, len(rows) - 1)
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == "#":
                    continue
                paths.add((x, y))
        return paths, start, end


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
