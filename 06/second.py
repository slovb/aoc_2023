from pprint import pprint


def count(time, distance):
    out = 0
    for speed in range(1, time):
        if distance < speed * (time - speed):
            out += 1
    return out


def solve(input):
    time, distance = input
    out = count(time, distance)
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        times = []
        distances = []

        row = rows[0].split(":")[1]
        for group in row.split(" "):
            if group != "":
                times.append(group)
        time = int("".join(times))

        row = rows[1].split(":")[1]
        for group in row.split(" "):
            if group != "":
                distances.append(group)
        distance = int("".join(distances))

        return time, distance


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
