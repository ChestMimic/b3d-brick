#import bpy

if __name__ == "__main__":
	points = [
	(1,1),
	(0,0),
	(0,1),
	(13,0)]


	minX = 0
	maxX = 0
	minY = 0
	maxY = 0
	for tp in points:
		minX = min(minX, tp[0])
		maxX = max(maxX, tp[0])
		minY = min(minY, tp[1])
		maxY = max(maxY, tp[1])

	bSize = .5

	index = 0
	
	lsX = []
	lsY = []

	while(index <= maxX):
		lsX.append(index)
		index = index + bSize

	index = 0
	while(index <= maxY):
		lsY.append(index)
		index = index + bSize

	print(lsX)
	print(lsY)