import threading
import time
import colorsys

from random import randint


class AnimationHandler(object):
    def __init__(self, led):
        self.led = led
        self.animationSpeed = 1
        self.animationRunning = False
        self.animationType = Animation()
        self.thread = threading.Thread(target=self.animation)

    def set_animation_type(self, animation_type):
        if animation_type == "breathing":
            self.animationType = AnimationBreathing(self.led.get_color())
        elif animation_type == "random":
            self.animationType = AnimationRandom()
        elif animation_type == "colorcircle":
            self.animationType = AnimationColorCircle()
        elif animation_type == "colorcirclebreathing":
            self.animationType = AnimationColorCircleBreathing()
        elif animation_type == "randombreathing":
            self.animationType = AnimationRandomBreathing()

    def set_animation_speed(self, animation_speed):
        self.animationSpeed = animation_speed

    def start(self):
        if not self.animationRunning:
            self.animationRunning = True
            self.thread.start()

    def stop(self):
        if self.animationRunning:
            self.animationRunning = False
            self.thread.join()
            self.thread = threading.Thread(target=self.animation)

    def is_running(self):
        return self.animationRunning

    def animation(self):
        while self.animationRunning:
            self.led.set_color(self.animationType.next_color())
            time.sleep(self.animationType.get_delay() * 1 / self.animationSpeed)


class Animation(object):
    pass


class AnimationAbstractBreathing(Animation):
    def __init__(self):
        self.down = True
        self.percentage = 1

    def breath(self):
        if self.down:
            if self.percentage > 0:
                self.percentage -= 0.01
            else:
                self.down = False
                self.percentage += 0.01
        else:
            if self.percentage < 1:
                self.percentage += 0.01
            else:
                self.down = True
                self.percentage -= 0.01


class AnimationOff(Animation):
    @staticmethod
    def next_color():
        return 0, 0, 0

    @staticmethod
    def get_delay():
        return 0


class AnimationRandom(Animation):
    @staticmethod
    def next_color():
        return randint(0, 255), randint(0, 255), randint(0, 255)

    @staticmethod
    def get_delay():
        return 0.5


class AnimationBreathing(AnimationAbstractBreathing):
    def __init__(self, color):
        super().__init__()
        multiplier = 255 / max(color)
        self.color = (round(multiplier * color[0]),
                      round(multiplier * color[1]),
                      round(multiplier * color[2]))

    def next_color(self):
        self.breath()
        return (round(self.percentage * self.color[0]),
                round(self.percentage * self.color[1]),
                round(self.percentage * self.color[2]))

    @staticmethod
    def get_delay():
        return 0.05


class AnimationColorCircle(Animation):
    def __init__(self):
        self.hue = 0

    def next_color(self):
        self.hue = (self.hue + 1) % 360
        color = colorsys.hsv_to_rgb(self.hue / 360, 1, 1)
        return (round(255 * color[0]),
                round(255 * color[1]),
                round(255 * color[2]))

    @staticmethod
    def get_delay():
        return 0.05


class AnimationColorCircleBreathing(AnimationAbstractBreathing):
    def __init__(self):
        super().__init__()
        self.hue = 0

    def next_color(self):
        self.breath()
        if not self.percentage:
            self.hue = (self.hue + 50) % 360
        color = colorsys.hsv_to_rgb(self.hue / 360, 1, 1)
        return (round(self.percentage * 255 * color[0]),
                round(self.percentage * 255 * color[1]),
                round(self.percentage * 255 * color[2]))

    @staticmethod
    def get_delay():
        return 0.05


class AnimationRandomBreathing(AnimationAbstractBreathing):
    def __init__(self):
        super().__init__()
        self.color = (4 * randint(0, 63), 4 * randint(0, 63), 4 * randint(0, 63))

    def next_color(self):
        self.breath()
        if not self.percentage:
            self.color = (4 * randint(0, 63), 4 * randint(0, 63), 4 * randint(0, 63))
        return (round(self.percentage * self.color[0]),
                round(self.percentage * self.color[1]),
                round(self.percentage * self.color[2]))

    @staticmethod
    def get_delay():
        return 0.05
