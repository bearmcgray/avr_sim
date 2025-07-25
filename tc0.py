import sys
from time import sleep

class tc0:
	PSR0=1
	
	CS00=0
	CS01=1
	CS02=2
	
	TOV0=0
	OCF0=1
	
	WGM00=6
	WGM01=3
	
	MAX = 0xff
	def __init__(self,mem,tccr0,tcnt0,ocr0,assr,timsk,tifr,sfior):
		
		self.__mem = mem
		
		self.__tick = 0 
		#registers
		self.__mask={
			tccr0:0xff,
			tcnt0:0xff,
			ocr0:0xff,
			assr:0x0f,
			timsk:0x03,
			tifr:0x03,
			sfior:0x82,
		}
		
		self.__TCCR0 = tccr0
		self.__TCNT0 = tcnt0
		self.__OCR0 = ocr0
		self.__ASSR = assr
		self.__TIMSK = timsk
		self.__TIFR = tifr
		self.__SFIOR = sfior
		
		#state
		self.__prescaler = 0
		self.__prevpresc = 0
	
	def reset(self):
		self.__tick = 0
		self.__prescaler = 0
		self.__prevpresc = 0

	def tick(self):
		self.__process()
		#~ print("tick:",str(self.__tick).rjust(5," "),self.__mem)
		
		#~ mem = []
		#~ for i in self.__mask.keys():
			#~ mem.append((hex(i),self.__mem[i]))
		
		#~ print("tick:",str(self.__tick).rjust(5," "),mem)
		
	
	def __process(self):
		self.__tick+=1
		self.__prescaler+=1
		if self.__mem[self.__SFIOR]&(1<<tc0.PSR0):
			self.__mem[self.__SFIOR]&=~(1<<tc0.PSR0)
			self.__prescaler = 0
		
		clk_sel = self.__mem[self.__TCCR0]&0x07
		wgm = ((self.__mem[self.__TCCR0]&(1<<self.WGM01))>>(self.WGM01-1))|((self.__mem[self.__TCCR0]&(1<<self.WGM00))>>self.WGM00)
		#~ print(clk_sel,wgm)
		if clk_sel == 0:
			clk = 0
		elif clk_sel == 1:
			#~ clk = 1-self.__prevpresc
			clk = (self.__prescaler&(1<<0))>>0
		elif clk_sel == 2:	
			clk = (self.__prescaler&(1<<3))>>3
		elif clk_sel == 3:	
			clk = (self.__prescaler&(1<<5))>>5
		elif clk_sel == 4:	
			clk = (self.__prescaler&(1<<6))>>6
		elif clk_sel == 5:	
			clk = (self.__prescaler&(1<<7))>>7
		elif clk_sel == 6:
			clk = (self.__prescaler&(1<<8))>>8			
		elif clk_sel == 7:	
			clk = (self.__prescaler&(1<<10))>>10
			
		if clk!=self.__prevpresc:
			if wgm==0:
				if self.__mem[self.__TCNT0]==self.MAX:
					self.__mem[self.__TIFR] |= 1<<tc0.TOV0
			elif wgm == 1:
				raise RuntimeError("mode not implemented")
			elif wgm == 2:
				if self.__mem[self.__TCNT0]==self.__mem[self.__OCR0]:
					self.__mem[self.__TIFR] |= 1<<tc0.OCF0
				if self.__mem[self.__TCNT0]==self.MAX:
					self.__mem[self.__TIFR] |= 1<<tc0.TOV0
			elif wgm == 3:
				raise RuntimeError("mode not implemented")
			else:
				raise RuntimeError("mode not implemented")
				
			self.__mem[self.__TCNT0] = (self.__mem[self.__TCNT0]+1)&self.__mask[self.__TCNT0]
		self.__prevpresc = clk
		
def main():
	mem=[0x09,0,0x64,0,0,0,0]
	tc = tc0(mem,0,1,2,3,4,5,6)
	
	while 1:
		tc.tick()
		if mem[5]&1:
			break
		sleep(0.033)

if __name__=="__main__":
	main()