from abc import ABC
from typing import List


class Section:
    def __init__(self, color: str):
        self.color = color
        self.enabled = False

    def set_enabled(self, value: bool):
        self.enabled = value

    def __str__(self):
        return self.color if self.enabled else ' '

class BaseState(ABC):
    def __init__(self):
        self.data = [0, 0, 0]

    def set_lamps(self, lamps: List[Section]) -> None:
        for i in range(len(self.data)):
            lamps[i].set_enabled(bool(self.data[i]))

class RedState(BaseState):
    def __init__(self):
        super().__init__()
        self.data[0] = 1

class YellowState(BaseState):
    def __init__(self):
        super().__init__()
        self.data[1] = 1

class GreenState(BaseState):
    def __init__(self):
        super().__init__()
        self.data[2] = 1

class StateChanger:
    def __init__(self):
        self.states = [
            (0, GreenState),
            (3, YellowState),
            (4, RedState)
        ]
        self.loop_time = 6

    def __get_lower_or_equal(self, index: int):
        data = sorted(self.states, key=lambda  x: x[0])
        i = 0
        while i < len(data) and data[i][0] <= index:
            i += 1
        return data[i - 1][1]

    def get_state_by_time(self, time: int) -> BaseState:
        index = time % self.loop_time
        return self.__get_lower_or_equal(index)()


class TrafficLight:
    def __init__(self):
        self.sections = [
            Section('RED'),
            Section('YELLOW'),
            Section('GREEN'),
        ]
        self.state = None
        self.time = 0
        self.state = StateChanger().get_state_by_time(self.time)
        self.state.set_lamps(self.sections)

    def add_time(self, time):
        self.time += time
        self.state = StateChanger().get_state_by_time(self.time)
        self.state.set_lamps(self.sections)

    def __str__(self):
        return ','.join(
            str(section) for section in self.sections if section.enabled
        )


def main():
    time = int(input())
    traffic_light = TrafficLight()
    traffic_light.add_time(time)
    print(traffic_light)

if __name__ == '__main__':
    main()

