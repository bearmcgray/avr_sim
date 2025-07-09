# I/O registers

# Input Pins, Port F
PINF =         0X20

# Input Pins, Port E
PINE =         0X21

# Data Direction Register, Port E
DDRE =         0X22

# Data Register, Port E
PORTE =        0X23

# ADC Data Register
ADCW =         0X24
#ifndef __ASSEMBLER__
ADC =          0X24
#endif
ADCL =         0X24
ADCH =         0X25

# ADC Control and status register
ADCSR =        0X26
ADCSRA =       0X26 # new name in datasheet (2467E-AVR-05/02)

# ADC Multiplexer select
ADMUX =        0X27

# Analog Comparator Control and Status Register
ACSR =         0X28

# USART0 Baud Rate Register Low
UBRR0L =       0X29

# USART0 Control and Status Register B
UCSR0B =       0X2A

# USART0 Control and Status Register A
UCSR0A =       0X2B

# USART0 I/O Data Register
UDR0 =         0X2C

# SPI Control Register
SPCR =         0X2D

# SPI Status Register
SPSR =         0X2E

# SPI I/O Data Register
SPDR =         0X2F

# Input Pins, Port D
PIND =         0X30

# Data Direction Register, Port D
DDRD =         0X31

# Data Register, Port D
PORTD =        0X32

# Input Pins, Port C
PINC =         0X33

# Data Direction Register, Port C
DDRC =         0X34

# Data Register, Port C
PORTC =        0X35

# Input Pins, Port B
PINB =         0X36

# Data Direction Register, Port B
DDRB =         0X37

# Data Register, Port B
PORTB =        0X38

# Input Pins, Port A
PINA =         0X39

# Data Direction Register, Port A
DDRA =         0X3A

# Data Register, Port A
PORTA =        0X3B

# EEPROM Control Register
EECR =         0X3C

# EEPROM Data Register
EEDR =         0X3D

# EEPROM Address Register
EEAR =         0X3E
EEARL =        0X3E
EEARH =        0X3F

# Special Function I/O Register
SFIOR =        0X40

# Watchdog Timer Control Register
WDTCR =        0X41

# On-chip Debug Register
OCDR =         0X42

# Timer2 Output Compare Register
OCR2 =         0X43

# Timer/Counter 2
TCNT2 =        0X44

# Timer/Counter 2 Control register
TCCR2 =        0X45

# T/C 1 Input Capture Register
ICR1 =         0X46
ICR1L =        0X46
ICR1H =        0X47

# Timer/Counter1 Output Compare Register B
OCR1B =        0X48
OCR1BL =       0X48
OCR1BH =       0X49

# Timer/Counter1 Output Compare Register A
OCR1A =        0X4A
OCR1AL =       0X4A
OCR1AH =       0X4B

# Timer/Counter 1
TCNT1 =        0X4C
TCNT1L =       0X4C
TCNT1H =       0X4D

# Timer/Counter 1 Control and Status Register
TCCR1B =       0X4E

# Timer/Counter 1 Control Register
TCCR1A =       0X4F

# Timer/Counter 0 Asynchronous Control & Status Register
ASSR =         0X50

# Output Compare Register 0
OCR0 =         0X51

# Timer/Counter 0
TCNT0 =        0X52

# Timer/Counter 0 Control Register
TCCR0 =        0X53

# MCU Status Register
MCUSR =        0X54
MCUCSR =       0X54 # new name in datasheet (2467E-AVR-05/02)

# MCU general Control Register
MCUCR =        0X55

# Timer/Counter Interrupt Flag Register
TIFR =         0X56

# Timer/Counter Interrupt MaSK register
TIMSK =        0X57

# External Interrupt Flag Register
EIFR =         0X58

# External Interrupt MaSK register
EIMSK =        0X59

# External Interrupt Control Register B
EICRB =        0X5A

# RAM Page Z select register
RAMPZ =        0X5B

# XDIV Divide control register
XDIV =         0X5C

# 0x3D..0x3E SP

# 0x3F SREG

# Extended I/O registers

# Data Direction Register, Port F
DDRF =         0x61

# Data Register, Port F
PORTF =        0x62

# Input Pins, Port G
PING =         0x63

# Data Direction Register, Port G
DDRG =         0x64

# Data Register, Port G
PORTG =        0x65

