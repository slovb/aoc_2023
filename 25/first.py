from itertools import combinations
import networkx as nx


def solve(G):
    nodes = G.nodes()
    for picked in combinations(nodes, 2):
        cut_value, partition = nx.minimum_cut(G, picked[0], picked[1])
        if cut_value == 3:
            reachable, non_reachable = partition
            return len(reachable) * len(non_reachable)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        G = nx.Graph()

        for row in rows:
            base, others = row.split(":")
            others = others.strip().split(" ")
            for other in others:
                G.add_edge(base, other, capacity=1)

        return G


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
