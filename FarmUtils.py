from KrunkUtils import *

def whatCrop(x,y,pumpkinSize = 0):
	cropId = (x+y)%numCrops
	if pumpkinSize > 0 and x < pumpkinSize and y < pumpkinSize:
		return Entities.Pumpkin
	if cropId == 1:
		return Entities.Tree
	elif cropId == 2:
		return Entities.Carrot
	elif cropId == 3:
		return Entities.Sunflower
	elif cropId == 4:
		return Entities.Pumpkin
	else:
		return Entities.Grass

def tryHarvest(pumpkinSize = 0):
	retVal = False
	if get_entity_type() == Entities.Dead_Pumpkin:
		retVal = harvest()
	elif pumpkinSize > 0 and get_entity_type() == Entities.Pumpkin:
		if get_pos_x() == pumpkinSize-1 and get_pos_y() == pumpkinSize-1 and can_harvest():
			retVal = harvest()
	elif pumpkinSize == 0 and get_entity_type() == Entities.Pumpkin:
		retVal = harvest()
	elif get_entity_type() == Entities.Sunflower and can_harvest():
		if measure() >= flowerPower() or len(sunflowers) < 10:
			retVal = harvest()
	elif get_entity_type() != None and can_harvest():
		retVal = harvest()
	elif get_entity_type() == None:
		retVal = True
	return retVal


def farmPrep(pumpkinSize=0):
	resetPos()
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			
			thisCrop = whatCrop(x,y,pumpkinSize)
			mapping[(x,y)] = thisCrop
			
			if thisCrop != Entities.Grass:
				if get_ground_type() != Grounds.Soil:
					till()
				harvest()
				plant(thisCrop)
				if thisCrop == Entities.Sunflower:
					sunflowers[(x,y)] = measure()
			else:
				if get_ground_type() != Grounds.Grassland:
					till()
			
			move(North)
		move(East)