from pprint import pprint


def count(time, distance):
    out = 0
    for speed in range(1, time):
        # print(speed, time - speed, speed * (time - speed))
        if distance < speed * (time - speed):
            # print("++")
            out += 1
    return out


def solve(input):
    times, distances = input
    out = 1
    for i in range(len(times)):
        print(count(times[i], distances[i]))
        out *= count(times[i], distances[i])
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        times = []
        distances = []

        row = rows[0].split(":")[1]
        for group in row.split(" "):
            if group != "":
                times.append(int(group))
        row = rows[1].split(":")[1]
        for group in row.split(" "):
            if group != "":
                distances.append(int(group))

        return times, distances


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