# Store Program Memory Control and Status Register
SPMCR =        0x68
SPMCSR =       0x68 # new name in datasheet (2467E-AVR-05/02)

# External Interrupt Control Register A
EICRA =        0x6A

# External Memory Control Register B
XMCRB =        0x6C

# External Memory Control Register A
XMCRA =        0x6D

# Oscillator Calibration Register
OSCCAL =       0x6F

# 2-wire Serial Interface Bit Rate Register
TWBR =         0x70

# 2-wire Serial Interface Status Register
TWSR =         0x71

# 2-wire Serial Interface Address Register
TWAR =         0x72

# 2-wire Serial Interface Data Register
TWDR =         0x73

# 2-wire Serial Interface Control Register
TWCR =         0x74

# Time Counter 1 Output Compare Register C
OCR1C =        0x78
OCR1CL =       0x78
OCR1CH =       0x79

# Timer/Counter 1 Control Register C
TCCR1C =       0x7A

# Extended Timer Interrupt Flag Register
ETIFR =        0x7C

# Extended Timer Interrupt Mask Register
ETIMSK =       0x7D

# Timer/Counter 3 Input Capture Register
ICR3 =         0x80
ICR3L =        0x80
ICR3H =        0x81

# Timer/Counter 3 Output Compare Register C
OCR3C =        0x82
OCR3CL =       0x82
OCR3CH =       0x83

# Timer/Counter 3 Output Compare Register B
OCR3B =        0x84
OCR3BL =       0x84
OCR3BH =       0x85

# Timer/Counter 3 Output Compare Register A
OCR3A =        0x86
OCR3AL =       0x86
OCR3AH =       0x87

# Timer/Counter 3 Counter Register
TCNT3 =        0x88
TCNT3L =       0x88
TCNT3H =       0x89

# Timer/Counter 3 Control Register B
TCCR3B =       0x8A

# Timer/Counter 3 Control Register A
TCCR3A =       0x8B

# Timer/Counter 3 Control Register C
TCCR3C =       0x8C

# USART0 Baud Rate Register High
UBRR0H =       0x90

# USART0 Control and Status Register C
UCSR0C =       0x95

# USART1 Baud Rate Register High
UBRR1H =       0x98

# USART1 Baud Rate Register Low
UBRR1L =       0x99

# USART1 Control and Status Register B
UCSR1B =       0x9A

# USART1 Control and Status Register A
UCSR1A =       0x9B

# USART1 I/O Data Register
UDR1 =         0x9C

# USART1 Control and Status Register C
UCSR1C =       0x9D


#   The Register Bit names are represented by their bit number (0-7).


# 2-wire Control Register - TWCR
TWINT =        7
TWEA =         6
TWSTA =        5
TWSTO =        4
TWWC =         3
TWEN =         2
TWIE =         0

# 2-wire Address Register - TWAR
TWA6 =         7
TWA5 =         6
TWA4 =         5
TWA3 =         4
TWA2 =         3
TWA1 =         2
TWA0 =         1
TWGCE =        0

# 2-wire Status Register - TWSR
TWS7 =         7
TWS6 =         6
TWS5 =         5
TWS4 =         4
TWS3 =         3
TWPS1 =        1
TWPS0 =        0

# External Memory Control Register A - XMCRA
SRL2 =         6
SRL1 =         5
SRL0 =         4
SRW01 =        3
SRW00 =        2
SRW11 =        1

# External Memory Control Register B - XMCRA
XMBK =         7
XMM2 =         2
XMM1 =         1
XMM0 =         0

# XDIV Divide control register - XDIV
XDIVEN =       7
XDIV6 =        6
XDIV5 =        5
XDIV4 =        4
XDIV3 =        3
XDIV2 =        2
XDIV1 =        1
XDIV0 =        0

# RAM Page Z select register - RAMPZ
RAMPZ0 =       0

# External Interrupt Control Register A - EICRA
ISC31 =        7
ISC30 =        6
ISC21 =        5
ISC20 =        4
ISC11 =        3
ISC10 =        2
ISC01 =        1
ISC00 =        0

# External Interrupt Control Register B - EICRB
ISC71 =        7
ISC70 =        6
ISC61 =        5
ISC60 =        4
ISC51 =        3
ISC50 =        2
ISC41 =        1
ISC40 =        0

