#! /bin/bash
avr-as -mmcu=atmega128 cp_test.asm -o cp_test.elf
avr-objcopy -O binary cp_test.elf cp_test.bin
