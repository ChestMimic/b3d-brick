# BEGIN GPL BLOCK    
#    Generates bricks and nontextured brick structures
#    Copyright (C) 2017  Mark Fitzgibbon
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# END GPL BLOCK
bl_info = {
	"name":"Brick",
	"description":"Generates bricks and nontextured brick structures",
	"tracker_url":"https://github.com/ibbolia/b3d-brick/issues",
	"version":(0,1,0),
	"blender":(2,78,0),
	"support":"TESTING",
	"category":"Objects",
	"author":"Mark Fitzgibbon"
}

import random

#Blender3D imports
import bpy
import bmesh
from bpy.props import FloatProperty, IntProperty

##################################
#!        GLOBAL VARIABLES      !#
##################################
addon_keymaps = []


##################################
#!       CLASS DEFINITIONS      !#
##################################

class Brick:
	'''
	Generic Brick class
		Contains length, width, and height 
		Can generate vertices & faces as lists
	'''
	def __init__(self, length=4, width = 4, height = 2):
		'''
		Constructor defaults to a 4x4x2 brick
		length - Desired length of Brick 
		width - Desired width of Brick
		height - Desired height of Brick
		B3D expected to interpret as (X,Y,Z) == (length, width, height)
		'''
		self.lwh = (length, width, height)

	def genMeshData(self):
		'''
		Use lwh to generate verts, edges, and faces as lists
		'''
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

		#Edges remains empty in a correctly formed Brick

		#Faces
		#Blender determines normals by vertices in a face clockwise (!?! Might be reverse 2017-01-24)
		faces.append((6,7,3,2)) #-Y (Front)
		faces.append((1,5,4,0)) #+Y (Back)
		faces.append((2,3,1,0)) #+X (Right)
		faces.append((7,6,4,5))	#-X (Left)
		faces.append((4,6,2,0))	#+Z (Top)
		faces.append((3,7,5,1))	#-Z (Bottom)

		#Assign values to self
		self.verts = verts 
		self.edges = edges
		self.faces = faces

class NBrick:
	'''
	NBrick Brick class with a known number of subdivisions
	'''
	def __init__(self, base = Brick(), subdivs = 1):
		'''
		Construct using a Brick and desired number of subdivisions
		base - Brick object to base length, width, and height off of
		subdivs - Number of subdivided sections. 1 is expected minimum, no divisions made
		'''
		self.base = base
		self.subdivs = subdivs

	def genMeshData(self):
		self.verts = []
		self.edges= []
		self.faces = []

		numX  = self.subdivs + 1

		faceIndex = 0

		posit = lambda n: -self.base.lwh[n]/2 + (i * (self.base.lwh[n])/self.subdivs)
		facet = lambda n, m: (self.base.lwh[n]/2) * (-1 if m%2 == 0 else 1)

		while(faceIndex < 6):
			indx = len(self.verts)

			#XPos
			for i in range(0, numX):
				for j in range(0, numX):
					x = facet(0, faceIndex) if (faceIndex is 0 or faceIndex is 1) else posit(0) 
					y = facet(1, faceIndex) if (faceIndex is 2 or faceIndex is 3) else posit(1) 
					z = facet(2, faceIndex) if (faceIndex is 4 or faceIndex is 5) else posit(2) 

					vrt = (x, y, z)
					self.verts.append(vrt)

			count = 0
			for i in range(0, numX * (numX-1)):
				if count < numX - 1:
					A = i + indx
					B = i + 1 + indx
					C = (i+numX)+1 + indx
					D = (i+ numX) + indx

					face = (A, B, C, D)
					self.faces.append(face)
					count = count + 1
				else:
					count = 0
			faceIndex = faceIndex + 1

##################################
#!       CLASSLESS METHODS      !#
##################################

def randVertsBMesh(mesh, ran= .05, seed = 0):
	'''
	Apply noise to mesh
	ran - range of random values, from negative ran to positive ran
	seed - seed value to use with random
	'''
	random.seed(seed)
	bm = bmesh.new()
	bm.from_mesh(mesh)

	bmesh.ops.automerge(bm, verts = bm.verts, dist = 0.001)
	bmesh.ops.recalc_face_normals(bm, faces = bm.faces)

	for v in bm.verts:
		v.co.x += random.uniform(-ran, ran)
		v.co.y += random.uniform(-ran, ran)
		v.co.z += random.uniform(-ran, ran)

	bm.to_mesh(mesh)
	bm.free()

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

##################################
#!       BLENDER OPERATORS      !#
##################################

class BrickGeneratorOperator(bpy.types.Operator):
	bl_idname = "object.brick"
	bl_label = "Brick"
	bl_options = {'REGISTER', 'UNDO'}

	subds = IntProperty(
		name= "Subdivisions",
		min = 1,
		default = 1)

	length = FloatProperty(
		name = "length",
		default = 1.0)
	width = FloatProperty(
		name = "width",
		default = 2.0)
	height = FloatProperty(
		name = "height",
		default = 1.0)
	intensity = FloatProperty(
		name = "Noise Intensity",
		default = 0.05)
	seed = IntProperty(
		name="Random Seed",
		default = random.seed())

	def execute(self, context):
		#Create mesh data
		mesh_data = bpy.data.meshes.new("brick_mesh_data")
		br = Brick(self.length, self.width, self.height)
		samp_brick = NBrick(br, self.subds)
		samp_brick.genMeshData()
		mesh_data.from_pydata(samp_brick.verts, samp_brick.edges, samp_brick.faces)
		randVertsBMesh(mesh_data, self.intensity, self.seed)

		mesh_data.update()

		#create blender object
		obj = bpy.data.objects.new("Brick", mesh_data)
		obj.location = bpy.context.scene.cursor_location

		#Link object to mesh data
		scene = bpy.context.scene
		scene.objects.link(obj)

		return {'FINISHED'}

##################################
#! REGISTER & UNREGISTER BLOCKS !#
##################################

def register():
	bpy.utils.register_class(BrickGeneratorOperator)

	wm = bpy.context.window_manager
	km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
	#kmi = km.keymap_items.new(BrickGeneratorOperator.bl_idname, 'SPACE', 'PRESS', ctrl=False, shift=False)
	#kmi.properties.subds = 1
	addon_keymaps.append(km)
	
def unregister():
	bpy.utils.unregister_class(BrickGeneratorOperator)
	#bpy.types.INFO_MT_add.remove(add_MirrorBox_button)
	#for km, kmi in addon_keymaps:
	#	km.keymap_items.remove(kmi)
	addon_keymaps.clear()



if __name__ == "__main__":

	register()

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