# Store Program Memory Control Register - SPMCSR, SPMCR
SPMIE =        7
RWWSB =        6
RWWSRE =       4
BLBSET =       3
PGWRT =        2
PGERS =        1
SPMEN =        0

# External Interrupt MaSK register - EIMSK
INT7 =         7
INT6 =         6
INT5 =         5
INT4 =         4
INT3 =         3
INT2 =         2
INT1 =         1
INT0 =         0

# External Interrupt Flag Register - EIFR
INTF7 =        7
INTF6 =        6
INTF5 =        5
INTF4 =        4
INTF3 =        3
INTF2 =        2
INTF1 =        1
INTF0 =        0

# Timer/Counter Interrupt MaSK register - TIMSK
OCIE2 =        7
TOIE2 =        6
TICIE1 =       5
OCIE1A =       4
OCIE1B =       3
TOIE1 =        2
OCIE0 =        1
TOIE0 =        0

# Timer/Counter Interrupt Flag Register - TIFR
OCF2 =         7
TOV2 =         6
ICF1 =         5
OCF1A =        4
OCF1B =        3
TOV1 =         2
OCF0 =         1
TOV0 =         0

# Extended Timer Interrupt MaSK register - ETIMSK
TICIE3 =       5
OCIE3A =       4
OCIE3B =       3
TOIE3 =        2
OCIE3C =       1
OCIE1C =       0

# Extended Timer Interrupt Flag Register - ETIFR
ICF3 =         5
OCF3A =        4
OCF3B =        3
TOV3 =         2
OCF3C =        1
OCF1C =        0

# MCU general Control Register - MCUCR
SRE =          7
SRW =          6
SRW10 =        6 # new name in datasheet (2467E-AVR-05/02)
SE =           5
SM1 =          4
SM0 =          3
SM2 =          2
IVSEL =        1
IVCE =         0

# MCU Status Register - MCUSR, MCUCSR
JTD =          7
JTRF =         4
WDRF =         3
BORF =         2
EXTRF =        1
PORF =         0

# Timer/Counter Control Register (generic)
FOC =          7
WGM0 =         6
COM1 =         5
COM0 =         4
WGM1 =         3
CS2 =          2
CS1 =          1
CS0 =          0

# Timer/Counter 0 Control Register - TCCR0
FOC0 =         7
WGM00 =        6
COM01 =        5
COM00 =        4
WGM01 =        3
CS02 =         2
CS01 =         1
CS00 =         0

# Timer/Counter 2 Control Register - TCCR2
FOC2 =         7
WGM20 =        6
COM21 =        5
COM20 =        4
WGM21 =        3
CS22 =         2
CS21 =         1
CS20 =         0

# Timer/Counter 0 Asynchronous Control & Status Register - ASSR
AS0 =          3
TCN0UB =       2
OCR0UB =       1
TCR0UB =       0

# Timer/Counter Control Register A (generic)
COMA1 =        7
COMA0 =        6
COMB1 =        5
COMB0 =        4
COMC1 =        3
COMC0 =        2
WGMA1 =        1
WGMA0 =        0

# Timer/Counter 1 Control and Status Register A - TCCR1A
COM1A1 =       7
COM1A0 =       6
COM1B1 =       5
COM1B0 =       4
COM1C1 =       3
COM1C0 =       2
WGM11 =        1
WGM10 =        0

# Timer/Counter 3 Control and Status Register A - TCCR3A
COM3A1 =       7
COM3A0 =       6
COM3B1 =       5
COM3B0 =       4
COM3C1 =       3
COM3C0 =       2
WGM31 =        1
WGM30 =        0

# Timer/Counter Control and Status Register B (generic)
ICNC =         7
ICES =         6
WGMB3 =        4
WGMB2 =        3
CSB2 =         2
CSB1 =         1
CSB0 =         0

# Timer/Counter 1 Control and Status Register B - TCCR1B
ICNC1 =        7
ICES1 =        6
WGM13 =        4
WGM12 =        3
CS12 =         2
CS11 =         1
CS10 =         0

# Timer/Counter 3 Control and Status Register B - TCCR3B
ICNC3 =        7
ICES3 =        6
WGM33 =        4
WGM32 =        3
CS32 =         2
CS31 =         1
CS30 =         0

# Timer/Counter Control Register C (generic)
FOCA =         7
FOCB =         6
FOCC =         5

