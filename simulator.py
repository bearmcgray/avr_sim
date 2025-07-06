from core import Core

core = Core()
for cycle in range(10000000):
	if cycle % 1000000 == 0:
		print('cycle', cycle)
	core.tick()
print('end')
