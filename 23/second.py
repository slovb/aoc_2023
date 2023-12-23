from heapq import heappop, heappush


class Node:
    def __init__(self, position):
        self.position = position
        self.options = {}  # node, length of longest connection to node

    def link(self, other, length):
        if other not in self.options or self.options[other] < length:
            self.options[other] = length
        if self not in other.options or other.options[self] < length:
            other.options[self] = length

    def __str__(self):
        output = []
        output.append("Node: {}".format(str(self.position)))
        for node, length in self.options.items():
            output.append("  {} - {}".format(length, str(node.position)))
        return "\n".join(output)

    def __lt__(self, other):
        return self.position < other.position


def initialize(paths):
    alternatives = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    nodes = {}
    for point in paths:
        x, y = point
        adjacent_points = sum(
            [1 for dx, dy in alternatives if (x + dx, y + dy) in paths]
        )
        if adjacent_points != 2:
            nodes[point] = Node(point)
    for node in nodes.values():
        leafs = [(node.position, [node.position])]
        while len(leafs) > 0:
            leaf, history = leafs.pop()
            x, y = leaf
            for dx, dy in alternatives:
                pos = (x + dx, y + dy)
                if pos in history:
                    continue
                elif pos in nodes:
                    node.link(nodes[pos], len(history))
                elif pos in paths:
                    leafs.append((pos, history + [leaf]))
    return nodes


def solve(input):
    out = 0
    paths, start, end = input
    nodes = initialize(paths)
    for node in nodes.values():
        print(node)
        print("-" * 40)
    start_node = nodes[start]
    end_node = nodes[end]
    leafs = [(0, start_node, [start_node])]
    out = 0
    while len(leafs) > 0:
        score, at, history = heappop(leafs)
        if at == end_node:
            length = 0 - score
            if length > out:
                out = length
                # for node in history:
                #     print(node.position)
                # print(at.position)
                print(out)
        else:
            for node, length in at.options.items():
                if node not in history:
                    heappush(leafs, (score - length, node, history + [node]))
    return out


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
    # 4998 too low
    # 5534 too low
    # 5682 too low
    # 5906 wrong
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
