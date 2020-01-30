from util import hex2rgb


def parse(leds, data, logger):
    if "name" in data:
        logger.info("Message parsed")
        led = data["name"]
        if led == "all":
            for led in leds:
                set_led(data[led], data)
        elif led in leds:
            set_led(data[led], data)
    else:
        logger.warning("Message does not contain useful information")


def set_led(led, data):
    if data["type"] == "static":
        led.set_static_color(hex2rgb(data["color"]))
    elif data["type"] == "animation":
        led.start_animation(data["animationType"],
                            float(data["animationSpeed"]))
