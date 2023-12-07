import functools
from pprint import pprint


def card_to_num(card):
    if card == "T":
        return 10
    elif card == "J":
        return 11
    elif card == "Q":
        return 12
    elif card == "K":
        return 13
    elif card == "A":
        return 14
    return int(card)


def classify(hand):
    counts = {}
    for c in hand:
        if c not in counts:
            counts[c] = 0
        counts[c] += 1
    if len(counts) == 1:
        return 7  # five of a kind
    elif len(counts) == 2:
        for count in counts.values():
            if count == 4:
                return 6  # four of a kind
            if count == 3:
                return 5  # full house
    elif len(counts) == 3:
        for count in counts.values():
            if count == 3:
                return 4  # three of a kind
            if count == 2:
                return 3  # two pair
    elif len(counts) == 4:
        return 2  # one pair
    return 1  # high card


def compare(row1, row2):
    hand1, _, type1 = row1
    hand2, _, type2 = row2
    if hand1 == hand2:
        return 0

    if type1 < type2:
        return -1
    elif type1 > type2:
        return 1
    for i in range(len(hand1)):
        c1 = card_to_num(hand1[i])
        c2 = card_to_num(hand2[i])
        if c1 < c2:
            return -1
        elif c1 > c2:
            return 1
    raise SystemError("Equal check is broken")


def solve(input):
    out = 0
    input.sort(key=functools.cmp_to_key(compare))
    for i, row in enumerate(input):
        _, bid, _ = row
        out += (i + 1) * bid
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            # row = row.split(",")
            # row = map(str.strip, row)
            # row = map(int, row)
            hand, bid = row.split(" ")
            bid = int(bid)
            input.append((hand, bid, classify(hand)))
            # input.append(int(row))
            # input.append(list(row))
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
