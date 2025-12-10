
def pacmanTo(i,j):
	currX = get_pos_x()
	currY = get_pos_y()
	
	xeast = 0
	xwest = 0
	ynorth = 0
	ysouth = 0
	
	if i < currX:
		xwest = currX - i
		xeast = i + (get_world_size() - currX)
	elif i > currX:
		xeast = i - currX
		xwest = currX + (get_world_size() - i)
	
	if j < currY:
		ysouth = currY - j
		ynorth = j + (get_world_size() - currY)
	elif j > currY:
		ynorth = j - currY
		ysouth = currY + (get_world_size() - j)
	
	dirNS = North
	dirEW = East
	if xwest<xeast:
		dirEW = West

	if ysouth<ynorth:
		dirNS = South
	
	moved = True
	while moved and i != currX:
		moved = move(dirEW)
		currX = get_pos_x()
	while moved and j != currY:
		moved = move(dirNS)
		currY = get_pos_y()
	
	if get_pos_x() == i and get_pos_y() == j:
		return True
	else:
		return False
		
def navigateTo(i,j):
	while get_pos_x() > i:
		move(West)
	while get_pos_x() < i:
		move(East)
	while get_pos_y() > j:
		move(South)
	while get_pos_y() < j:
		move(North)

def resetPos():
	pacmanTo(0,0)

def tillSlice():
	for y in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		move(North)

def clearSlice():
	for y in range(get_world_size()):
		harvest()
		move(North)

def clearMap(tillFarm = False):
	navigateTo(0,0)
	funcToUse = clearSlice
	if tillFarm:
		funcToUse = tillSlice
	
	for x in range(get_world_size()):
		if not spawn_drone(funcToUse):
			funcToUse()
		move(East)

def tryNavigate(tx,ty):
	startx = get_pos_x()
	starty = get_pos_y()
	failed = False
	x = startx
	y = starty
	
	while (x != tx or y != ty) and not failed:
		moved = False
		if tx > x:
			moved = move(East)
		elif tx < x:
			moved = move(West)
		if not moved:
			if ty > y:
				moved = move(North)
			elif ty < y:
				moved = move(South)
		x = get_pos_x()
		y = get_pos_y()
		failed = not moved
	return not failed
	

