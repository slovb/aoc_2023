from pprint import pprint


def count(time, distance):
    # maximum at time = 2 speed
    def is_winning(speed):
        return distance < speed * (time - speed)

    start = 0
    end = time

    # find the start
    low = 0
    high = int(time // 2)
    while high - low > 1:
        mid = low + int((high - low) // 2)
        if is_winning(mid):
            high = mid
        else:
            low = mid
    start = high

    # find the end
    low = int(time // 2)
    high = time
    while high - low > 1:
        mid = low + int((high - low) // 2)
        if is_winning(mid):
            low = mid
        else:
            high = mid
    end = low

    return end - start


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
