import asyncio
import websockets
import json
import pigpio
import logging

from util import hex2rgb
from led import Led


def set_led(led, data):
    if data["type"] == "static":
        leds[led].set_static_color(hex2rgb(data["color"]))
    elif data["type"] == "animation":
        leds[led].start_animation(data["animationType"],
                                  float(data["animationSpeed"]))


async def send_web_config(websocket):
    await websocket.send(json.dumps(web_config))


async def consumer_handler(websocket, path):
    logger.info("Client connected")
    await send_web_config(websocket)
    async for message in websocket:
        logger.info("Message recived: " + message)
        try:
            data = json.loads(message)
            if "name" in data:
                logger.info("Message parsed")
                led = data["name"]
                if led == "all":
                    for led in leds:
                        set_led(led, data)
                elif led in leds:
                    set_led(led, data)
            else:
                logger.warning("Message does not contain useful information")
        except ValueError:
            logger.warning("Message could not be parsed")


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='app.log', filemode='a', format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Application started")
CONFIG_FILE = "config.json"
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)
leds = dict()
pizw = pigpio.pi()
for led_strip in config.get("leds"):
    leds[led_strip.get("name")] = Led(pizw, led_strip.get("pins"))
web_config = dict()
web_config["leds"] = list(leds.keys())
logger.info("Configuration loaded with {} LED(s)".format(len(leds)))

start_server = websockets.serve(consumer_handler, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
