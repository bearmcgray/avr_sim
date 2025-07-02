from core import Core

core = Core()
for cycle in range(100):
	if cycle % 1000000 == 0:
		print('cycle', 0)
	core.cyclon()

