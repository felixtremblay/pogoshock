
uint8_t outputPin = 2;

void setup() {
  pinMode(outputPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  while(!Serial.available());
  uint16_t duration = Serial.parseInt();
  if(duration != 0){
    digitalWrite(outputPin, HIGH);
    delay(duration);
    digitalWrite(outputPin, LOW);
    Serial.read();
  }
}
