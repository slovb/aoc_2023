from enum import Enum
from math import lcm
from typing import Dict, Generator, List, Tuple


class Pulse(Enum):
    HIGH = 1
    LOW = 0


class Signal:
    def __init__(self, origin: str, recipient: str, pulse: Pulse) -> None:
        self.origin = origin
        self.recipient = recipient
        self.pulse = pulse

    def __str__(self) -> str:
        return "{} -{}-> {}".format(self.origin, str(self.pulse), self.recipient)


class Module:
    def __init__(self, name: str, type: str, outs: List[str]) -> None:
        self.name = name
        self.type = type
        self.outs = outs
        self.memory: Dict[str, Pulse] = {}
        self.state = Pulse.LOW

    def handle(self, signal: Signal) -> Generator[Signal, None, None]:
        if self.type == "":
            self.state = signal.pulse
        elif self.type == "%":
            if signal.pulse == Pulse.HIGH:
                return
            self.state = Pulse.LOW if self.state == Pulse.HIGH else Pulse.HIGH
        elif self.type == "&":
            self.memory[signal.origin] = signal.pulse
            if all([pulse == Pulse.HIGH for pulse in self.memory.values()]):
                self.state = Pulse.LOW
            else:
                self.state = Pulse.HIGH
        else:
            raise Exception("!!")
        for out in self.outs:
            yield Signal(self.name, out, self.state)

    def __str__(self) -> str:
        return "{}{}: {} {}".format(
            self.type, self.name, str(self.state), str(self.memory)
        )


def setup_modules(input: List[Tuple[str, List[str]]]) -> Dict[str, Module]:
    modules = {}
    linking = []
    for name, outs in input:
        if name.startswith("%"):
            name = name[1:]
            type = "%"
        elif name.startswith("&"):
            name = name[1:]
            type = "&"
        else:
            type = ""
        modules[name] = Module(name, type, outs)
        for out in outs:
            linking.append((out, name))
    for out, name in linking:
        if out not in modules:
            modules[out] = Module(out, "", [])
        module = modules[out]
        if module.type == "&":
            modules[out].memory[name] = Pulse.LOW
    return modules


def solve(input: List[Tuple[str, List[str]]]) -> int:
    modules = setup_modules(input)

    button_presses = 0
    # keys found from reading inputs to the input of rx
    watching: Dict[str, List[int]] = {"xj": [], "qs": [], "kz": [], "km": []}
    out = 1
    while True:
        button_presses += 1
        signals = [Signal("button", "broadcaster", Pulse.LOW)]
        while len(signals) > 0:
            signal = signals.pop(0)
            if signal.pulse == Pulse.LOW:
                if signal.recipient == "rx":
                    return button_presses
                elif signal.recipient in watching:
                    watching[signal.recipient].append(button_presses)
                    # print(
                    #     "{}: {}".format(
                    #         signal.recipient, str(watching[signal.recipient])
                    #     )
                    # )
                    # prev = 0
                    # for i in watching[signal.recipient]:
                    #     print(i - prev)
                    #     prev = i

                    # they cycle with no issues at the start
                    out = lcm(out, button_presses)
                    if all([len(x) > 0 for x in watching.values()]):
                        return out
            signals += list(modules[signal.recipient].handle(signal))


def read(filename: str) -> List[Tuple[str, List[str]]]:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            parts = row.split(" ")
            name = parts[0]
            outs = [part.rstrip(",") for part in parts[2:]]
            input.append((name, outs))
        return input


def main(filename: str) -> int:
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}\n".format(main("input.txt")))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))
