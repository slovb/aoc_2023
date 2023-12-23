from heapq import heappop, heappush


class Edge:
    def __init__(self, start_position, end_position, length):
        self.start_position = start_position
        self.end_position = end_position
        self.length = length

    def __str__(self):
        return "{}-{} <{}>".format(
            str(self.start_position), str(self.end_position), str(self.length)
        )


def initialize(paths, start, end):
    edges = {}

    def add_edge(start_position, end_position, length):
        if start_position not in edges:
            edges[start_position] = []
        if end_position not in edges:
            edges[end_position] = []
        edge = Edge(start_position, end_position, length)
        if length == 1:
            for edge in edges[start_position]:
                if edge.length == 1 and edge.end_position == end_position:
                    # ugly avoiding duplicate joinings
                    return
        edges[start_position].append(edge)
        edges[end_position].append(edge)

    leafs = [(start, start, 0, None)]
    visited = set()
    visited.add(start)
    while len(leafs) > 0:
        base, at, length, prev = leafs.pop()
        alternatives = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        viable = []
        for dx, dy in alternatives:
            pos = (at[0] + dx, at[1] + dy)
            if pos != prev and pos in paths:
                viable.append(pos)
        if len(viable) == 0:
            add_edge(base, at, length)
        elif len(viable) == 1:
            if viable[0] in visited:
                add_edge(base, at, length)

                # adds too many extra duplicate edges, TODO make joining dangling edges cleaner
                add_edge(at, viable[0], 1)
            else:
                visited.add(viable[0])
                leafs.append((base, viable[0], length + 1, at))
        else:
            add_edge(base, at, length)
            for pos in viable:
                if pos in visited:
                    add_edge(at, pos, 1)
                else:
                    visited.add(pos)
                    leafs.append((at, pos, 1, at))
    return edges


def solve(input):
    paths, start, end = input
    out = 0
    edges = initialize(paths, start, end)
    for at, edge_list in edges.items():
        print(at)
        for edge in edge_list:
            print(edge)
        print("-" * 40)
    assert len(edges[start]) == 1
    assert len(edges[end]) == 1
    near_end = edges[end][0].start_position
    end_length = edges[end][0].length

    start_edge = edges[start][0]
    memory = {}
    leafs = [
        (
            -start_edge.length,
            start_edge.length,
            start_edge.end_position,
            [start],
            [start_edge],
        )
    ]
    while len(leafs) > 0:
        score, length, position, visited, history = leafs.pop(0)
        if position in memory and length < memory[position]:
            continue
        memory[position] = length
        if position == near_end:
            length += end_length
            if length > out:
                for edge in history:
                    print(edge)
                print(length)
                print("-" * 40)
                out = length
        elif position in edges:
            for edge in edges[position]:
                if edge not in history:
                    if edge.end_position == position:
                        pos = edge.start_position
                    else:
                        pos = edge.end_position
                    if pos not in visited:
                        leafs.append(
                            (
                                score - edge.length,
                                length + edge.length,
                                pos,
                                visited + [position],
                                history + [edge],
                            ),
                        )
                        # leafs.append(
                        #     (
                        #         length + edge.length,
                        #         pos,
                        #         visited + [position],
                        #         history + [edge],
                        #     )
                        # )
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
