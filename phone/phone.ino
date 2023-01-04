#include <HardwareSerial.h>
#include <DFRobotDFPlayerMini.h>

DFRobotDFPlayerMini noise;

void setup()
{
  Serial.begin(115200);

  Serial2.begin(9600);

  // initializing DFPlayer (may take 3~5 seconds)
  if (!noise.begin(Serial2))
  {
    Serial.println("unable to begin");

    while (true)
    {
      delay(1);
    }
  }
  Serial.println("noise online");

  noise.volume(10);  // set volume value. From 0 to 30
  noise.randomAll(); // play random mp3
}

void loop()
{
  static unsigned long timer = millis();

  if (millis() - timer > 10000)
  {
    timer = millis();
    noise.next(); // play next mp3 every 10 second.
    Serial.println("play");
  }

  // other code here
}
