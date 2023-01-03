import time
from dfplayermini import Player
from machine import Pin

def run():
    player_rx = 17
    player_tx = 16
    led = Pin(19, Pin.OUT)
    button = Pin(0, Pin.PULL_UP)
    player= Player (player_tx, player_rx)
    player.volume(20)
    button_down = False

    print("hello")

    while True:
        if not button.value() and not button_down:
            print("down")
            led.on()
            player.play(1)
            button_down = True
        if button_down and button.value():
            led.off()
            button_down = False

        time.sleep(1)

