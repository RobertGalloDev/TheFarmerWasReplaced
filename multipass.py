from KrunkUtils import navigateTo
from KrunkUtils import pacmanTo
from KrunkTypes import farmTypes
from KrunkConfig import *

startx = 0
starty = 0
gridsize = 8
gridx = 8
gridy = 8
farmtype = "default"
croplayout = {}
myflowers = []
globalGrid = False


def tryTill(crop):
	gnd = get_ground_type()
	if (crop==Entities.Grass and gnd != Grounds.Grassland) or (crop!=Entities.Grass and gnd==Grounds.Grassland):
		till()

def farmPrep(myX = 0, myY = 0, farmSize = -1, farmtype = "default", globalLayout = False):
	navigateTo(myX,myY)
	if farmSize < 0:
		farmSize = get_world_size()
	
	mycrops = farmTypes[farmtype]
	if len(mycrops) < 1:
		mycrops = [Entities.Grass,Entities.Tree,Entities.Carrot]
	croplength = len(mycrops)

	for x in range(farmSize):
		for y in range(farmSize):
			if globalLayout:
				cropnum = (myX+x+myY+y)%croplength
			else:
				cropnum = (x+y)%croplength
			thisCrop = mycrops[cropnum]
			croplayout[(x,y)] = thisCrop
			
			tryTill(thisCrop)
			
			if thisCrop != Entities.Grass:
				harvest()
				plant(thisCrop)
				if thisCrop == Entities.Sunflower:
					myflowers.append(measure())

			if y < farmSize-1:
				move(North)
			else:
				navigateTo(get_pos_x(),myY)
		if x < farmSize-1:
			move(East)

def polyPrep(myX = 0, myY = 0, farmSizeX = -1, farmSizeY = -1, farmtype = "default", globalLayout = False):
	pacmanTo(myX,myY)
	if farmSizeX < 0:
		farmSizeX = get_world_size()
	if farmSizeY < 0:
		farmSizeY = get_world_size()
	
	mycrops = farmTypes[farmtype]
	if len(mycrops) < 1:
		mycrops = [Entities.Grass,Entities.Tree,Entities.Carrot]
	croplength = len(mycrops)

	for x in range(farmSizeX):
		for y in range(farmSizeY):
			if globalLayout:
				cropnum = (myX+x+myY+y)%croplength
			else:
				cropnum = (x+y)%croplength
			thisCrop = mycrops[cropnum]
			croplayout[(x,y)] = thisCrop
			
			tryTill(thisCrop)
			
			if thisCrop != Entities.Grass:
				harvest()
				plant(thisCrop)
				if thisCrop == Entities.Sunflower:
					myflowers.append(measure())

			if y < farmSizeY-1:
				move(North)
			else:
				navigateTo(get_pos_x(),myY)
		if x < farmSizeX-1:
			move(East)

def constantPrep():
	farmPrep(startx,starty,gridsize,farmtype,globalGrid)

def recalc(myX,myY,farmSize):
	retX = get_pos_x()
	retY = get_pos_y()
	navigateTo(myX,myY)
	newflowers = []
	for x in range(farmSize):
		for y in range(farmSize):
			if get_entity_type() != Entities.Sunflower:
				harvest()
				plant(Entities.Sunflower)

			newflowers.append(measure())
			if y < farmSize-1:
				move(North)
			else:
				navigateTo(get_pos_x(),myY)
		if x < farmSize-1:
			move(East)
	navigateTo(retX,retY)
	return newflowers

def harvestLoop(myX = 0, myY = 0, farmSize = -1, farmtype = "default",gbl=False):
	if farmSize < 0:
		farmSize = get_world_size() - myX
	lastX = myX + farmSize - 1
	lastY = myY + farmSize - 1
	
	if len(croplayout) < (farmSize*farmSize):
		farmPrep(myX,myY,farmSize,farmtype,gbl)

	while(True):
		navigateTo(myX,myY)
		for x in range(farmSize):
			for y in range(farmSize):
				here = get_entity_type()
				if here == Entities.Bush:
					if can_harvest():
						harvest()
						plant(Entities.Bush)
				elif here == Entities.Cactus:
					if can_harvest():
						if farmtype != "cactus":
							harvest()
							plant(Entities.Cactus)
				elif here == Entities.Carrot:
					if can_harvest():
						harvest()
						plant(Entities.Carrot)
				elif here == Entities.Dead_Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
				elif here == Entities.Grass:
					if can_harvest():
						harvest()
				elif here == Entities.Pumpkin:
					if can_harvest():
						if (farmtype != "pumpkin") or (farmtype=="pumpkin" and x==farmSize-1 and y==farmSize-1):
							harvest()
							plant(Entities.Pumpkin)
				elif here == Entities.Sunflower:
					if can_harvest():
						if len(myflowers) < farmSize * farmSize:
							print("uh oh")
							recalc(myX,myY,farmSize)
						if measure() == max(myflowers):
							harvest()
							myflowers.remove(max(myflowers))
							plant(Entities.Sunflower)
							myflowers.append(measure())
				elif here == Entities.Tree:
					if can_harvest():
						harvest()
						plant(Entities.Tree)
				elif here == None:
					plant(croplayout[(x,y)])
				else:
					if can_harvest():
						harvest()
						plant(here)
				
				if get_water() < 0.3:
					use_item(Items.Water)
						
				if y < farmSize-1:
					move(North)
				else:
					navigateTo(get_pos_x(),myY)
			if x < farmSize-1:
				move(East)

