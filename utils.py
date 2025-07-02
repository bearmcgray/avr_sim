def b(v, pos):
	return (v & (1 << pos)) >> pos

def lbyte(v):
	return v & 0xFF

def hbyte(v):
	return v >> 8

def ll(v):
	return (v & 0x000F)

def lh(v):
	return (v & 0x00F0) >> 4

def hl(v):
	return (v & 0x0F00) >> 8

def hh(v):
	return (v & 0xF000) >> 12