# Akademie_Objects

## Referenzen

- https://docs.micropython.org/en/latest/esp32/quickref.html#installing-micropython
- https://docs.micropython.org/en/latest/esp32/general.html
- https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299
- [esp32 pinout](https://raw.githubusercontent.com/AchimPieters/esp32-homekit-camera/master/Images/ESP32-38%20PIN-DEVBOARD.png)
- https://learn.adafruit.com/welcome-to-circuitpython
- https://learn.adafruit.com/getting-started-with-web-workflow-using-the-code-editor
- https://learn.adafruit.com/circuitpython-with-esp32-quick-start

## Micropython libraries

- [DFPlayer](https://github.com/lavron/micropython-dfplayermini)

## Circuitpython librarires

- [DFPlayer](https://github.com/bablokb/circuitpython-dfplayer)

## Micropython Installationanweisungen

1. Tool zum esp flashen installieren mit `pip install esptool`
2. den flash löschon mit `esptool.py --port /dev/ttyUSB0* erase_flash` \*durch das entsprechende Serial port ersetzen
3. Die richtige Firmware von https://micropython.org/download/#esp32 flashen mit `esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20190125-v1.10.bin`
4. Mit `screen /dev/ttyUSB0* 115200` Kann eine Serial Connection zur REPL (eine art Python Konsole) aufgebaut werden \*durch das entsprechende Serial port ersetzen
5. Zum flashen von Skripten ampy installieren mit `pip install adafruit-ampy`
6. `main.py` auf den esp flashen mit `ampy --port /dev/ttyUSB0* put main.py` \*durch das entsprechende Serial port ersetzen

## Circuitpython Installationanweisungen

1. Tool zum esp flashen installieren mit `pip install esptool`
2. den flash löschon mit `esptool.py --port /dev/ttyUSB0* erase_flash` \*durch das entsprechende Serial port ersetzen
3. die richtige Firmware von https://circuitpython.org/downloads (wir haben Adafruit Feather HUZZAH32 verwendet) flashen mit `esptool.py --chip esp32 --port /dev/ttyUSB0* --baud 460800 write_flash -z 0x0 adafruit-circuitpython-adafruit_feather_huzzah32-en_US-8.0.0-beta.6.bin`
4. an die REPL verbinden mit `screen /dev/ttyUSB0* 115200` und die richtigen Verbindingsdaten angeben mit:
   ```
   f = open('settings.toml', 'w')
   f.write('CIRCUITPY_WIFI_SSID = "wifissid"\n')
   f.write('CIRCUITPY_WIFI_PASSWORD = "wifipassword"\n')
   f.write('CIRCUITPY_WEB_API_PASSWORD = "webpassword"\n')
   f.close()
   ```
   diese Zeilen Zeile für Zeile eingeben und den entsprechenden Netzwerknamen, Passwort, etc. angeben
5. die IP des esp herausfinden mit:
   ```
   import wifi
   print("My IP address is", wifi.radio.ipv4_address)
   ```
6. entweder über http://circuitpython.local oder über die IP des esp (z.B. http://192.168.0.121) über den browser verbinden
7. Bibliotheken von https://circuitpython.org/libraries (wir nutzen cicuitpython 8.x) in den lib ordner kopieren

# Notizen

- um `screen` zu schließen, `screen -ls` eingeben und dann mit der ID `screen -X -S {ID} quit`
