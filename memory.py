class Memory():
	"""Memory"""
	def __init__(self):
		self.RAM_SIZE = (1 << 12) + 0x100
		self.RAM = [0] * self.RAM_SIZE
		self.pm = []
	
	def loadProgramMemory(self, filePath):
		words = []
		
		with open(filePath, 'rb') as pmfp:
			pmData = pmfp.read()
		for i in range(0, len(pmData), 2):
			words.append(pmData[i] + (pmData[i + 1] << 8))
		print(f'Program memory loaded: {filePath}, {len(words)} words')
		self.pm = words
		