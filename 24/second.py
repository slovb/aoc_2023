from z3 import Int, Real, Solver


class Hail:
    def __init__(self, position, velocity, limits):
        self.position = position
        self.velocity = velocity
        self.dim = len(position)

    def __str__(self):
        return "{} @ {}".format(str(self.position), str(self.velocity))


def solve(input):
    hail_list, limits = input
    # h4p = hail_list[0].position
    # h4v = hail_list[0].velocity

    t1 = Int("t1")
    t2 = Int("t2")
    t3 = Int("t3")
    # t4 = Int('t4')
    times = [t1, t2, t3]

    px = Int("px")
    py = Int("py")
    pz = Int("pz")
    positions = [px, py, pz]

    vx = Int("vx")
    vy = Int("vy")
    vz = Int("vz")
    velocities = [vx, vy, vz]

    s = Solver()

    # time constraints
    s.add(t1 >= 0)
    s.add(t2 >= 0)
    s.add(t3 >= 0)

    for j in range(3):
        hj = hail_list[j]
        hjp = hj.position
        hjv = hj.velocity
        for i in range(3):
            s.add(hjp[i] + times[j] * hjv[i] == positions[i] + times[j] * velocities[i])

    print(s.check())
    m = s.model()
    print(m)

    out = m[px] + m[py] + m[pz]
    return out


def read(filename):
    limits = (7, 27)
    if filename == "input.txt":
        limits = (200000000000000, 400000000000000)
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]

        def parse(part):
            return tuple(list(map(int, map(str.strip, part.split(",")))))

        input = []
        for row in rows:
            left, right = row.split("@")
            position = parse(left)
            velocity = parse(right)
            hail = Hail(position, velocity, limits)
            input.append(hail)
        return input, limits


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