# Timer/Counter 3 Control Register C - TCCR3C
FOC3A =        7
FOC3B =        6
FOC3C =        5

# Timer/Counter 1 Control Register C - TCCR1C
FOC1A =        7
FOC1B =        6
FOC1C =        5

# On-chip Debug Register - OCDR
IDRD =         7
OCDR7 =        7
OCDR6 =        6
OCDR5 =        5
OCDR4 =        4
OCDR3 =        3
OCDR2 =        2
OCDR1 =        1
OCDR0 =        0

# Watchdog Timer Control Register - WDTCR
WDCE =         4
WDE =          3
WDP2 =         2
WDP1 =         1
WDP0 =         0


#   The ADHSM bit has been removed from all documentation, 
#   as being not needed at all since the comparator has proven 
#   to be fast enough even without feeding it more power.


# Special Function I/O Register - SFIOR
TSM =          7
ACME =         3
PUD =          2
PSR0 =         1
PSR321 =       0

# SPI Status Register - SPSR
SPIF =         7
WCOL =         6
SPI2X =        0

# SPI Control Register - SPCR
SPIE =         7
SPE =          6
DORD =         5
MSTR =         4
CPOL =         3
CPHA =         2
SPR1 =         1
SPR0 =         0

# USART Register C (generic)
UMSEL =        6
UPM1 =         5
UPM0 =         4
USBS =         3
UCSZ1 =        2
UCSZ0 =        1
UCPOL =        0

# USART1 Register C - UCSR1C
UMSEL1 =       6
UPM11 =        5
UPM10 =        4
USBS1 =        3
UCSZ11 =       2
UCSZ10 =       1
UCPOL1 =       0

# USART0 Register C - UCSR0C
UMSEL0 =       6
UPM01 =        5
UPM00 =        4
USBS0 =        3
UCSZ01 =       2
UCSZ00 =       1
UCPOL0 =       0

# USART Status Register A (generic)
RXC =          7
TXC =          6
UDRE =         5
FE =           4
DOR =          3
UPE =          2
U2X =          1
MPCM =         0

# USART1 Status Register A - UCSR1A
RXC1 =         7
TXC1 =         6
UDRE1 =        5
FE1 =          4
DOR1 =         3
UPE1 =         2
U2X1 =         1
MPCM1 =        0

# USART0 Status Register A - UCSR0A
RXC0 =         7
TXC0 =         6
UDRE0 =        5
FE0 =          4
DOR0 =         3
UPE0 =         2
U2X0 =         1
MPCM0 =        0

# USART Control Register B (generic)
RXCIE =        7
TXCIE =        6
UDRIE =        5
RXEN =         4
TXEN =         3
UCSZ =         2
UCSZ2 =        2 # new name in datasheet (2467E-AVR-05/02)
RXB8 =         1
TXB8 =         0

# USART1 Control Register B - UCSR1B
RXCIE1 =       7
TXCIE1 =       6
UDRIE1 =       5
RXEN1 =        4
TXEN1 =        3
UCSZ12 =       2
RXB81 =        1
TXB81 =        0

# USART0 Control Register B - UCSR0B
RXCIE0 =       7
TXCIE0 =       6
UDRIE0 =       5
RXEN0 =        4
TXEN0 =        3
UCSZ02 =       2
RXB80 =        1
TXB80 =        0

# Analog Comparator Control and Status Register - ACSR
ACD =          7
ACBG =         6
ACO =          5
ACI =          4
ACIE =         3
ACIC =         2
ACIS1 =        1
ACIS0 =        0

# ADC Control and status register - ADCSRA
ADEN =         7
ADSC =         6
ADFR =         5
ADIF =         4
ADIE =         3
ADPS2 =        2
ADPS1 =        1
ADPS0 =        0

# ADC Multiplexer select - ADMUX
REFS1 =        7
REFS0 =        6
ADLAR =        5
MUX4 =         4
MUX3 =         3
MUX2 =         2
MUX1 =         1
MUX0 =         0

# Port A Data Register - PORTA
PA7 =          7
PA6 =          6
PA5 =          5
PA4 =          4
PA3 =          3
PA2 =          2
PA1 =          1
PA0 =          0

# Port A Data Direction Register - DDRA
DDA7 =         7
DDA6 =         6
DDA5 =         5
DDA4 =         4
DDA3 =         3
DDA2 =         2
DDA1 =         1
DDA0 =         0

