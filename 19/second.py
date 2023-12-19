from functools import reduce
import operator
from typing import Dict, List, Tuple


class MultiPart:
    def __init__(
        self,
        x_ranges: List[Tuple[int, int]],
        m_ranges: List[Tuple[int, int]],
        a_ranges: List[Tuple[int, int]],
        s_ranges: List[Tuple[int, int]],
    ) -> None:
        self.ranges = {"x": x_ranges, "m": m_ranges, "a": a_ranges, "s": s_ranges}

    def total_key(self, key) -> int:
        out = 0
        for a, b in self.ranges[key]:
            out += 1 + b - a
        return out

    def total(self) -> int:
        return reduce(operator.mul, [self.total_key(key) for key in self.ranges])

    def with_ranges(self, category, ranges):
        out = MultiPart(
            self.ranges["x"], self.ranges["m"], self.ranges["a"], self.ranges["s"]
        )
        out.ranges[category] = ranges
        return out

    def __str__(self) -> str:
        lines = []
        lines.append("MultiPart:")
        for key, ranges in self.ranges.items():
            lines.append("    {}: {}".format(key, str(ranges)))
        return "\n".join(lines)


class State:
    def __init__(self, name: str, multipart: MultiPart) -> None:
        self.name = name
        self.multipart = multipart

    def __str__(self) -> str:
        return "State: {}\n  {}".format(self.name, str(self.multipart))


class Rule:
    def __init__(self, rule_text: str) -> None:
        self.rule_text = rule_text
        self.category = rule_text[0]
        self.op = rule_text[1]

        num_text, target = rule_text[2:].split(":")
        self.num = int(num_text)
        self.target = target

    def handle(self, part: MultiPart) -> Tuple[MultiPart, MultiPart]:
        ranges = []
        ranges = part.ranges[self.category]
        failing = []
        passing = []
        for a, b in ranges:
            if self.op == "<":
                if b < self.num:
                    passing.append((a, b))
                elif a >= self.num:
                    failing.append((a, b))
                else:
                    passing.append((a, self.num - 1))
                    failing.append((self.num, b))
            elif self.op == ">":
                if a > self.num:
                    passing.append((a, b))
                elif b <= self.num:
                    failing.append((a, b))
                else:
                    failing.append((a, self.num))
                    passing.append((self.num + 1, b))
            else:
                raise Exception("!!")
        passing_part = part.with_ranges(self.category, passing)
        failing_part = part.with_ranges(self.category, failing)
        return (passing_part, failing_part)

    def __str__(self) -> str:
        return "Rule: {}".format(self.rule_text)


class Workflow:
    def __init__(self, name: str, rules: List[Rule], default: str) -> None:
        self.name = name
        self.rules = rules
        self.default = default

    def handle(self, part: MultiPart) -> List[State]:
        states = []
        for rule in self.rules:
            passing_part, part = rule.handle(part)
            if passing_part.total() > 0:
                states.append(State(rule.target, passing_part))
            if part.total() == 0:
                return states
        if part.total() > 0:
            states.append(State(self.default, part))
        return states

    def __str__(self) -> str:
        lines = []
        lines.append("Workflow: {}".format(self.name))
        for rule in self.rules:
            lines.append("  {}".format(str(rule)))
        lines.append("  Default: {}".format(self.default))
        return "\n".join(lines)


def solve(input):
    out = 0
    workflows = input
    states = [
        State(
            "in",
            MultiPart(
                [(1, 4000)],
                [(1, 4000)],
                [(1, 4000)],
                [(1, 4000)],
            ),
        )
    ]
    while len(states) > 0:
        state = states.pop()
        print(state)
        if state.name == "R":
            print("Reject: {}".format(state.multipart.total()))
        elif state.name == "A":
            total = state.multipart.total()
            print("Reject: {}".format(total))
            out += total
        else:
            workflow = workflows[state.name]
            print(workflow)
            for s in workflow.handle(state.multipart):
                states.append(s)
                print(s)
        print("-" * 40)
    return out


def read(filename: str) -> Dict[str, Workflow]:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        workflows = {}
        for row in rows:
            if row == "":
                break
            name, rules_text = row.split("{")
            rules_text = rules_text[:-1]  # remove }
            rule_texts = rules_text.split(",")
            default = rule_texts[-1]
            rule_texts = rule_texts[:-1]  # ignore default
            rules = []
            for rule_text in rule_texts:
                rules.append(Rule(rule_text))
            workflows[name] = Workflow(name, rules, default)

        return workflows


def main(filename: str) -> int:
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
