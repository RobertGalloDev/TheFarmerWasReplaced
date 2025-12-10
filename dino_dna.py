from KrunkUtils import navigateTo
from KrunkUtils import tryNavigate
from KrunkUtils import clearSlice
from KrunkUtils import clearMap

def randomChance():
	size = 0
	tryNavigate(0,0)
	change_hat(Hats.Dinosaur_Hat)
	x,y = measure()
	while tryNavigate(x,y):
		x,y = measure()
		size = size+1
	change_hat(Hats.Straw_Hat)

def getBones():
	change_hat(Hats.Straw_Hat)
	pet_the_piggy()
	change_hat(Hats.Dinosaur_Hat)

def tryStep(dir):
	if not move(dir):
		getBones()

def dinoLoop(worldsize = 12):
	if worldsize != get_world_size():
		set_world_size(worldsize)

	navigateTo(0,0)
	change_hat(Hats.Dinosaur_Hat)
	startpoints = []
	for j in range(get_world_size()):
		if j % 2 == 0:
			startpoints.append(j)
	while True:
		navigateTo(0,0)
		tryStep(North)
		for i in startpoints:
			#go up
			for y in range(get_world_size()-2):
				tryStep(North)
			tryStep(East)
			for y in range(get_world_size()-2):
				tryStep(South)
			if get_pos_x() < get_world_size()-1:
				tryStep(East)
		tryStep(South)
		while(get_pos_x() > 0):
			tryStep(West)
