# Akademie_Objects

## Referenzen

- https://docs.micropython.org/en/latest/esp32/quickref.html#installing-micropython

## Installationanweisungen

1. Tool zum esp flashen installieren mit `pip install esptool`
2. den flash löschon mit `esptool.py --port /dev/ttyUSB0* erase_flash` \*durch das entsprechende Serial port ersetzen
3. Die richtige Firmware von https://micropython.org/download/#esp32 flashen mit `esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20190125-v1.10.bin`
4. Mit `screen /dev/ttyUSB0* 115200` Kann eine Serial Connection zur REPL (eine art Python Konsole) aufgebaut werden \*durch das entsprechende Serial port ersetzen
5. Zum flashen von Skripten ampy installieren mit `pip install adafruit-ampy`
