#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

volatile uint8_t cnt = 0;

ISR(TIMER0_OVF_vect)
{
	cnt+=1;
}

void main (void){
	DDRD = 1<<1;
	
	TCCR0 = 0x9;
	TIMSK = 0x1;
	
	sei();
	while(1) {
		PORTD &= ~(1<<1);
		PORTD |= (cnt&1)?1:0;
	}
}