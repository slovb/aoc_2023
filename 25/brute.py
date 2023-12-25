from itertools import combinations


def count(node, g, cuts):
    # size of g starting form node not going across cuts
    visited = set()
    processing = [node]
    out = 0

    def ok(a, b):
        return (a, b) not in cuts and (b, a) not in cuts

    while len(processing) > 0:
        current = processing.pop()
        if current in visited:
            continue
        visited.add(current)
        others = [other for other in g[current] if ok(current, other)]
        processing += others
        out += 1
    return out


def solve(input):
    connections, sorted_edges = input
    out = 0
    size = len(connections)
    node = sorted_edges[0][0]
    for cuts in combinations(sorted_edges, 3):
        c = count(node, connections, cuts)
        if c < size:
            print(cuts)
            print(c)
            out = c * (size - c)
            break
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        connections = {}
        edges = []

        def add(a, b):
            if a not in connections:
                connections[a] = []
            connections[a].append(b)
            if b not in connections:
                connections[b] = []
            connections[b].append(a)
            edges.append((a, b))

        for row in rows:
            base, others = row.split(":")
            others = others.strip().split(" ")
            for other in others:
                add(base, other)

        for a, b in edges:
            assert (b, a) not in edges

        ac = {key: len(connections[key]) for key in connections}

        sorted_edges = sorted(edges, key=lambda e: ac[e[0]] + ac[e[1]])

        return connections, sorted_edges


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
