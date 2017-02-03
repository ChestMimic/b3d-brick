def getMin(points = []):
	minX = None
	minY = None
	minZ = None
	for tp in points:
		minX = min(minX, tp[0]) if minX is not None else tp[0]
		minY = min(minY, tp[1]) if minY is not None else tp[1]
		minZ = min(minZ, tp[2]) if minZ is not None else tp[2]
	return {'X':minX, 'Y':minY, 'Z':minZ}

def getMax(points= []):
	minX = 0
	minY = 0
	minZ = None
	for tp in points:
		minX = max(minX, tp[0]) if minX is not None else tp[0]
		minY = max(minY, tp[1]) if minY is not None else tp[1]
		minZ = max(minZ, tp[2]) if minZ is not None else tp[2]
	return {'X':minX, 'Y':minY, 'Z':minZ}



if __name__ == "__main__":

	points = [
	(1,1,1),
	(0,0, 0),
	(0,1, 3),
	(13,-4, 8)]

	mini = getMin(points)
	maxi = getMax(points)
	bSize = .5

	index = mini['X']
	print("Mini X " + str(mini['X']))
	print("Mini Y " + str(mini['Y']))
	print("Mini Z " + str(mini['Z']))

	lsX = []
	lsY = []
	lsZ = []

	while(index <= maxi['X']):
		lsX.append(index)
		index = float(index) + bSize

	index = mini['Y']
	while(index <= maxi['Y']):
		lsY.append(index)
		index = index + bSize


	print(lsX)
	print(lsY)