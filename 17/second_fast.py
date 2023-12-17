from dataclasses import dataclass
import heapq

# barely faster, can't find a good heuristic so scrapped that


@dataclass
class Direction:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def step(x, y, dir):
    if dir == Direction.NORTH:
        return (x, y - 1)
    elif dir == Direction.EAST:
        return (x + 1, y)
    elif dir == Direction.SOUTH:
        return (x, y + 1)
    elif dir == Direction.WEST:
        return (x - 1, y)
    raise Exception("!!!")


def solve(input):
    max_x = len(input[0]) - 1
    max_y = len(input) - 1
    destination = (max_x, max_y)

    # loss, x, y, steps since turn, direction
    states = []
    heapq.heappush(states, (0, 0, 0, 0, Direction.EAST))

    # x, y, steps since turn, direction : loss
    memory = {(0, 0, 0, Direction.EAST): 0, (0, 0, 0, Direction.SOUTH): 0}

    out = None
    while len(states) > 0:
        loss, x, y, steps_since_turn, direction = heapq.heappop(states)
        if (x, y) == destination:
            return loss

        candidates = []
        # move forward:
        if steps_since_turn < 10:
            new_x, new_y = step(x, y, direction)
            candidates.append((new_x, new_y, steps_since_turn + 1, direction))
        # turn left:
        if steps_since_turn >= 4:
            new_direction = (direction - 1) % 4
            new_x, new_y = step(x, y, new_direction)
            candidates.append((new_x, new_y, 1, new_direction))
        # turn right:
        if steps_since_turn >= 4:
            new_direction = (direction + 1) % 4
            new_x, new_y = step(x, y, new_direction)
            candidates.append((new_x, new_y, 1, new_direction))

        # process candidates
        for candidate in candidates:
            new_x, new_y, new_steps, new_direction = candidate
            if new_x < 0 or new_x > max_x:
                continue
            if new_y < 0 or new_y > max_y:
                continue
            new_loss = loss + input[new_y][new_x]
            new_memkey = (new_x, new_y, new_steps, new_direction)
            new_state = (new_loss, new_x, new_y, new_steps, new_direction)
            if new_memkey not in memory or memory[new_memkey] > new_loss:
                memory[new_memkey] = new_loss
                heapq.heappush(states, new_state)
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            row = list(map(int, row))

            input.append(row)
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