def polyHarvest(myX = 0, myY = 0, farmSizeX = -1, farmSizeY = -1, farmtype = "default",gbl=False):
	if farmSizeX < 0:
		farmSizeX = get_world_size()
	if farmSizeY < 0:
		farmSizeY = get_world_size()
	lastX = myX + farmSizeX - 1
	lastY = myY + farmSizeY - 1
	
	if len(croplayout) < (farmSizeX*farmSizeY):
		polyPrep(myX,myY,farmSizeX,farmSizeY,farmtype,gbl)

	while(True):
		navigateTo(myX,myY)
		for x in range(farmSizeX):
			for y in range(farmSizeY):
				here = get_entity_type()
				if here == Entities.Bush:
					if can_harvest():
						harvest()
						plant(Entities.Bush)
				elif here == Entities.Cactus:
					if can_harvest():
						if farmtype != "cactus":
							harvest()
							plant(Entities.Cactus)
				elif here == Entities.Carrot:
					if can_harvest():
						harvest()
						plant(Entities.Carrot)
				elif here == Entities.Dead_Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
				elif here == Entities.Grass:
					if can_harvest():
						harvest()
				elif here == Entities.Pumpkin:
					if can_harvest():
						if (farmtype != "pumpkin") or (farmtype=="pumpkin" and x==farmSizeX-1 and y==farmSizeY-1):
							harvest()
							plant(Entities.Pumpkin)
				elif here == Entities.Sunflower:
					if can_harvest():
						if len(myflowers) < farmSize * farmSize:
							print("uh oh")
							recalc(myX,myY,farmSize)
						if measure() == max(myflowers):
							harvest()
							myflowers.remove(max(myflowers))
							plant(Entities.Sunflower)
							myflowers.append(measure())
				elif here == Entities.Tree:
					if can_harvest():
						harvest()
						plant(Entities.Tree)
				elif here == None:
					plant(croplayout[(x,y)])
				else:
					if can_harvest():
						harvest()
						plant(here)
				
				if get_water() < 0.3:
					use_item(Items.Water)
						
				if y < farmSizeY-1:
					move(North)
				else:
					navigateTo(get_pos_x(),myY)
			if x < farmSizeX-1:
				move(East)

def constantLoop():
	harvestLoop(startx,starty,gridsize,farmtype,globalGrid)

def constPoly():
	polyPrep(startx,starty,gridx,gridy,farmtype,globalGrid)
	polyHarvest(startx,starty,gridx,gridy,farmtype,globalGrid)

def goFarm(x,y,size,type,glob):
	if type == "cactus":
		#do cactus things
		farmPrep(x,y,size,"default",glob)
		harvestLoop(x,y,size,"default",glob)
	else:
		farmPrep(x,y,size,type,glob)
		harvestLoop(x,y,size,type,glob)

def constFarm():
	goFarm(startx,starty,gridsize,farmtype,globalGrid)

globalGrid = True

farmtype = "nopower"
startx = 6
starty = 6
gridsize = 8
spawn_drone(constFarm)
startx = 14
spawn_drone(constFarm)
starty = 14
spawn_drone(constFarm)
startx = 6
spawn_drone(constFarm)

startx = 0
starty = 0
gridsize = 6
farmtype = "pumpkin"
spawn_drone(constFarm)

starty = 8
spawn_drone(constFarm)

starty = 16
spawn_drone(constFarm)

farmtype="wood"
gridx=6
gridy=2
starty=6
spawn_drone(constPoly)
starty=14
spawn_drone(constPoly)

starty = 0
startx = 12
spawn_drone(constFarm)

farmtype = "power"
startx = 6
spawn_drone(constFarm)

farmtype = "nopower"
startx = 18
gridx = 4
gridy = 6
spawn_drone(constPoly)



#farmtype = "nopower"
#startx = 8
#spawn_drone(constFarm)

#gridsize=4
#startx = 0
#starty = 8

#farmtype = "power"
#spawn_drone(constFarm)

#starty = 12
#farmtype = "nopower"
#spawn_drone(constFarm)

#startx = 4
#farmtype = "pumpkin"
#spawn_drone(constFarm)

#starty = 8
#farmtype = "nopower"
#spawn_drone(constFarm)

#startx = 8
#starty = 8
#gridsize = 8
#spawn_drone(constFarm)

#farmtype="pumpkin"
#startx = 0
#starty = 0
#constFarm()