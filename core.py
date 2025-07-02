from utils import *
		
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




class Core():
	def __init__(self):
		self.pm = self.loadProgramMemory()
		self.SR = SREG()
		self.Rs = [0 for _ in range(32)]
		self.IOs = [0 for _ in range(64)]
		RAM_SIZE = (1 << 12) + 0x100
		self.RAM = [0 for _ in range(RAM_SIZE)]
		self.pc = 0
		self.sph = 62
		self.spl = 61
		self.skipCycleCounter = 0
		
	def loadProgramMemory(self):
		words = []
		with open('test_binary/cp_test.bin', 'rb') as pmfp:
		# with open('q27rf.bin', 'rb') as pmfp:
			pmData = pmfp.read()
		for i in range(0, len(pmData), 2):
			words.append(pmData[i] + (pmData[i + 1] << 8))
		print('Program memory loaded,', len(words), 'words')
		return words

	def debug(self, *args):
		print(hex(self.pc*2), *args)
		pass


	def cyclon(self):
		if self.skipCycleCounter > 0:
			self.skipCycleCounter -= 1
		else:	
			opcode = self.pm[self.pc]

			if opcode & 0xFE0E == 0x940C: # JMP, p. 82
				k = b(opcode, 8) << 21
				k += lh(opcode) << 17
				k += b(opcode, 0) << 16
				k += self.pm[self.pc + 1]
				self.debug('jmp', k)
				self.pc = k - 1
				self.skipCycleCounter = 2
			elif opcode & 0xFC00 == 0x2400: # EOR, p. 71
				r = b(opcode, 9) << 4
				r += ll(opcode)
				d = b(opcode, 8) << 4
				d += lh(opcode)
				R = self.Rs[r] ^ self.Rs[d]
				self.SR.V = 0
				self.SR.N = b(R, 7)
				self.SR.S = self.SR.N ^ self.SR.V 
				self.SR.Z = 1 if R == 0 else 0
				self.Rs[d] = R
				self.debug('eor', r, d)
			elif opcode & 0xF800 == 0xB800: # OUT, p. 108
				r = b(opcode, 8) << 4
				r += lh(opcode)
				d = b(opcode, 10) << 5
				d += b(opcode, 9) << 4
				d += ll(opcode)
				self.IOs[d] = self.Rs[r]
				self.debug('out', r, d)
			elif opcode & 0xF000 == 0xE000: # LDI, p. 91
				r = hl(opcode) << 4
				r += ll(opcode)
				d = lh(opcode)
				d += 16
				self.Rs[d] = r
				self.debug('ldi', r, d)
			elif opcode & 0xF000 == 0xC000: # RJMP, p. 114
				r = hl(opcode) << 8
				r += lbyte(opcode)
				if (r >> 11) > 0:
					r -= 1
					r = ~r
					r &= 0xFFFFFF
					r = -r
				self.pc += r
				self.skipCycleCounter = 1
				self.debug('rjmp', r)
			elif opcode & 0xF000 == 0x3000: # CPI, p. 63
				k = hl(opcode) << 4
				k += ll(opcode)
				d = lh(opcode)
				d += 16
				Rd = self.Rs[d]
				R = Rd - k
				self.SR.H = (~b(Rd, 3) & b(k, 3) | b(k, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3)) & 1
				self.SR.V = (b(Rd, 7) & ~b(k, 7) & ~b(R, 7) | ~b(Rd, 7) & b(k, 7) & b(R, 7)) & 1
				self.SR.N = b(R, 7)
				self.SR.Z = 1 if R == 0 else 0
				self.SR.C = (~b(Rd, 7) & b(k, 7) | b(k, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7)) & 1
				self.SR.S = self.SR.N ^ self.SR.V
				self.debug('cpi', k, d)
			elif opcode & 0xFC00 == 0x0400: # CPC, p. 61
				r = b(opcode, 9) << 4
				r += ll(opcode)
				d = b(opcode, 8) << 4
				d += lh(opcode)
				Rr = self.Rs[r]
				Rd = self.Rs[d]
				R = Rd - Rr - self.SR.C
				self.SR.H = (~b(Rd, 3) & b(Rr, 3) | b(Rr, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3)) & 1
				self.SR.V = (b(Rd, 7) & ~b(Rr, 7) & ~b(R, 7) | ~b(Rd, 7) & b(Rr, 7) & b(R, 7)) & 1
				self.SR.N = b(R, 7)
				self.SR.Z = 1 if R == 0 else 0
				self.SR.C = (~b(Rd, 7) & b(Rr, 7) | b(Rr, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7)) & 1
				self.SR.S = self.SR.N ^ self.SR.V
				self.debug('cpc', r, d)
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
				if self.SR.Z == 0:
					self.pc += k
					self.skipCycleCounter = 1
				self.debug('brne', k)
			elif opcode & 0xFE0E == 0x940E: # CALL, p. 47
				k = self.pm[self.pc + 1]
				sp = self.IOs[self.sph] << 8
				sp += self.IOs[self.spl]
				
				self.RAM[sp] = hbyte(self.pc + 2)
				self.RAM[sp - 1] = lbyte(self.pc + 2)
				sp += -2
				self.IOs[self.sph] = hbyte(sp)
				self.IOs[self.spl] = lbyte(sp)

				self.skipCycleCounter = 2
				self.pc = k - 1
				self.debug('call', hex(k*2))
			elif opcode & 0xFF00 == 0x9A00: # SBI, p. 120
				a = lh(opcode) << 1
				a += b(opcode, 3)
				d = b(opcode, 2) << 2
				d += b(opcode, 1) << 1
				d += b(opcode, 0)
				self.Rs[a] |= (1 << d)
				self.debug('sbi', a, d)
			elif opcode & 0xFFFF == 0x9488: # CLC, p. 50
				self.SR.C = 0
				self.debug('clc')
			elif opcode & 0xFC00 == 0x1400: # CP, p. 60
				r = b(opcode, 9) << 4
				r += ll(opcode)
				d = b(opcode, 8) << 4
				d += lh(opcode)
				Rr = self.Rs[r]
				Rd = self.Rs[d]
				R = Rd - Rr
				self.SR.H = (~b(Rd, 3) & b(Rr, 3) | b(Rr, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3)) & 1
				self.SR.V = (b(Rd, 7) & ~b(Rr, 7) & ~b(R, 7) | ~b(Rd, 7) & b(Rr, 7) & b(R, 7)) & 1
				self.SR.N = b(R, 7)
				self.SR.Z = 1 if R == 0 else 0
				self.SR.C = (~b(Rd, 7) & b(Rr, 7) | b(Rr, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7)) & 1
				self.SR.S = self.SR.N ^ self.SR.V
				self.debug('cp', r, d)
			elif opcode & 0xF800 == 0xB000: # IN, p. 80
				d = b(opcode, 8) << 4
				d += lh(opcode)
				a = b(opcode, 10) << 5
				a += b(opcode, 9) << 4
				a += ll(opcode)
				self.Rs[d] = self.IOs[a]
				self.debug('in', a, d)
			elif opcode & 0xFE08 == 0xFE00: # SBRS, p. 126
				r = b(opcode, 8) << 4
				r += lh(opcode)
				d = b(opcode, 2) << 2
				d += b(opcode, 1) << 1
				d += b(opcode, 0)
				if b(self.Rs[r], d) == 1:
					nopcode = self.pm[self.pc + 1]
					# check if the next opcode is two word 
					if nopcode & 0xFE0E == 0x940E or nopcode & 0xFE0E == 0x940C:
						self.pc += 2
					else:
						self.pc += 1
				self.debug('sbrs', r, d)
			else:
				print('Unknown opcode', hex(opcode))
				raise
			self.pc += 1
