result = []
padding = 14
with open('iom128.h', 'r') as fp:
			for i, line in enumerate(fp):
				if i <= 50 or 358 < i <= 539 or i >= 1190:
					continue
				elif i == 235:
					result.append('# Stack Pointer Register\n')
					result.append('SP ='.ljust(padding, ' ') + ' 0x5D\n')
					result.append('SPL ='.ljust(padding, ' ') + ' 0x5D\n')
					result.append('SPH ='.ljust(padding, ' ') + ' 0x5E\n')
				elif i == 237:
					result.append('# Status Register\n')
					result.append('SREG ='.ljust(padding, ' ') + ' 0x5F\n')
				elif i == 344:
					result.append('# ' + line[3:-3] + '\n')
				elif i == 543:
					result.append('\n')
					result.append('# Status Register - SREG\n')
					result.append('SREGI ='.ljust(padding, ' ') + ' 7\n')
					result.append('SREGT ='.ljust(padding, ' ') + ' 6\n')
					result.append('SREGH ='.ljust(padding, ' ') + ' 5\n')
					result.append('SREGS ='.ljust(padding, ' ') + ' 4\n')
					result.append('SREGV ='.ljust(padding, ' ') + ' 3\n')
					result.append('SREGN ='.ljust(padding, ' ') + ' 2\n')
					result.append('SREGZ ='.ljust(padding, ' ') + ' 1\n')
					result.append('SREGC ='.ljust(padding, ' ') + ' 0\n')
					result.append('\n')
				elif i in [540, 542, 829, 833]:
					result.append('\n')
				elif i in [541, 830, 831, 832]:
					result.append('#' + line)
				elif len(line.split()) >= 3 and line.split()[0].strip() == '#define':
					# print(line)
					res = []
					for j, word in enumerate(line.split()):
						if word == '#define' or word == '*/':
							continue
						elif j == 1:
							res.append((word.strip() + ' =').ljust(padding, ' '))
						elif j == 2:
							if word.startswith('_SFR_IO8'):
								res.append(f'{int(word[9:-1], 16) + 0x20:#X}')
							elif word.startswith('_SFR_IO16'):
								res.append(f'{int(word[10:-1], 16) + 0x20:#X}')
							elif word.startswith('_SFR_MEM8'):
								res.append(word[10:-1])
							elif word.startswith('_SFR_MEM16'):
								res.append(word[11:-1])
							else:
								res.append(word)
						elif word == '/*':
							res.append('#')
						else:
							res.append(word)
					result.append(' '.join(res) + '\n')
				elif len(line.split()) >= 3 and line.split()[0].strip() == '/*' and  line.split()[-1].strip() == '*/':
					result.append('# ' + ' '.join(line.split()[1:-1]) + '\n')
				else:
					# print(line.split())
					result.append(line)
# for line in result:
# 	print(line)

with open('iom128.py', 'w') as out:
	out.writelines(result)