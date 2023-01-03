// #include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>

const uint8_t POT = 4;

DFRobotDFPlayerMini sound;
DFRobotDFPlayerMini noise;

// SoftwareSerial serialPort; // RX, TX

void setup()
{
  Serial.begin(115200);

  Serial2.begin(9600);
  // serialPort.begin(9600, SWSERIAL_8N1, 18, 19, false);

  // initializing DFPlayer ... (may take 3~5 seconds)
  if (!sound.begin(Serial2))
  {
    Serial.println("unable to begin");

    while (true)
    {
      delay(1);
    }
  }
  Serial.println("sound mini online");
  // if (!noise.begin(serialPort))
  // {
  //   Serial.println("unable to begin");

  //   while (true)
  //   {
  //     delay(1);
  //   }
  // }
  Serial.println("noise mini online");

  sound.volume(10); // set volume value. From 0 to 30
  // noise.volume(10);
  sound.play(1);    // play the first mp3
  // noise.play(1);
}

void loop()
{
  static unsigned long timer = millis();

  if (millis() - timer > 10000)
  {
    timer = millis();
    sound.next(); // play next mp3 every 10 second.
    // noise.next();
  }

  // other code here
  Serial.println(analogRead(A10));
  delay(100);
}
