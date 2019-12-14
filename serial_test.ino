boolean state = 0;
char value[20] = "Hello there";
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(value);
  delay(1000);
  state = !state;
  digitalWrite(13, state);
}
