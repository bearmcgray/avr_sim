#! /bin/bash
rm -f *.o *.elf *.lst
avr-as -mmcu=atmega128 cp_test.asm -o cp_test.o
avr-gcc -mmcu=atmega128 -o cp_test.elf cp_test.o
avr-objcopy -O binary cp_test.elf cp_test.bin
avr-objdump -d cp_test.elf > cp_test.lst