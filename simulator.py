# class Word():
# 	"""2 Byte Word"""
# 	def __init__(self, value):
# 		self.lbyte = value & 0xFF
# 		self.hbyte = value >> 8
# 		self.v = value
# 		self.ll = self.lbyte & 0xF
# 		self.lh = self.lbyte >> 4
# 		self.hl = self.hbyte & 0xF
# 		self.hh = self.hbyte >> 4

# 	def __str__(self):
# 		return f"{self.v:04x}"

# 	def __and__(self, other):
# 		return  Word(self.v & other.v)

# 	def __or__(self, other):
# 	    return  Word(self.v | other.v)

# 	def __xor__(self, other):
# 	    return  Word(self.v ^ other.v)

# 	def __lshift__(self, shift):
# 	    return  Word(self.v << shift)

# 	def __rshift__(self, shift):
# 	    return Word(self.v >> shift)

# 	def __invert__(self):
# 	    return Word(~self.v)

# 	def __add__(self, other):
# 		return Word(self.v + other.v)

# 	def __radd__(self, other):
# 		return self.__add__(other)

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
		
class SREG():
	"""Status Register"""
	def __init__(self):
		self.C = 0
		self.Z = 0
		self.N = 0
		self.V = 0
		self.S = 0
		self.H = 0
		self.T = 0
		self.I = 0


def loadProgramMemory():
	words = []
	with open('q27rf.bin', 'rb') as pmfp:
		pmData = pmfp.read()
	for i in range(0, len(pmData), 2):
		words.append(pmData[i] + (pmData[i + 1] << 8))
		# words.append(Word(pmData[i] + (pmData[i + 1] << 8)))
	return words

def debug(*args):
	print(*args)



print('SIM')

pm = loadProgramMemory()
SR = SREG()
Rs = [0 for _ in range(32)]
IOs = [0 for _ in range(64)]
pc = 0
skipCycleCounter = 0

for cycle in range(10000):
	if skipCycleCounter > 0:
		skipCycleCounter -= 1
	else:	
		opcode = pm[pc]
		if opcode & 0xFE0E == 0x940C: # JMP, p. 82
			k = b(opcode, 8) << 21
			k += lh(opcode) << 17
			k += b(opcode, 0) << 16
			k += pm[pc + 1]
			debug('jmp', k)
			pc = k
			skipCycleCounter = 2
			continue
		elif opcode & 0xFC00 == 0x2400: # EOR, p. 71
			r = b(opcode, 9) << 4
			r += ll(opcode)
			d = b(opcode, 8) << 4
			d += lh(opcode)
			R = Rs[r] ^ Rs[d]
			SR.V = 0
			SR.N = b(R, 7)
			SR.S = SR.N ^ SR.V 
			SR.Z = 0 if R > 0 else 1
			Rs[d] = R
			debug('eor', r, d)
		elif opcode & 0xF800 == 0xB800: # OUT, p. 108
			r = b(opcode, 8) << 4
			r += lh(opcode)
			d = b(opcode, 10) << 5
			d += b(opcode, 9) << 4
			d += ll(opcode)
			IOs[d] = Rs[r]
			debug('out', r, d)
		elif opcode & 0xF000 == 0xE000: # LDI, p. 91
			r = hl(opcode) << 4
			r += ll(opcode)
			d = lh(opcode)
			d += 16
			Rs[d] = r
			debug('ldi', r, d)
		elif opcode & 0xF000 == 0xC000: # RJMP, p. 114
			r = hl(opcode) << 8
			r += lbyte(opcode)
			if (r >> 11) > 0:
				r -= 1
				r = ~r
				r &= 0xFFFFFF
				r = -r
			pc += r
			skipCycleCounter = 1
			debug('rjmp', r)
		elif opcode & 0xF000 == 0x3000: # CPI, p. 63
			k = hl(opcode) << 4
			k += ll(opcode)
			d = lh(opcode)
			d += 16
			Rd = Rs[d]
			R = Rd - k
			SR.H = (~b(Rd, 3) & b(k, 3) | b(k, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3)) & 1
			SR.V = (b(Rd, 7) & ~b(k, 7) & ~b(R, 7) | ~b(Rd, 7) & b(k, 7) & b(R, 7)) & 1
			SR.N = b(R, 7)
			SR.Z = 0 if R > 0 else 1
			SR.C = (~b(Rd, 7) & b(k, 7) | b(k, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7)) & 1
			SR.S = SR.N ^ SR.V
			debug('cpi', k, d)
		else:
			print('Unknown opcode', hex(opcode))
			break
		pc += 1
