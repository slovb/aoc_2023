directions = {"U": 0, "R": 1, "D": 2, "L": 3}


class Node:
    def __init__(self, x, y, turn_nr):
        self.x = x
        self.y = y
        self.turn_nr = turn_nr

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def dist_prev(self):
        return self.dist(self.prev)

    def dist_next(self):
        return self.dist(self.next)

    def area(self):
        return self.dist_prev() * self.dist_next()


def position_after_dir(x, y, dir, step=1):
    if dir == "U":
        return (x, y - step)
    elif dir == "R":
        return (x + step, y)
    elif dir == "D":
        return (x, y + step)
    elif dir == "L":
        return (x - step, y)
    raise Exception("!!")


def initialize_nodes(input):
    x, y = 0, 0
    nodes = []

    # draw the exterior
    prev_node = None
    prev_dir = None
    for row in input:
        dir, num = row

        # add the current poitn as a node
        turn_nr = None
        if prev_dir is not None:
            turn_nr = (directions[dir] - prev_dir) % 4
            node = Node(x, y, turn_nr)
            prev_node.next = node
            node.prev = prev_node
        else:
            node = Node(x, y, None)

        nodes.append(node)
        prev_dir = directions[dir]
        prev_node = node

        # traverse forward
        x, y = position_after_dir(x, y, dir, num)

    # adjust the root nodes turn_nr
    turn_nr = (directions[input[0][0]] - prev_dir) % 4
    nodes[0].turn_nr = turn_nr
    prev_node.next = nodes[0]
    nodes[0].prev = prev_node
    return nodes


# def sign(x):
#     if x == 0:
#         return 0
#     elif x > 0:
#         return 1
#     return -1


# def between(aligned_corner, opposite_corner, peek):
#     if aligned_corner[1] == opposite_corner[1] == peek.y:
#         if aligned_corner[0] == opposite_corner[0]:
#             raise Exception("!")
#         if aligned_corner[0] <= peek.x <= opposite_corner[0]:
#             return True
#         if opposite_corner[0] <= peek.x <= aligned_corner[0]:
#             return True
#     elif aligned_corner[0] == opposite_corner[0] == peek.x:
#         if aligned_corner[1] == opposite_corner[1]:
#             raise Exception("!")
#         if aligned_corner[1] <= peek.y <= opposite_corner[1]:
#             return True
#         if opposite_corner[1] <= peek.y <= aligned_corner[1]:
#             return True
#     return False


def solve(input):
    nodes = initialize_nodes(input)
    double_area = 0
    boundry = 0
    for node in nodes:
        double_area += node.y * (node.prev.x - node.next.x)
        boundry += node.dist_prev()
    area = double_area // 2

    # while len(nodes) > 0:
    #     node = nodes.pop(0)
    #     if node.turn_nr == 3:
    #         continue
    #     # try to work our way to next
    #     dx = node.next.x - node.x
    #     dy = node.next.y - node.y
    #     i = 1
    #     while True:
    #         aligned_corner = (node.x + i * sign(dx), node.y + i * sign(dy))
    #         if aligned_corner == (node.next.x, node.next.y):
    #             break
    #         opposite_corner = (node.prev.x + i * sign(dx), node.prev.y + i * sign(dy))
    #         peek = node.next
    #         done = False
    #         while peek is not node.prev:
    #             peek = peek.next
    #             if between(aligned_corner, opposite_corner, peek):
    #                 i -= 1
    #                 aligned_corner = (node.x + i * sign(dx), node.y + i * sign(dy))
    #                 opposite_corner = (
    #                     node.prev.x + i * sign(dx),
    #                     node.prev.y + i * sign(dy),
    #                 )
    #                 if node.prev in nodes:
    #                     nodes.remove(node.prev)
    #                     ### TODO HEADACHE
    #                 done = True
    #                 break
    #         if done:
    #             break
    #         i += 1
    #     print(
    #         (1 + abs(opposite_corner[0] - node.x))
    #         * (1 + abs(opposite_corner[1] - node.y))
    #     )
    #     area += (1 + abs(opposite_corner[0] - node.x)) * (
    #         1 + abs(opposite_corner[1] - node.y)
    #     )
    return area + (boundry // 2) + 1


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            _, _, color = row.split(" ")
            color = color[2:-1]
            num = color[:-1]
            num = int("0x" + num, 0)
            dir = color[-1]
            if dir == "0":
                dir = "R"
            elif dir == "1":
                dir = "D"
            elif dir == "2":
                dir = "L"
            elif dir == "3":
                dir = "U"
            input.append((dir, num))
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
