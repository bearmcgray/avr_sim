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
	with open('test_binary/cp_test.bin', 'rb') as pmfp:
	# with open('q27rf.bin', 'rb') as pmfp:
		pmData = pmfp.read()
	for i in range(0, len(pmData), 2):
		words.append(pmData[i] + (pmData[i + 1] << 8))
		# words.append(Word(pmData[i] + (pmData[i + 1] << 8)))
	return words

def debug(*args):
	# print(hex(pc*2), *args)
	pass


pm = loadProgramMemory()
SR = SREG()
Rs = [0 for _ in range(32)]
IOs = [0 for _ in range(64)]
RAM_SIZE = (1 << 12) + 0x100
RAM = [0 for _ in range(RAM_SIZE)]
pc = 0
sph = 62
spl = 61
skipCycleCounter = 0

print('RAM', hex(RAM_SIZE))

for cycle in range(100000000):
	if cycle % 10000000 == 0:
		print(cycle)

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
			pc = k - 1
			skipCycleCounter = 2
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
			SR.Z = 1 if R == 0 else 0
			SR.C = (~b(Rd, 7) & b(k, 7) | b(k, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7)) & 1
			SR.S = SR.N ^ SR.V
			debug('cpi', k, d)
		elif opcode & 0xFC00 == 0x0400: # CPC, p. 61
			r = b(opcode, 9) << 4
			r += ll(opcode)
			d = b(opcode, 8) << 4
			d += lh(opcode)
			Rr = Rs[r]
			Rd = Rs[d]
			R = Rd - Rr - SR.C
			SR.H = (~b(Rd, 3) & b(Rr, 3) | b(Rr, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3)) & 1
			SR.V = (b(Rd, 7) & ~b(Rr, 7) & ~b(R, 7) | ~b(Rd, 7) & b(Rr, 7) & b(R, 7)) & 1
			SR.N = b(R, 7)
			SR.Z = 1 if R == 0 else 0
			SR.C = (~b(Rd, 7) & b(Rr, 7) | b(Rr, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7)) & 1
			SR.S = SR.N ^ SR.V
			debug('cpc', r, d)
		elif opcode & 0xFC07 == 0xF401: # BRNE, p. 38
			k = b(opcode, 9) << 6
			k += b(opcode, 8) << 5
			k += lh(opcode) << 1
			k += b(opcode, 3)
			if (k >> 6) > 0:
				k -= 1
				k = ~k
				k &= 0x7F
				k = -k
			if SR.Z == 0:
				pc += k
				skipCycleCounter = 1
			debug('brne', k)
		elif opcode & 0xFE0E == 0x940E: # CALL, p. 47
			k = pm[pc + 1]
			sp = IOs[sph] << 8
			sp += IOs[spl]
			
			RAM[sp] = hbyte(pc + 2)
			RAM[sp - 1] = lbyte(pc + 2)
			sp += -2
			IOs[sph] = hbyte(sp)
			IOs[spl] = lbyte(sp)

			skipCycleCounter = 2
			pc = k - 1
			debug('call', hex(k*2))
		elif opcode & 0xFF00 == 0x9A00: # SBI, p. 120
			a = lh(opcode) << 1
			a += b(opcode, 3)
			d = b(opcode, 2) << 2
			d += b(opcode, 1) << 1
			d += b(opcode, 0)
			Rs[a] |= (1 << d)
			debug('sbi', a, d)
		elif opcode & 0xFFFF == 0x9488: # CLC, p. 50
			SR.C = 0
			debug('clc')
		elif opcode & 0xFC00 == 0x1400: # CP, p. 60
			r = b(opcode, 9) << 4
			r += ll(opcode)
			d = b(opcode, 8) << 4
			d += lh(opcode)
			Rr = Rs[r]
			Rd = Rs[d]
			R = Rd - Rr
			SR.H = (~b(Rd, 3) & b(Rr, 3) | b(Rr, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3)) & 1
			SR.V = (b(Rd, 7) & ~b(Rr, 7) & ~b(R, 7) | ~b(Rd, 7) & b(Rr, 7) & b(R, 7)) & 1
			SR.N = b(R, 7)
			SR.Z = 1 if R == 0 else 0
			SR.C = (~b(Rd, 7) & b(Rr, 7) | b(Rr, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7)) & 1
			SR.S = SR.N ^ SR.V
			debug('cp', r, d)
		elif opcode & 0xF800 == 0xB000: # IN, p. 80
			d = b(opcode, 8) << 4
			d += lh(opcode)
			a = b(opcode, 10) << 5
			a += b(opcode, 9) << 4
			a += ll(opcode)
			Rs[d] = IOs[a]
			debug('in', a, d)
		elif opcode & 0xFE08 == 0xFE00: # SBRS, p. 126
			r = b(opcode, 8) << 4
			r += lh(opcode)
			d = b(opcode, 2) << 2
			d += b(opcode, 1) << 1
			d += b(opcode, 0)
			if b(Rs[r], d) == 1:
				nopcode = pm[pc + 1]
				# check if the next opcode is two word 
				if nopcode & 0xFE0E == 0x940E or nopcode & 0xFE0E == 0x940C:
					pc += 2
				else:
					pc += 1
			debug('sbrs', r, d)
		else:
			print('Unknown opcode', hex(opcode))
			break
		pc += 1
