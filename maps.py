from KrunkUtils import navigateTo
from KrunkTypes import *

def mazeGen(stayput=False):
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	midpoint = get_world_size() // 2 
	if substance >= num_items(Items.Weird_Substance):
		return False
	if not stayput:
		navigateTo(midpoint,midpoint)
	harvest()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance,substance)
	return True

def mazeRun():
	lastMove = None
	currentHeading = North
	
	splitChance = 1/(get_world_size()*4)

	while get_entity_type() == Entities.Hedge:
		if not move(rightOf[currentHeading]):
			if not move(currentHeading):
				if not move(leftOf[currentHeading]):
					currentHeading = behindOf[currentHeading]
				else:
					currentHeading = leftOf[currentHeading]
					lastMove = currentHeading
			else:
				lastMove = currentHeading
		else:
			currentHeading = rightOf[currentHeading]
			lastMove = currentHeading
		if random() < splitChance:
			spawn_drone(mazeRunLeft)
	harvest()

def mazeRunLeft():
	lastMove = None
	currentHeading = North
	splitChance = 1/(get_world_size()*4)
	
	while get_entity_type() == Entities.Hedge:
		if not move(leftOf[currentHeading]):
			if not move(currentHeading):
				if not move(rightOf[currentHeading]):
					currentHeading = behindOf[currentHeading]
				else:
					currentHeading = rightOf[currentHeading]
					lastMove = currentHeading
			else:
				lastMove = currentHeading
		else:
			currentHeading = leftOf[currentHeading]
			lastMove = currentHeading
		if random() < splitChance:
			spawn_drone(mazeRun)
	harvest()

interval = get_world_size()//3
startx = interval
starty = interval

def quadMaze():
	while True:
		navigateTo(startx,starty)
		while get_entity_type() != Entities.Hedge and get_entity_type() != Entities.Treasure:
			do_a_flip()
		pal = spawn_drone(mazeRunLeft)
		mazeRun()
		if pal != None:
			wait_for(pal)

def runner():
	navigateTo(startx,starty)
	return spawn_drone(quadMaze)
	
if get_entity_type() == Entities.Hedge:
	lefty = spawn_drone(mazeRunLeft)
	mazeRun()
	wait_for(lefty)
	
startx = get_world_size() - interval
starty = get_world_size() - interval
TR = spawn_drone(runner)

startx = interval
TL = spawn_drone(runner)

startx = starty
starty = interval
BR = spawn_drone(runner)

startx = interval
wait_for(TR)
wait_for(TL)
wait_for(BR)
while True:
	navigateTo(startx,starty)
	mazeGen(True)
	fren = spawn_drone(mazeRunLeft)
	mazeRun()
	if fren != None:
		wait_for(fren)