#include "DFRobotDFPlayerMini.h"

DFRobotDFPlayerMini myDFPlayer;

void setup()
{
  Serial.begin(115200);

  Serial2.begin(9600);

  // initializing DFPlayer ... (may take 3~5 seconds)
  if (!myDFPlayer.begin(Serial2))
  {
    Serial.println("unable to begin");

    while (true)
    {
      delay(1);
    }
  }
  Serial.println("DFPlayer mini online");

  myDFPlayer.volume(10); // set volume value. From 0 to 30
  myDFPlayer.play(1);    // play the first mp3
}

void loop()
{
  static unsigned long timer = millis();

  if (millis() - timer > 10000)
  {
    timer = millis();
    myDFPlayer.next(); // play next mp3 every 10 second.
  }

  // other code here
}
