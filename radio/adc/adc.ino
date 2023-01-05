void setup() {
  Serial.begin(9600);

  Serial.println(0);
  delay(1000);
}

void loop() {
  Serial.println(analogRead(A3));
  delay(10);
}
