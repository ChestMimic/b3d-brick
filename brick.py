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
	"version":(0,2,0),
	"blender":(2,78,0),
	"support":"TESTING",
	"category":"Objects",
	"author":"Mark Fitzgibbon"
}

##################################
#!            IMPORTS           !#
##################################
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

class NBrick:
	'''
	NBrick Brick class with a known number of subdivisions
	'''
	def __init__(self, base = (4,4,2), subdivs = 1):
		'''
		Construct using a Brick and desired number of subdivisions
		base - Brick object to base length, width, and height off of
		subdivs - Number of subdivided sections. 1 is expected minimum, no divisions made
		'''
		self.base = base
		self.subdivs = subdivs

	def genMeshData(self):
		'''
		Create Blender compatible lists for vertex and face data
		'''

		#Self-assign empty lists
		self.verts = []
		self.edges= []
		self.faces = []

		#1 Subdivision level creates 2 edges per axis
		numX  = self.subdivs + 1

		faceIndex = 0

		#Lambdas defining single axis coordinate positioning
		posit = lambda n, m: -self.base[n]/2 + (m * (self.base[n])/self.subdivs)
		facet = lambda n, m: (self.base[n]/2) * (-1 if m%2 == 0 else 1)

		#Each face of a cuboid
		while(faceIndex < 6):
			#Starting point of side's vertices
			indx = len(self.verts)

			#Iterate through a plane
			for i in range(0, numX):
				for j in range(0, numX):
					#This started as a really good idea, I swear
					x = facet(0, faceIndex) if (faceIndex is 0 or faceIndex is 1) else posit(0, (i if (faceIndex is 2 or faceIndex is 3) else j)) 
					y = facet(1, faceIndex) if (faceIndex is 2 or faceIndex is 3) else posit(1, (i if (faceIndex is 4 or faceIndex is 5) else j)) 
					z = facet(2, faceIndex) if (faceIndex is 4 or faceIndex is 5) else posit(2, (i if (faceIndex is 0 or faceIndex is 1) else j)) 
					vrt = (x, y, z)
					self.verts.append(vrt)
			count = 0
			for i in range(0, numX * (numX-1)):
				if count < numX - 1:
					#Circle around vertexes with a knonw order in a list
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
		default = 0)

	def randVertsBMesh(mesh, ran= .05, seed = 0):
		'''
		Apply noise to mesh
		ran - range of random values, from negative ran to positive ran
		seed - seed value to use with random
		'''
		random.seed(seed)
		bm = bmesh.new()
		bm.from_mesh(mesh)

		#Correct mesh errors caused by genMeshData 
		bmesh.ops.automerge(bm, verts = bm.verts, dist = 0.001)
		bmesh.ops.recalc_face_normals(bm, faces = bm.faces)

		#For each vertice randomize addition
		for v in bm.verts:
			v.co.x += random.uniform(-ran, ran)
			v.co.y += random.uniform(-ran, ran)
			v.co.z += random.uniform(-ran, ran)

		#Apply modifications to mesh
		bm.to_mesh(mesh)
		bm.free()

	def newBrick(self, length=length, width=width, height=height, subds=subds, intensity=intensity, seed=seed, location=bpy.context.scene.cursor_location):
		#Create mesh data
		mesh_data = bpy.data.meshes.new("brick_mesh_data")
		br = (length, width, height)
		samp_brick = NBrick(br, subds)
		samp_brick.genMeshData()
		mesh_data.from_pydata(samp_brick.verts, samp_brick.edges, samp_brick.faces)
		self.randVertsBMesh(mesh_data, intensity, seed)
		mesh_data.update()

		#create blender object
		obj = bpy.data.objects.new("Brick", mesh_data)
		obj.location = location

		#Link object to mesh data
		scene = bpy.context.scene
		scene.objects.link(obj)

	def execute(self, context):
		self.newBrick()
		return {'FINISHED'}

class WallGeneratorOperator(bpy.types.Operator):
	bl_idname = "object.brick_wall"
	bl_label = "Brick Wall"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		return {'FINISHED'}

##################################
#!    USER INTERFACE BUTTONS    !#
##################################

def add_Brick_button(self, context):
	'''
	Add Brick button for Add menu
	'''
	self.layout.operator(
		BrickGeneratorOperator.bl_idname,
		text = "Brick",
		icon = "MOD_MIRROR") #Find a better icon

##################################
#! REGISTER & UNREGISTER BLOCKS !#
##################################

def register():
	#Operators
	bpy.utils.register_class(BrickGeneratorOperator)
	#Buttons
	bpy.types.INFO_MT_add.append(add_Brick_button)
	#Keymaps
	wm = bpy.context.window_manager
	km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
	addon_keymaps.append(km)
	
def unregister():
	bpy.utils.unregister_class(BrickGeneratorOperator)
	bpy.types.INFO_MT_add.remove(add_Brick_button)
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