import pigpio
import json
import logging

from util import hex2rgb
from led import Led


class Controller:

    def __init__(self, logger, config_path):
        self.logger = logging.getLogger(__name__)
        with open(config_path, "r") as f:
            config = json.load(f)
            f.close()
        self.leds = dict()
        pizw = pigpio.pi()
        for led_group in config.get("leds"):
            self.leds[led_group.get("name")] = Led(led_group.get("name"), pizw, led_group.get("pins"))
        self.web_config = dict()
        self.web_config["leds"] = list(self.leds.keys())
        self.logger.info("Configuration from {} loaded with {} LED(s)".format(config_path, len(self.leds)))

    def parse(self, data):
        if "name" in data:
            self.logger.info("Message parsed")
            led_name = data["name"]
            if led_name == "all":
                for led in self.leds.values():
                    self.set_led(led, data)
            elif led_name in self.leds:
                self.set_led(self.leds[led_name], data)
        else:
            self.logger.warning("Message does not contain useful information")

    def set_led(self, led, data):
        if data["type"] == "static":
            led.set_static_color(hex2rgb(data["color"]))
            self.logger.info("Led {} set to static {}".format(led.get_name(), data["color"]))
        elif data["type"] == "animation":
            led.start_animation(data["animationType"],
                                float(data["animationSpeed"]))
            self.logger.info("Led {} set to animation {}".format(led.get_name(), data["animationType"]))

    def get_webconfig(self):
        return self.web_config
