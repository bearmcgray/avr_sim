from utils import *
import vic
import tc0
		
class Core():
	def __init__(self):
		self.pm = self.loadProgramMemory()
		
		self.SREG = 0x5F
		self.RAMPZ = 0x5B

		self.IARXH = 27
		self.IARXL = 26
		self.IARYH = 29
		self.IARYL = 28
		self.IARZH = 31
		self.IARZL = 30

		self.srC = 0
		self.srZ = 1
		self.srN = 2
		self.srV = 3
		self.srS = 4
		self.srH = 5
		self.srT = 6
		self.srI = 7

		RAM_SIZE = (1 << 12) + 0x100
		self.RAM = [0 for _ in range(RAM_SIZE)]
		
		self.pc = 0
		self.sph = 0x5E
		self.spl = 0x5D
		self.skipCycleCounter = 0
		self.__vic = vic.vic(self.RAM)
		self.__tc0 = tc0.tc0(self.RAM,0x53,0x52,0x51,0x50,0x57,0x56,0x40)
		
		self.__vic.register(0x57,0,0x56,0,0x0020)

		
	def loadProgramMemory(self):
		words = []
		# with open('test_binary/cp_test.bin', 'rb') as pmfp:
		#~ with open('q27rf.bin', 'rb') as pmfp:
		with open('test_binary/tc0/tc0_test.bin', 'rb') as pmfp:
			pmData = pmfp.read()
		for i in range(0, len(pmData), 2):
			words.append(pmData[i] + (pmData[i + 1] << 8))
		print('Program memory loaded,', len(words), 'words')
		return words

	def debug(self, *args):
		hexedArgs = [hex(arg) if type(arg) == int else arg for arg in args ]
		print(hex(self.pc*2), f"{self.RAM[self.SREG]:#04x}", *hexedArgs)
		pass


	def tick(self):
		if self.skipCycleCounter > 0:
			self.skipCycleCounter -= 1
		else:	
			if self.RAM[self.SREG]&(1<<self.srI):
				intpc = self.__vic.check()
				#~ print("!!!",intpc)
				if intpc:
					#~ print(intpc)
					#push self.pc
					sp = (self.RAM[self.sph]<<8)|self.RAM[self.spl]
					
					#~ print (self.RAM[self.spl],self.RAM[self.sph])
					
					self.RAM[sp] = self.pc&0xff
					sp-=1
					self.RAM[sp] = (self.pc>>8)&0xff
					sp-=1
					
					self.RAM[self.sph] = (sp>>8)&0xff
					self.RAM[self.spl] = sp&0xff
					
					self.pc = intpc
					print ("vector",intpc)	
					pass
			
			opcode = self.pm[self.pc]
			hh_opcode = hh(opcode)
			if hh_opcode == 0x0:
				if opcode == 0x0: # NOP, p. 105
					self.debug('nop')
				elif opcode & 0xFC00 == 0x0400: # CPC, p. 61
					r = b(opcode, 9) << 4
					r += ll(opcode)
					d = b(opcode, 8) << 4
					d += lh(opcode)
					Rr = self.RAM[r]
					Rd = self.RAM[d]
					
					SR = self.RAM[self.SREG]
					R = Rd - Rr - b(SR, self.srC)

					SR = self.RAM[self.SREG]
					SR = updb(SR, self.srH, ~b(Rd, 3) & b(Rr, 3) | b(Rr, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3))
					SR = updb(SR, self.srV, b(Rd, 7) & ~b(Rr, 7) & ~b(R, 7) | ~b(Rd, 7) & b(Rr, 7) & b(R, 7))
					SR = updb(SR, self.srN, b(R, 7))
					SR = updb(SR, self.srZ, 1 if R == 0 else 0)
					SR = updb(SR, self.srC, ~b(Rd, 7) & b(Rr, 7) | b(Rr, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7))
					SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
					self.RAM[self.SREG] = SR

					self.debug('cpc', r, d)
				else:
					raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
			elif hh_opcode == 0x1:
				if opcode & 0xFC00 == 0x1400: # CP, p. 60
					r = b(opcode, 9) << 4
					r += ll(opcode)
					d = b(opcode, 8) << 4
					d += lh(opcode)
					Rr = self.RAM[r]
					Rd = self.RAM[d]
					R = Rd - Rr

					SR = self.RAM[self.SREG]
					SR = updb(SR, self.srH, ~b(Rd, 3) & b(Rr, 3) | b(Rr, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3))
					SR = updb(SR, self.srV, b(Rd, 7) & ~b(Rr, 7) & ~b(R, 7) | ~b(Rd, 7) & b(Rr, 7) & b(R, 7))
					SR = updb(SR, self.srN, b(R, 7))
					SR = updb(SR, self.srZ, 1 if R == 0 else 0)
					SR = updb(SR, self.srC, ~b(Rd, 7) & b(Rr, 7) | b(Rr, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7))
					SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
					self.RAM[self.SREG] = SR

					self.debug('cp', r, d)
				else:
					raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
			elif hh_opcode == 0x2:
				if opcode & 0xFC00 == 0x2000: # AND, p. 19
					r = b(opcode, 9) << 4
					r += ll(opcode)
					d = b(opcode, 8) << 4
					d += lh(opcode)
					R = self.RAM[r] & self.RAM[d]
					SR = self.RAM[self.SREG]
					SR = updb(SR, self.srV, 0)
					SR = updb(SR, self.srN, b(R, 7))
					SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
					SR = updb(SR, self.srZ, 1 if R == 0 else 0)
					self.RAM[self.SREG] = SR
					
					self.RAM[d] = R
					self.debug('and', r, d)
				elif opcode & 0xFC00 == 0x2400: # EOR, p. 71
					r = b(opcode, 9) << 4
					r += ll(opcode)
					d = b(opcode, 8) << 4
					d += lh(opcode)
					R = self.RAM[r] | self.RAM[d]
					SR = self.RAM[self.SREG]
					SR = updb(SR, self.srV, 0)
					SR = updb(SR, self.srN, b(R, 7))
					SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
					SR = updb(SR, self.srZ, 1 if R == 0 else 0)
					self.RAM[self.SREG] = SR
					
					self.RAM[d] = R
					self.debug('or', r, d)
				elif opcode & 0xFC00 == 0x2800: # OR, p. 106
					r = b(opcode, 9) << 4
					r += ll(opcode)
					d = b(opcode, 8) << 4
					d += lh(opcode)
					R = self.RAM[r] ^ self.RAM[d]
					SR = self.RAM[self.SREG]
					SR = updb(SR, self.srV, 0)
					SR = updb(SR, self.srN, b(R, 7))
					SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
					SR = updb(SR, self.srZ, 1 if R == 0 else 0)
					self.RAM[self.SREG] = SR
					
					self.RAM[d] = R
					self.debug('eor', r, d)
				else:
					raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
			elif hh_opcode == 0x3:
				if opcode & 0xF000 == 0x3000: # CPI, p. 63
					k = hl(opcode) << 4
					k += ll(opcode)
					d = lh(opcode)
					d += 16
					Rd = self.RAM[d]
					R = Rd - k
					SR = self.RAM[self.SREG]
					SR = updb(SR, self.srH, ~b(Rd, 3) & b(k, 3) | b(k, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3))
					SR = updb(SR, self.srV, b(Rd, 7) & ~b(k, 7) & ~b(R, 7) | ~b(Rd, 7) & b(k, 7) & b(R, 7))
					SR = updb(SR, self.srN, b(R, 7))
					SR = updb(SR, self.srZ, 1 if R == 0 else 0)
					SR = updb(SR, self.srC, ~b(Rd, 7) & b(k, 7) | b(k, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7))
					SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
					self.RAM[self.SREG] = SR

					self.debug('cpi', k, d, Rd)
				else:
					raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')

			elif hh_opcode == 0x4: # SBCI, p. 119
				k = hl(opcode) << 4
				k += ll(opcode)
				d = lh(opcode)
				d += 16
				Rd = self.RAM[d]
				SR = self.RAM[self.SREG]
				R = (Rd - k - b(SR, self.srC)) & 0xFF
				self.RAM[d] = R
				
				SR = updb(SR, self.srH, ~b(Rd, 3) & b(k, 3) | b(k, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3))
				SR = updb(SR, self.srV, b(Rd, 7) & ~b(k, 7) & ~b(R, 7) | ~b(Rd, 7) & b(k, 7) & b(R, 7))
				SR = updb(SR, self.srN, b(R, 7))
				SR = updb(SR, self.srZ, 1 if R == 0 else 0)
				SR = updb(SR, self.srC, ~b(Rd, 7) & b(k, 7) | b(k, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7))
				SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
				self.RAM[self.SREG] = SR

				self.debug('sbci', k, d, R)
			elif hh_opcode == 0x5: # SUBI, p. 150
				k = hl(opcode) << 4
				k += ll(opcode)
				d = lh(opcode)
				d += 16
				Rd = self.RAM[d]
				R = (Rd - k) & 0xFF
				self.RAM[d] = R

				SR = self.RAM[self.SREG]
				SR = updb(SR, self.srH, ~b(Rd, 3) & b(k, 3) | b(k, 3) & b(R, 3) | b(R, 3) & ~b(Rd, 3))
				SR = updb(SR, self.srV, b(Rd, 7) & ~b(k, 7) & ~b(R, 7) | ~b(Rd, 7) & b(k, 7) & b(R, 7))
				SR = updb(SR, self.srN, b(R, 7))
				SR = updb(SR, self.srZ, 1 if R == 0 else 0)
				SR = updb(SR, self.srC, ~b(Rd, 7) & b(k, 7) | b(k, 7) & b(R, 7) | b(R, 7) & ~b(Rd, 7))
				SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
				self.RAM[self.SREG] = SR

				self.debug('subi', k, d, R)
			elif hh_opcode == 0x6: # ORI, p. 107
				k = hl(opcode) << 4
				k += ll(opcode)
				d = lh(opcode)
				d += 16
				Rd = self.RAM[d]
				R = Rd | k
				self.RAM[d] = R
				SR = self.RAM[self.SREG]
				SR = updb(SR, self.srV, 0)
				SR = updb(SR, self.srN, b(R, 7))
				SR = updb(SR, self.srZ, 1 if R == 0 else 0)
				SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
				self.RAM[self.SREG] = SR

				self.debug('ori', k, d, Rd)
			elif hh_opcode == 0x7: # ANDI, p. 20
				k = hl(opcode) << 4
				k += ll(opcode)
				d = lh(opcode)
				d += 16
				Rd = self.RAM[d]
				R = Rd & k
				self.RAM[d] = R
				SR = self.RAM[self.SREG]
				SR = updb(SR, self.srV, 0)
				SR = updb(SR, self.srN, b(R, 7))
				SR = updb(SR, self.srZ, 1 if R == 0 else 0)
				SR = updb(SR, self.srS, b(SR, self.srN) ^ b(SR, self.srV))
				self.RAM[self.SREG] = SR
				self.debug('andi', k, d, Rd)

			elif hh_opcode == 0x9:
				if opcode & 0xFE0F == 0x900F: # POP, p. 109	
					d = (opcode >>4)&0x1f
					sp = (self.RAM[self.sph]<<8)|self.RAM[self.spl]
					sp+=1
					self.RAM[d] = self.RAM[sp]
					self.RAM[self.sph] = (sp>>8)&0xff
					self.RAM[self.spl] = sp&0xff
					self.debug('pop', d)
				elif opcode & 0xFE0F == 0x920F: # PUSH, p. 110	
					d = (opcode >>4)&0x1f
					sp = (self.RAM[self.sph]<<8)|self.RAM[self.spl]
					Rd = self.RAM[d]
					self.RAM[sp] = Rd
					sp-=1
					self.RAM[self.sph] = (sp>>8)&0xff
					self.RAM[self.spl] = sp&0xff
					self.debug('push', d)
				elif opcode & 0xFE00 == 0x9200: # ST, p. 141
					X = self.RAM[self.IARXH] << 8
					X += self.RAM[self.IARXL]
					r = b(opcode, 8) << 4
					r += lh(opcode)
					if ll(opcode) == 0xC:
						self.RAM[X] = self.RAM[r]
						self.debug('st', opcode, X, r)
					elif ll(opcode) == 0xD:
						self.RAM[X] = self.RAM[r]
						X += 1
						self.RAM[self.IARXH] = hbyte(X)
						self.RAM[self.IARXL] = lbyte(X)
						self.debug('st', opcode, X, r)
					elif ll(opcode) == 0xE:
						X -= 1
						self.RAM[self.IARXH] = hbyte(X)
						self.RAM[self.IARXL] = lbyte(X)
						self.RAM[X] = self.RAM[r]
						self.debug('st', opcode, X, r)
					elif ll(opcode) == 0x0:
						d = (opcode>>4)&0x001f	
						self.pc += 1
						k = self.pm[self.pc]
						self.RAM[k]=self.RAM[d]
						self.debug('sts', k, r)
					else :
						raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
						self.skipCycleCounter = 1

					#~ self.debug('st', opcode, X, r)
				elif opcode & 0xFE0E == 0x940C: # JMP, p. 82
					k = b(opcode, 8) << 21
					k += lh(opcode) << 17
					k += b(opcode, 0) << 16
					k += self.pm[self.pc + 1]
					self.debug('jmp', k * 2)
					if k == 0:
						raise
					self.pc = k - 1
					self.skipCycleCounter = 2
				elif opcode & 0xFE0E == 0x940E: # CALL, p. 47
					k = self.pm[self.pc + 1]
					sp = self.RAM[self.sph] << 8
					sp += self.RAM[self.spl]
					
					self.RAM[sp] = hbyte(self.pc + 2)
					self.RAM[sp - 1] = lbyte(self.pc + 2)
					sp += -2
					self.RAM[self.sph] = hbyte(sp)
					self.RAM[self.spl] = lbyte(sp)

					self.skipCycleCounter = 2
					self.pc = k - 1
					self.debug('call', k * 2)
				elif opcode & 0xFFFF == 0x9488: # CLC, p. 50
					SR = self.RAM[self.SREG]
					SR = updb(SR, self.srC, 0)
					self.RAM[self.SREG] = SR
					self.debug('clc')
				elif opcode & 0xFFFF == 0x9478: # SEI, p. 128
					SR = self.RAM[self.SREG]
					SR = updb(SR, self.srI, 1)
					self.RAM[self.SREG] = SR
					self.debug('sei')	
				elif opcode & 0xFFFF == 0x9518: # RETI, p. 113
					SR = self.RAM[self.SREG]
					SR = updb(SR, self.srI, 1)
					self.RAM[self.SREG] = SR
					
					sp = (self.RAM[self.sph]<<8)|self.RAM[self.spl]
					sp+=1
					pch = self.RAM[sp]
					sp+=1
					pcl = self.RAM[sp]
					
					self.RAM[self.sph] = (sp>>8)&0xff
					self.RAM[self.spl] = sp&0xff
					self.pc = ((pch<<8)|pcl)-1
					
					self.debug('reti')					
				elif opcode & 0xFFFF == 0x95D8: # ELPM i, p. 69
					Z = b(self.RAM[self.RAMPZ], 0) << 16
					Z += self.RAM[self.IARZH] << 8
					Z += self.RAM[self.IARZL]
					if Z % 2:
						self.RAM[0] = hbyte(self.pm[Z // 2])
					else:
						self.RAM[0] = lbyte(self.pm[Z // 2])
					self.skipCycleCounter = 2
					self.debug('elpm i', Z)
				elif opcode & 0xFE0F == 0x9006: # ELPM ii, p. 69
					Z = b(self.RAM[self.RAMPZ], 0) << 16
					Z += self.RAM[self.IARZH] << 8
					Z += self.RAM[self.IARZL]
					d = b(opcode, 8) << 4
					d += lh(opcode)
					if Z % 2:
						self.RAM[d] = hbyte(self.pm[Z // 2])
					else:
						self.RAM[d] = lbyte(self.pm[Z // 2])
					self.skipCycleCounter = 2
					self.debug('elpm ii', Z, d)
				elif opcode & 0xFE0F == 0x9007: # ELPM iii, p. 69
					Z = b(self.RAM[self.RAMPZ], 0) << 16
					Z += self.RAM[self.IARZH] << 8
					Z += self.RAM[self.IARZL]
					d = b(opcode, 8) << 4
					d += lh(opcode)
					if Z % 2:
						self.RAM[d] = hbyte(self.pm[Z // 2])
					else:
						self.RAM[d] = lbyte(self.pm[Z // 2])
					Z += 1
					self.RAM[self.RAMPZ] = b(Z, 16)
					self.RAM[self.IARZH] = (Z & 0xFFFF) >> 8
					self.RAM[self.IARZL] = Z & 0xFF
					self.skipCycleCounter = 2
					self.debug('elpm iii', Z, d)
				elif opcode & 0xFFFF == 0x9508: # RET, p. 112
					sp = self.RAM[self.sph] << 8
					sp += self.RAM[self.spl]
					sp += 2
					pc = self.RAM[sp] << 8
					pc += self.RAM[sp - 1]

					self.RAM[self.sph] = hbyte(sp)
					self.RAM[self.spl] = lbyte(sp)

					self.skipCycleCounter = 3
					self.pc = pc - 1
					self.debug('ret', sp, pc)
				elif opcode & 0xFF00 == 0x9A00: # SBI, p. 120
					a = lh(opcode) << 1
					a += b(opcode, 3)
					d = b(opcode, 2) << 2
					d += b(opcode, 1) << 1
					d += b(opcode, 0)
					self.RAM[0x20 + a] |= (1 << d)
					self.debug('sbi', a, d)
				elif opcode & 0xFF00 == 0x9800: # CBI, p. 48
					a = lh(opcode) << 1
					a += b(opcode, 3)
					d = b(opcode, 2) << 2
					d += b(opcode, 1) << 1
					d += b(opcode, 0)
					self.RAM[0x20 + a] &= ~(1 << d)
					self.debug('cbi', a, d)	
				elif opcode & 0xFE0F == 0x9000: # lds, p. 92
					d = (opcode>>4)&0x001f	
					self.pc += 1
					k = self.pm[self.pc]
					self.RAM[d]=self.RAM[k]
					self.debug('lds', d, k)					
				else:
					raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
			elif hh_opcode == 0xB:
				r = b(opcode, 8) << 4
				r += lh(opcode)
				d = b(opcode, 10) << 5
				d += b(opcode, 9) << 4
				d += ll(opcode)
				if opcode & 0xF800 == 0xB000: # IN, p. 80
					self.RAM[r] = self.RAM[d + 0x20]
					self.debug('in', r, d)
				elif opcode & 0xF800 == 0xB800: # OUT, p. 108
					self.RAM[d + 0x20] = self.RAM[r]
					self.debug('out', r, d)
				else:
					raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
			elif hh_opcode == 0xC:
				if opcode & 0xF000 == 0xC000: # RJMP, p. 114
					r = hl(opcode) << 8
					r += lbyte(opcode)
					#~ print(r)
					if (r >> 11) > 0:
						r -= 1
						r = ~r
						r &= 0xFFF
						r = -r
					self.pc += r
					self.skipCycleCounter = 1
					self.debug('rjmp', r * 2)
				else:
					raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
			elif hh_opcode == 0xE:
				if opcode & 0xF000 == 0xE000: # LDI, p. 91
					r = hl(opcode) << 4
					r += ll(opcode)
					d = lh(opcode)
					d += 16
					self.RAM[d] = r
					self.debug('ldi', r, d)
				else:
					raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
			elif hh_opcode == 0xF:
				if opcode & 0xFC07 == 0xF401: # BRNE, p. 38
					k = b(opcode, 9) << 6
					k += b(opcode, 8) << 5
					k += lh(opcode) << 1
					k += b(opcode, 3)
					if (k >> 6) > 0:
						k -= 1
						k = ~k
						k &= 0x7F
						k = -k
					if b(self.RAM[self.SREG], self.srZ) == 0:
						self.pc += k
						self.skipCycleCounter = 1
					self.debug('brne', k*2)
				elif opcode & 0xFE08 == 0xFE00: # SBRS, p. 126
					r = b(opcode, 8) << 4
					r += lh(opcode)
					d = b(opcode, 2) << 2
					d += b(opcode, 1) << 1
					d += b(opcode, 0)
					if b(self.RAM[r], d) == 1:
						nopcode = self.pm[self.pc + 1]
						# check if the next opcode is two word 
						if nopcode & 0xFE0E == 0x940E or nopcode & 0xFE0E == 0x940C:
							self.pc += 2
						else:
							self.pc += 1
					self.debug('sbrs', r, d)
				else:
					raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
			else:
				raise RuntimeError(f'Unknown opcode {hex(opcode)}@{hex(self.pc*2)}')
				
			self.__tc0.tick()
					
			self.pc += 1
