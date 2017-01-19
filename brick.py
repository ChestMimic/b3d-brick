#import bpy

class Brick:
	def __init__(self, length=4, width = 4, height = 2):
		self.lwh = (length, width, height)

	def genMeshData(self):
		verts = []
		edges = []
		faces = []

		#Vertexes
		verts.append((self.lwh[0], self.lwh[1], self.lwh[2]))	#0
		verts.append((self.lwh[0], self.lwh[1], -self.lwh[2]))	#1
		verts.append((self.lwh[0], -self.lwh[1], self.lwh[2]))	#2
		verts.append((self.lwh[0], -self.lwh[1], -self.lwh[2]))	#3
		verts.append((-self.lwh[0], self.lwh[1], self.lwh[2]))	#4
		verts.append((-self.lwh[0], self.lwh[1], -self.lwh[2]))	#5
		verts.append((-self.lwh[0], -self.lwh[1], self.lwh[2]))	#6
		verts.append((-self.lwh[0], -self.lwh[1], -self.lwh[2]))#7

		#Faces
		faces.append((2,3,6,7)) #-Y
		faces.append((0,1,4,5)) #+Y
		faces.append((0,1,2,3)) #+X
		faces.append((4,5,6,7))	#-X
		faces.append((0,2,4,6))	#+Z
		faces.append((1,3,5,7))	#-Z

		return (verts, edges, faces)


def getMin(points = []):
	minX = 0
	minY = 0
	for tp in points:
		minX = min(minX, tp[0])
		minY = min(minY, tp[1])

	return {'X':minX, 'Y':minY}

def getMax(points= []):
	minX = 0
	minY = 0
	for tp in points:
		minX = max(minX, tp[0])
		minY = max(minY, tp[1])

	return {'X':minX, 'Y':minY}

if __name__ == "__main__":
	points = [
	(1,1),
	(0,0),
	(0,1),
	(13,-4)]

	mini = getMin(points)
	maxi = getMax(points)
	bSize = .5

	index = mini['X']
	print(index)
	
	lsX = []
	lsY = []

	while(index <= maxi['X']):
		lsX.append(index)
		index = float(index) + bSize

	index = mini['Y']
	while(index <= maxi['Y']):
		lsY.append(index)
		index = index + bSize

	print(lsX)
	print(lsY)