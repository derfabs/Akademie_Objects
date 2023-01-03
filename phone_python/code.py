import board
import time
from simpleio import DigitalIn, DigitalOut
from digitalio import Pull
from busio import UART
from adafruit_debouncer import Debouncer
from DFPlayer import DFPlayer

# initializing pins
led = DigitalOut(board.D23)
switch = Debouncer(DigitalIn(board.D22, pull=Pull.UP))

# for only triigering once per press
switch_down = False

# waiting for the player (to not overwhelm it)
time.sleep(3)

# initializing serial connection
uart = UART(tx=board.D17, rx=board.D16, baudrate=9600)

# initailizing player
player = DFPlayer(uart, volume=30)
# stopping playback at start
player.stop()

while True:
  # updateing the button status (part of debouncing the button)
  switch.update()

  # if the switch gets pressed down, play a random track form the sd card
  if not switch.value and not switch_down:
    player.random()
    switch_down = True
    
  # if the switch goes up, stop playing
  if switch.value and switch_down:
    player.stop()
    switch_down = False