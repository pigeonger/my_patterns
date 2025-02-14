from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def green(self, traffic_lights):
        pass

    @abstractmethod
    def yellow(self, traffic_lights):
        pass

    @abstractmethod
    def red(self, traffic_lights):
        pass

class Green_light(State):
    def green(self, traffic_lights):
        print("GREEN")

    def yellow(self, traffic_lights):
        print("YELLOW")
        traffic_lights.set_state(Yellow_light())

    def red(self, traffic_lights):
        print("RED")
        traffic_lights.set_state(Red_light())


class Yellow_light(State):
    def green(self, traffic_lights):
        print("GREEN")
        traffic_lights.set_state(Green_light())

    def yellow(self, traffic_lights):
        print("YELLOW")

    def red(self, traffic_lights):
        print("RED")
        traffic_lights.set_state(Red_light())

class Red_light(State):
    def green(self, traffic_lights):
        print("GREEN")
        traffic_lights.set_state(Green_light())

    def yellow(self, traffic_lights):
        print("YELLOW")
        traffic_lights.set_state(Yellow_light())

    def red(self, traffic_lights):
        print("RED")

class Light:
    def __init__(self):
        self.state = Green_light()

    def set_state(self, state):
        self.state = state

    def green(self):
        self.state.green(self)

    def yellow(self):
        self.state.yellow(self)

    def red(self):
        self.state.red(self)

def main():
    flashlight = Light()
    minutes = int(input()) % 6
    color_mapping = {
        0: flashlight.green,
        1: flashlight.green,
        2: flashlight.green,
        3: flashlight.yellow,
        4: flashlight.red,
        5: flashlight.red
    }
    color_mapping[minutes]()

if __name__ == "__main__":
    main()