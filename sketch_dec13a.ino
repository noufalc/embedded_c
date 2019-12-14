#define READER1 0 
#define READER2 1



char reader1[128] = {0};// string buffer to store card1 bitpattern
char reader2[128] = {0};
// string buffer to store card1 bitpattern
int bitCount[2];
void clearBuffer(char string[], int n) {
  for(int i = 0; i < n; i++)
  {
    string[i] = 0;
  }
}

void setup() {
   Serial.begin(1000000);
   cli();
   attachInterrupt(digitalPinToInterrupt(2), readValue1D0, RISING);
   attachInterrupt(digitalPinToInterrupt(3), readValue1D1, RISING);
   TCCR0A = 0;
   TCCR0B = 0;
   TCNT0 = 0;
   //TCCR0B &= 0xF8;
   TCCR0A |= (1 << WGM01); //PWM for Normal port opertion
   TIMSK0 |= (1 << OCIE0A);
   sei();
}


void readValue1D0() {
  reader1[bitCount[READER1]++] = '0';
  OCR0A = 150;
  TCNT0 = 0;
  TCCR0B |= (1 << CS02); // start the timer for 2.5ms, after that start the timer  ISR
  
}

void readValue1D1() {
  reader1[bitCount[READER1]++] = '1';
  OCR0A = 150;
  TCNT0 = 0;
  TCCR0B |= (1 << CS02);
}

ISR(TIMER0_COMPA_vect){
  TCCR0B &= 0xF8;  //11111000
  Serial.println(reader1);
  clearBuffer(reader1, 128);
  bitCount[READER1] = 0;
}

void loop() {

}
