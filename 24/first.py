def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


class Hail:
    def __init__(self, position, velocity, limits):
        self.position = position
        self.velocity = velocity
        self.dim = len(position)
        self.start = self.determine_start(limits)
        self.end = self.determine_end(limits)

    def __str__(self):
        return "{} @ {} | {}->{}".format(
            str(self.position), str(self.velocity), str(self.start), str(self.end)
        )

    def determine_start(self, limits):
        low, high = limits

        def valid(position):
            # float leninency
            return all(low - 0.1 <= x <= high + 0.1 for x in position)

        def time_to_pos(time):
            return tuple(
                [self.position[i] + time * self.velocity[i] for i in range(self.dim)]
            )

        if valid(self.position):
            return self.position
        times = []
        for i in range(self.dim):
            x = self.position[i]
            v = self.velocity[i]
            if x < low and v > 0:
                times.append((low - x) / v)
            elif x > high and v < 0:
                times.append((high - x) / v)

        valid_times = []
        for time in times:
            candidate = time_to_pos(time)
            if valid(candidate):
                valid_times.append(time)

        if len(valid_times) == 0:
            return None
        time = min(valid_times)
        assert time >= 0
        return time_to_pos(time)

    def determine_end(self, limits):
        if self.start is None:
            return None
        low, high = limits

        def valid(position):
            # float leninency
            return all(low - 0.1 <= x <= high + 0.1 for x in position)

        def time_to_pos(time):
            return tuple(
                [self.start[i] + time * self.velocity[i] for i in range(self.dim)]
            )

        times = []
        for i in range(self.dim):
            x = self.start[i]
            v = self.velocity[i]
            if v < 0:
                times.append((low - x) / v)
            elif v > 0:
                times.append((high - x) / v)

        valid_times = []
        for time in times:
            candidate = time_to_pos(time)
            if valid(candidate):
                valid_times.append(time)
        if len(valid_times) == 0:
            return None
        time = min(valid_times)
        assert time >= 0
        return time_to_pos(time)

    def intersection(self, other):
        x1 = self.start[0]
        y1 = self.start[1]
        x2 = self.end[0]
        y2 = self.end[1]
        x3 = other.start[0]
        y3 = other.start[1]
        x4 = other.end[0]
        y4 = other.end[1]
        divisor = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if divisor == 0:
            return False  # parallell
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / divisor
        u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / divisor
        return 0 <= t <= 1 and 0 <= u <= 1

    def is_valid(self):
        return self.start is not None and self.end is not None


def solve(input):
    out = 0
    for i, hail_i in enumerate(input[:-1]):
        for hail_j in input[i + 1 :]:
            # print(hail_i)
            # print(hail_j)
            # print(hail_i.intersection(hail_j))
            # print("")
            if hail_i.intersection(hail_j):
                out += 1
    return out


def read(filename):
    limits = (7, 27)
    if filename == "input.txt":
        limits = (200000000000000, 400000000000000)
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]

        def parse(part):
            return tuple(list(map(int, map(str.strip, part.split(","))))[:2])

        input = []
        for row in rows:
            left, right = row.split("@")
            position = parse(left)
            velocity = parse(right)
            hail = Hail(position, velocity, limits)
            if hail.is_valid():
                input.append(hail)
            else:
                print(hail)
        return input


def main(filename):
    # 16752 too high
    # 16740 too high [guess]
    # 13036 too low
    # 16384 wrong
    # 16727 right
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
