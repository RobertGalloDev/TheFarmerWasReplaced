
cur_locked = dict()
Key = 0
for L in Unlocks:
	C = get_cost(L)
	if C != None and len(C) > 0:
		cur_locked[Key] = (L,C)
		Key += 1

def canAfford(thisthing):
	affordable = True
	for key in thisthing:
		if num_items(key) < thisthing[key]:
			affordable = False
	return affordable

greenLight = []
redLight = []

for i in cur_locked:
	which, what = cur_locked[i]
	if canAfford(what):
		greenLight.append(which)
	else:
		redLight.append(which)

quick_print( "What we can afford:")
quick_print( greenLight )
quick_print( "---------------")
quick_print( "What we can NOT afford:")
quick_print( redLight )