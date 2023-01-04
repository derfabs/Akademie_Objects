#include <HardwareSerial.h>
#include <DFRobotDFPlayerMini.h>

DFRobotDFPlayerMini sound;
DFRobotDFPlayerMini noise;

void setup()
{
  Serial.begin(115200);

  Serial1.begin(9600, SERIAL_8N1, 32, 33);
  Serial2.begin(9600);

  // initializing DFPlayer (may take 3~5 seconds)
  if (!sound.begin(Serial1))
  {
    Serial.println("unable to begin sound");

    while (true)
    {
      delay(1);
    }
  }
  Serial.println("sound online");
  if (!noise.begin(Serial2))
  {
    Serial.println("unable to begin noise");

    while (true)
    {
      delay(1);
    }
  }
  Serial.println("noise online");

  sound.volume(20);  // set volume value. From 0 to 30
  noise.volume(10);  // set volume value. From 0 to 30
  sound.randomAll(); // play random mp3
  noise.randomAll(); // play random mp3
}

void loop()
{
  static unsigned long timer = millis();

  if (millis() - timer > 10000)
  {
    timer = millis();
    sound.next(); // play next mp3 every 10 second.
    noise.next(); // play next mp3 every 10 second.
    Serial.println("play");
  }

  // other code here
}
