from animation import AnimationHandler


class Led:
    def __init__(self, pizw, pins):
        self.pizw = pizw
        self.animation = AnimationHandler(self)
        self.color = (0, 0, 0)
        self.pins = pins

    def get_color(self):
        return self.color

    def set_static_color(self, color):
        self.animation.stop()
        self.color = color
        self.set_color(color)

    def set_color(self, color):
        self.color = color
        self.pizw.set_PWM_dutycycle(self.pins[0], color[0])
        self.pizw.set_PWM_dutycycle(self.pins[1], color[1])
        self.pizw.set_PWM_dutycycle(self.pins[2], color[2])

    def start_animation(self, animation_type, animation_speed):
        if animation_type == "stop":
            self.animation.stop()
        else:
            self.animation.set_animation_type(animation_type)
            self.animation.set_animation_speed(animation_speed)
            self.animation.start()
