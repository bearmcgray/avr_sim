.org 0

.org 0x20
	reti

.global main


main:
	sbi 0x11,4
	clc
	ldi r16,0xff
	ldi r17,0xff
	cp r16,r17
	ldi r18,1;
	out 0x3f,r18
	in r16,0x3f
	sbrs r16,0
	sbi 0x12,4
	
	ldi r16, 9
	sts 0x53,r16

	ldi r16, 1
	sts 0x57,r16
	
	sei
	loop:
		jmp loop
