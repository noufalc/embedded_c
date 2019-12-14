boolean toggle = 0;
void setup() {
   cli();
   TCCR0A = 0;
   TCCR0B = 0;
   TCNT0 = 0;
   
   OCR0A = 150;
   TCCR0B |= (1 << CS02) ;  
   TCCR0A |= (1 << WGM01); //PWM for Normal port opertion
   TIMSK0 |= (1 << OCIE0A);
   sei();
}


ISR(TIMER0_COMPA_vect){//timer0 interrupt 2kHz toggles pin 8
//generates pulse wave of frequency 2kHz/2 = 1kHz (takes two cycles for full wave- toggle high then toggle low)
  if (toggle){
    digitalWrite(8,HIGH);
    toggle = 0;
  }
  else{
    digitalWrite(8,LOW);
    toggle = 1;
  }
}

void loop() {
}
