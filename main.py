from hcsr04 import HCSR04
from time import sleep

from machine import Pin
import neopixel

TRIGGER_PIN = 12
ECHO_PIN = 13

DIN_PIN = 5

MAX_BRIGHTNESS = 50
NUM_LEDS = 50

DISTANCE_THRES_MM = 500

class ClosetLights:
    def __init__(self):
        self.state = 'start'
        self.sensor = HCSR04(
            trigger_pin=TRIGGER_PIN,
            echo_pin=ECHO_PIN,
        )

        self.neo = neopixel.NeoPixel(Pin(DIN_PIN), NUM_LEDS)


    def _turn_on(self, s):
        for i in range(NUM_LEDS):
            self.neo[i] = (s, s, s)
        self.neo.write()
        self.state = 'on'


    def _turn_off(self):
        for i in range(NUM_LEDS):
            self.neo[i] = (0, 0, 0)
        self.neo.write()
        self.state = 'off'

    def _fade_on(self):
        for s in range(0, NUM_LEDS, 1):
            self._turn_on(s)
            sleep(0.01)

    def _fade_off(self):
        for s in range(NUM_LEDS, -1, -1):
            self._turn_on(s)
            sleep(0.01)
        self._turn_off()

    def _blink(self, sleep_time=0.5):
        self._fade_on()
        sleep(sleep_time)
        self._fade_off()

    def _neo_walk_on(self):
        for i in range(NUM_LEDS):
            self.neo[i] = (MAX_BRIGHTNESS, MAX_BRIGHTNESS, MAX_BRIGHTNESS)
            self.neo.write()
            sleep(0.02)
        self.state = 'on'

    def _neo_walk_off(self):
        for i in range(NUM_LEDS - 1, -1, -1):
            self.neo[i] = (0, 0, 0)
            self.neo.write()
            sleep(0.02)

        self.state = 'off'

    def _neo_color_walk_on(self):
        for i in range(NUM_LEDS):
            self.neo[i] = (0, MAX_BRIGHTNESS, 0)
            self.neo.write()
            sleep(0.02)
        for i in range(NUM_LEDS):
            self.neo[i] = (MAX_BRIGHTNESS, MAX_BRIGHTNESS, 0)
            self.neo.write()
            sleep(0.02)
        for i in range(NUM_LEDS):
            self.neo[i] = (MAX_BRIGHTNESS, MAX_BRIGHTNESS, MAX_BRIGHTNESS)
            self.neo.write()
            sleep(0.02)
        self.state = 'on'


    # doesn't work
    # TODO:
    # problem is that a low value happens every so often and averages things significantly
    # consider using a p90 or something
    def _measure(self):
        distances = []
        for _ in range(5):
            distances.append(self.sensor.distance_mm())
        return sum(distances) / len(distances)


    def _run_once(self):
        # distance = self._measure()
        distance = self.sensor.distance_mm()
        print("dist:", distance)

        if distance >= DISTANCE_THRES_MM:
            if self.state == 'start':
                print("lights blinking five times")
                # for _ in range(2):
                #     self._blink()
                self._neo_color_walk_on()

            elif self.state == 'off':
                print("light animation")
                self._neo_walk_on()

        else:
            print("lights off")
            self._neo_walk_off()


    def run(self):
        while True:
            self._run_once()
            sleep(0.5)


if __name__ == "__main__":
    closetlights = ClosetLights()
    closetlights.run()
