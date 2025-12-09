import KrunkUtils
pumpkinSize = min([get_world_size()//2,6])

KrunkUtils.farmPrep(pumpkinSize)
pet_the_piggy()

def doFarming():
	while(True):
		KrunkUtils.navigateTo(0,0)
		for x in range(get_world_size() - pumpkinSize):
			for y in range(get_world_size()):
				harvested = KrunkUtils.tryHarvest(pumpkinSize)
				thisCrop = KrunkUtils.mapping[(x,y)] #KrunkUtils.whatCrop(x,y,pumpkinSize)
				
				if thisCrop != None and thisCrop != Entities.Grass and thisCrop != Entities.Sunflower:
					plant(thisCrop)
					if thisCrop == Entities.Tree and random() > 0.49 and num_items(Items.Fertilizer) > 0:
						use_item(Items.Fertilizer)
				elif thisCrop == Entities.Sunflower and harvested:
					plant(Entities.Sunflower)
					KrunkUtils.sunflowers[(x,y)] = measure()
					
				KrunkUtils.water()
				move(North)
			move(East)
			
def doFarmingoffset():
	offset = get_pos_x()
	while(True):
		KrunkUtils.navigateTo(offset,0)
		for i in range(get_world_size()-offset):
			for y in range(get_world_size()):
				x = i + offset
				harvested = KrunkUtils.tryHarvest(pumpkinSize)
				thisCrop = KrunkUtils.mapping[(x,y)] #KrunkUtils.whatCrop(x,y,pumpkinSize)
				
				if thisCrop != None and thisCrop != Entities.Grass and thisCrop != Entities.Sunflower:
					plant(thisCrop)
					if thisCrop == Entities.Tree and random() > 0.49 and num_items(Items.Fertilizer) > 0:
						use_item(Items.Fertilizer)
				elif thisCrop == Entities.Sunflower and harvested:
					plant(Entities.Sunflower)
					KrunkUtils.sunflowers[(x,y)] = measure()
					
				KrunkUtils.water()
				move(North)
			move(East)

if pumpkinSize > 0:
	KrunkUtils.navigateTo(pumpkinSize,0)
	spawn_drone(doFarmingoffset)
KrunkUtils.navigateTo(0,0)
doFarming()