CC=avr-gcc
DUDE=avrdude
OBJCOPY=avr-objcopy
OBJDUMP=avr-objdump
RM=rm
SIZE=avr-size

TARGET=tc0_test
OBJS = main.o 
#~ OBJS = main.o ppm.o uart.o

#~ MCU=attiny2313
MCU=atmega128
#avrdude -B 2000 -c dragon_isp -p attiny2313 -P usb -U lfuse:r:-:i -v
#avrdude -B 2000 -c dragon_isp -p attiny2313 -P usb -U lfuse:w:0xDD:m -U hfuse:w:0xDF:m -U efuse:w:0xFF:m -U lock:w:0xFF:m

#~ MCU=atmega328p
#~ MCU=atmega8

F_CPU=8000000

CFLAGS=-std=c99 -Os -DMCU=$(MCU) -DF_CPU=$(F_CPU)UL -mmcu=$(MCU)
#~ -Os optimization by size reduces almost 20% of used size

LFLAGS=-mmcu=$(MCU)

SFLAGS=-C --mcu=$(MCU)

CPFLAGS=-O ihex -R .eeprom 

DFLAGS=-c usbasp -p $(MCU) -P usb

all: $(TARGET).hex $(TARGET).bin $(TARGET).lst
	$(SIZE) $(SFLAGS) $(TARGET).elf

$(TARGET).elf: $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET).elf $^

$(TARGET).hex: $(TARGET).elf
	$(OBJCOPY) -O ihex -R .eeprom $^ $@

$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary -R .eeprom $^ $@

$(TARGET).lst: $(TARGET).elf
	$(OBJDUMP) -d $^ > $@

clean:
	rm -f $(OBJS)
	rm -f *.o
	rm -f *.lst
	rm -f $(TARGET).elf $(TARGET).hex $(TARGET).bin

programm:
	$(DUDE) $(DFLAGS) -U  flash:w:$(TARGET).hex

