import sys

class vic:
	def __init__(self,mem):
		self.__mem = mem
		self.__table = { }
	
	def register(self,maddr,mbit,iaddr,ibit, vector):
		if self.__table.get(iaddr,None)==None:
			self.__table[iaddr]={}

		self.__table[iaddr][ibit]=[vector,maddr,mbit]
		
	def check(self):
		for k,bs in self.__table.items():
			#~ print(k,v) 
			for b,v in bs.items():
				if self.__mem[v[1]]&(1<<v[2]):
					if self.__mem[k]&(1<<b):
						#~ print("---")
						self.__mem[k] &= ~(1<<b)
						return v[0]
		
def main():
	ic = vic()
	ic.register(3,4,5,6,7)
	ic.check()

if __name__=="__main__":
	main()