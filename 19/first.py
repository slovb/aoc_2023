from typing import Callable, Dict, List, Tuple


class Part:
    def __init__(self, x: int, m: int, a: int, s: int) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def total(self) -> int:
        return self.x + self.m + self.a + self.s

    def __str__(self) -> str:
        return "Part{}".format(str((self.x, self.m, self.a, self.s)))


class Rule:
    def __init__(self, rule_text: str) -> None:
        self.rule_text = rule_text
        match rule_text[0]:
            case "x":
                self.get = get_x
            case "m":
                self.get = get_m
            case "a":
                self.get = get_a
            case "s":
                self.get = get_s
        num_text, target = rule_text[2:].split(":")
        n = int(num_text)
        match rule_text[1]:
            case "<":
                self.op = lt_op(n)
            case ">":
                self.op = gt_op(n)
        self.target = target

    def check(self, part: Part) -> bool:
        return self.op(self.get(part))

    def __str__(self) -> str:
        return "Rule: {}".format(self.rule_text)


class Workflow:
    def __init__(self, name: str, rules: List[Rule], default: str) -> None:
        self.name = name
        self.rules = rules
        self.default = default

    def handle(self, part: Part) -> str:
        for rule in self.rules:
            if rule.check(part):
                return rule.target
        return self.default

    def __str__(self) -> str:
        lines = []
        lines.append("Workflow: {}".format(self.name))
        for rule in self.rules:
            lines.append("  {}".format(str(rule)))
        lines.append("  Default: {}".format(self.default))
        return "\n".join(lines)


def get_x(part: Part) -> int:
    return part.x


def get_m(part: Part) -> int:
    return part.m


def get_a(part: Part) -> int:
    return part.a


def get_s(part: Part) -> int:
    return part.s


def lt_op(n: int) -> Callable[[int], bool]:
    return lambda i: i < n


def gt_op(n: int) -> Callable[[int], bool]:
    return lambda i: i > n


def solve(input):
    out = 0
    workflows, parts = input
    # for workflow in workflows.values():
    #     print("{}".format(str(workflow)))
    #     print("-" * 40)
    # for part in parts:
    #     print(part)
    for part in parts:
        step = "in"
        process = [step]
        while step not in ["A", "R"]:
            workflow = workflows[step]
            step = workflow.handle(part)
            process.append(step)
        if step == "A":
            out += part.total()
        print("{}: {}".format(part, " -> ".join(process)))
    return out


def read(filename: str) -> Tuple[Dict[str, Workflow], List[Part]]:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        workflows = {}
        for i, row in enumerate(rows):
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
        parts = []
        for row in rows[i + 1 :]:
            x_str, m_str, a_str, s_str = row.split(",")
            x = int(x_str.split("=")[1])
            m = int(m_str.split("=")[1])
            a = int(a_str.split("=")[1])
            s = int(s_str.split("=")[1][:-1])
            parts.append(Part(x, m, a, s))

        return workflows, parts


def main(filename: str) -> int:
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
