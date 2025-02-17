import sys
from abc import ABC, abstractmethod
from math import cos, sin, pi

import pyray
from raylib import colors

pyray.init_window(800, 600, 'Excavator example')


class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)


class RLScene(ABC):
    bg_color = colors.BLACK

    def __init__(self):
        self.scene_over = False
        self.objects = []

    def draw(self):
        pyray.clear_background(self.bg_color)
        for item in self.objects:
            item.draw()

    def process_events(self):
        if pyray.window_should_close():
            self.scene_over = True
        self.process_events()

    def process_event(self):
        pass

    @abstractmethod
    def process_logic(self):
        for item in self.objects:
            item.logic()

    def main_loop(self):
        while not self.scene_over:
            self.process_event()
            self.process_logic()
            pyray.begin_drawing()
            self.draw()
            pyray.end_drawing()
            pyray.wait_time(0.01)


class Command(ABC):
    def __init__(self, scene):
        self.scene = scene

    @abstractmethod
    def execute(self):
        pass


class UpCommand(Command):
    def execute(self):
        self.scene.excavator.move()
        self.scene.buttons['up'].set_enabled(True)
        self.scene.buttons['down'].set_enabled(False)


class DownCommand(Command):
    def execute(self):
        self.scene.excavator.stop()
        self.scene.buttons['down'].set_enabled(True)
        self.scene.buttons['up'].set_enabled(False)


class LeftCommand(Command):
    def execute(self):
        self.scene.excavator.rotate(-15)
        self.scene.buttons['left'].set_enabled(True)
        self.scene.buttons['right'].set_enabled(False)


class RightCommand(Command):
    def execute(self):
        self.scene.excavator.rotate(15)
        self.scene.buttons['right'].set_enabled(True)
        self.scene.buttons['left'].set_enabled(False)


class GameScene(RLScene):
    keydown_events = {
        pyray.KeyboardKey.KEY_W: UpCommand,
        pyray.KeyboardKey.KEY_S: DownCommand,
        pyray.KeyboardKey.KEY_A: LeftCommand,
        pyray.KeyboardKey.KEY_D: RightCommand,
    }
    def __init__(self):
        super().__init__()
        self.excavator = Excavator(200, 200)
        self.buttons = {
            'up': StateRect(100, 500, 20, 20, colors.GREEN, colors.RED),
            'down': StateRect(100, 530, 20, 20, colors.GREEN, colors.RED),
            'left': StateRect(70, 530, 20, 20, colors.GREEN, colors.RED),
            'right': StateRect(130, 530, 20, 20, colors.GREEN, colors.RED),
        }
        self.objects.append(self.excavator)
        self.objects += self.buttons.values()

    def process_logic(self):
        super().process_logic()

    def process_event(self):
        for key in self.keydown_events.keys():
            if pyray.is_key_pressed(key):
                self.keydown_events[key](self).execute()


class RLObject(ABC):
    @abstractmethod
    def draw(self):
        pass

    def logic(self):
        pass


class Excavator(RLObject):
    def __init__(self, x, y):
        super().__init__()
        img = pyray.load_image('excavator.png')
        self.rotated_texture = self.texture = pyray.load_texture_from_image(img)
        pyray.unload_image(img)
        self.x = x
        self.y = y
        self.w = self.rotated_texture.width
        self.h = self.rotated_texture.height
        self.rect = pyray.Rectangle(self.x, self.y, self.w, self.h)
        self.direction = 0
        self.speed = 0
        self.max_speed = 1

    def draw(self):
        self.rect.x = self.x - self.rect.width // 2
        self.rect.y = self.y - self.rect.height // 2
        pyray.draw_texture_pro(
            self.rotated_texture,
            pyray.Rectangle(0, 0, self.w, self.h),
            self.rect,
            pyray.Vector2(self.w // 2, self.h // 2),
            self.direction,
            colors.WHITE
        )

    def move(self):
        self.speed = self.max_speed

    def stop(self):
        self.speed = 0

    def step(self):
        self.x += cos(self.direction / 180 * pi) * self.speed
        self.y += sin(self.direction / 180 * pi) * self.speed

    def rotate(self, angle):
        self.direction += angle

    def logic(self):
        self.step()


class StateRect(RLObject):
    def __init__(self, x, y, width, height, color_enabled, color_disabled):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_enabled = color_enabled
        self.color_disabled = color_disabled
        self.enabled = False

    def draw(self):
        color = self.color_enabled if self.enabled else self.color_disabled
        pyray.draw_rectangle(self.x, self.y, self.width, self.height, color)

    def set_enabled(self, enabled):
        self.enabled = enabled


if __name__ == '__main__':
    gs = GameScene()
    gs.main_loop()
    sys.exit()