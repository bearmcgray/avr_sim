from core import Core
import tc0
from memory import Memory
from iom128 import *

class Simulator():
	"""Simulator"""
	def __init__(self):
		self.__mem = Memory()
		# self.__mem.loadProgramMemory('test_binary/cp_test.bin')
		self.__mem.loadProgramMemory('q27rf.bin')
		# self.__mem.loadProgramMemory('test_binary/tc0/tc0_test.bin')
		self.__core = Core(self.__mem.pm, self.__mem.RAM)
		self.__tc0 = tc0.tc0(self.__mem.RAM,TCCR0,TCNT0,OCR0,ASSR,TIMSK,TIFR,SFIOR)

	def run(self):
		for cycle in range(1000000):
			if cycle % 1000000 == 0:
				print('cycle', cycle)
			self.__core.tick()
			self.__tc0.tick()
		print('end')

def main():
	Simulator().run()

if __name__=="__main__":
	main()