# Port A Input Pins - PINA
PINA7 =        7
PINA6 =        6
PINA5 =        5
PINA4 =        4
PINA3 =        3
PINA2 =        2
PINA1 =        1
PINA0 =        0

# Port B Data Register - PORTB
PB7 =          7
PB6 =          6
PB5 =          5
PB4 =          4
PB3 =          3
PB2 =          2
PB1 =          1
PB0 =          0

# Port B Data Direction Register - DDRB
DDB7 =         7
DDB6 =         6
DDB5 =         5
DDB4 =         4
DDB3 =         3
DDB2 =         2
DDB1 =         1
DDB0 =         0

# Port B Input Pins - PINB
PINB7 =        7
PINB6 =        6
PINB5 =        5
PINB4 =        4
PINB3 =        3
PINB2 =        2
PINB1 =        1
PINB0 =        0

# Port C Data Register - PORTC
PC7 =          7
PC6 =          6
PC5 =          5
PC4 =          4
PC3 =          3
PC2 =          2
PC1 =          1
PC0 =          0

# Port C Data Direction Register - DDRC
DDC7 =         7
DDC6 =         6
DDC5 =         5
DDC4 =         4
DDC3 =         3
DDC2 =         2
DDC1 =         1
DDC0 =         0

# Port C Input Pins - PINC
PINC7 =        7
PINC6 =        6
PINC5 =        5
PINC4 =        4
PINC3 =        3
PINC2 =        2
PINC1 =        1
PINC0 =        0

# Port D Data Register - PORTD
PD7 =          7
PD6 =          6
PD5 =          5
PD4 =          4
PD3 =          3
PD2 =          2
PD1 =          1
PD0 =          0

# Port D Data Direction Register - DDRD
DDD7 =         7
DDD6 =         6
DDD5 =         5
DDD4 =         4
DDD3 =         3
DDD2 =         2
DDD1 =         1
DDD0 =         0

# Port D Input Pins - PIND
PIND7 =        7
PIND6 =        6
PIND5 =        5
PIND4 =        4
PIND3 =        3
PIND2 =        2
PIND1 =        1
PIND0 =        0

# Port E Data Register - PORTE
PE7 =          7
PE6 =          6
PE5 =          5
PE4 =          4
PE3 =          3
PE2 =          2
PE1 =          1
PE0 =          0

# Port E Data Direction Register - DDRE
DDE7 =         7
DDE6 =         6
DDE5 =         5
DDE4 =         4
DDE3 =         3
DDE2 =         2
DDE1 =         1
DDE0 =         0

# Port E Input Pins - PINE
PINE7 =        7
PINE6 =        6
PINE5 =        5
PINE4 =        4
PINE3 =        3
PINE2 =        2
PINE1 =        1
PINE0 =        0

# Port F Data Register - PORTF
PF7 =          7
PF6 =          6
PF5 =          5
PF4 =          4
PF3 =          3
PF2 =          2
PF1 =          1
PF0 =          0

# Port F Data Direction Register - DDRF
DDF7 =         7
DDF6 =         6
DDF5 =         5
DDF4 =         4
DDF3 =         3
DDF2 =         2
DDF1 =         1
DDF0 =         0

# Port F Input Pins - PINF
PINF7 =        7
PINF6 =        6
PINF5 =        5
PINF4 =        4
PINF3 =        3
PINF2 =        2
PINF1 =        1
PINF0 =        0

# Port G Data Register - PORTG
PG4 =          4
PG3 =          3
PG2 =          2
PG1 =          1
PG0 =          0

# Port G Data Direction Register - DDRG
DDG4 =         4
DDG3 =         3
DDG2 =         2
DDG1 =         1
DDG0 =         0

# Port G Input Pins - PING
PING4 =        4
PING3 =        3
PING2 =        2
PING1 =        1
PING0 =        0

# EEPROM Control Register
EERIE =        3
EEMWE =        2
EEWE =         1
EERE =         0

# Constants
SPM_PAGESIZE = 256
RAMSTART =     0x100
RAMEND =       0x10FF # Last On-Chip SRAM Location
XRAMEND =      0xFFFF
E2END =        0x0FFF
E2PAGESIZE =   8
FLASHEND =     0x1FFFF
