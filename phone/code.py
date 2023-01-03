import board
import time
import simpleio
import digitalio
from adafruit_debouncer import Debouncer

led = simpleio.DigitalOut(board.D14)
switch = Debouncer(simpleio.DigitalIn(board.D12, pull=digitalio.Pull.UP))

while True:
  switch.update()
  led.value = not switch.value