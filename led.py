from animation import AnimationHandler


class Led:
    def __init__(self, name, pizw, pins):
        self.name = name
        self.pizw = pizw
        self.animation = AnimationHandler(self)
        self.color = (0, 0, 0)
        self.pins = pins

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def set_static_color(self, color):
        self.animation.stop()
        self.color = color
        self.set_color(color)

    def set_color(self, color):
        self.color = color
        for i in range(3):
            if color[i] > 255 or color[i] < 0:
                raise Exception
        for i in range(3):
            self.pizw.set_PWM_dutycycle(self.pins[i], color[i])

    def start_animation(self, animation_type, animation_speed):
        if animation_type == "stop":
            self.animation.stop()
        else:
            self.animation.set_animation_type(animation_type)
            self.animation.set_animation_speed(animation_speed)
            self.animation.start()
