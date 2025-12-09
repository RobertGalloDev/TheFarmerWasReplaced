#Configuration
minWater = 0.1
minBuckets = 100
mapping = {}
sunflowers = {}

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
	navigateTo(0,0)

def clearSlice():
	for y in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		move(North)

def clearMap():
	navigateTo(0,0)
	for x in range(get_world_size()):
		if not spawn_drone(clearSlice):
			clearSlice()

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
	

def water():
	if get_water() < minWater and num_items(Items.Water) > minBuckets:
		use_item(Items.Water)
		return True
	return False
