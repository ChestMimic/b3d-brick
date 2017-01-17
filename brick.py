#import bpy

if __name__ == "__main__":
	points = [
	(1,1),
	(0,0),
	(0,1),
	(1,0)]

	bSize = .5

	index = 0
	minX = 0
	maxX = 1
	minY = 0
	maxY = 1
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