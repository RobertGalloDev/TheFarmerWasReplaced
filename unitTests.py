import KrunkUtils

tests = [
	[(0,0),(5,5)],
	[(8,8),(7,7)],
	[(19,0),(0,3)]
]

for testcase in tests:
	if len(testcase) == 2:
		quick_print(testcase)
		startx,starty = testcase[0]
		endx,endy = testcase[1]
		KrunkUtils.navigateTo(startx,starty)
		KrunkUtils.pacmanTo(endx,endy)
		do_a_flip()
	