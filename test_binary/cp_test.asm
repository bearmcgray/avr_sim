.org 0
.global main
main:
sbi 0x11,4
clc
ldi r16,0xff
ldi r17,0xff
cp r16,r17;
in r16,0x3f
sbrs r16,0
sbi 0x12,4
loop:
jmp .-4
