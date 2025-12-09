import KrunkUtils

def clearcut():
	for y in range(get_world_size()):
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		move(North)
	return True

def startover():
	KrunkUtils.navigateTo(0,0)
	for x in range(get_world_size()):
		if not spawn_drone(clearcut):
			clearcut()
		move(East)

def check(dir):
	if get_pos_x() == 0 and dir == West:
		return False
	if get_pos_x() == get_world_size()-1 and dir == East:
		return False
	if get_pos_y() == 0 and dir == South:
		return False
	if get_pos_y() == get_world_size()-1 and dir == North:
		return False
	if dir == North or dir == East:
		if measure() > measure(dir):
			swap(dir)
			return True
	if dir == South or dir == West:
		if measure() < measure(dir):
			swap(dir)
			return True
	return False

def sortRow(yval = -1):
	if yval < 0:
		yval = get_pos_y()
	KrunkUtils.navigateTo(0,yval)
	sorted = False
	while not sorted:
		oops = False
		for x in range(get_world_size()):
			oops = check(West) or oops
			oops = check(East) or oops
			if oops:
				check(West)
			move(East)
		sorted = not oops
	return True

def sortCol(xval = -1):
	if xval < 0:
		xval = get_pos_x()
	KrunkUtils.navigateTo(xval,0)
	sorted = False
	while not sorted:
		oops = False
		for y in range(get_world_size()):
			oops = check(South) or oops
			oops = check(North) or oops
			if oops:
				check(South)
			move(North)
		sorted = not oops
	return True

def cactiline():
	for _ in range(get_world_size()):
		plant(Entities.Cactus)
		move(East)

def cacti():
	KrunkUtils.navigateTo(0,0)
	for y in range(get_world_size()):
		if not spawn_drone(cactiline):
			cactiline()
		move(North)

def sort():
	KrunkUtils.navigateTo(0,0)
	for y in range(get_world_size()):
		if not spawn_drone(sortRow):
			sortRow()
		move(North)
	KrunkUtils.navigateTo(0,0)
	while num_drones() > 1:
		do_a_flip()
	for x in range(get_world_size()):
		if not spawn_drone(sortCol):
			sortCol()
		move(East)

startover()
while num_items(Items.Cactus) < 1000000:
	cacti()
	sort()
	while num_drones() > 1:
		do_a_flip()
	harvest()