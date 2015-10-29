"""
# Mesh
	This method sets the mesh controls, the element types, and specifies a global seed to make the mesh.
	The method makes sure that the number of nodes is between 60,000 and 75,000 inclusive.
	
	makeMesh(globalSeed) returns nodes and elements.
		*Input: 
			globalSeed: Numeric value for determining seed. Default is 20.
		*Output:
			nodes: Integer value for number of nodes.
			elements: Integer value for number of elements.
	
	EXAMPLE:
		numElm, numNodes = makeMesh(20) # Global seed is 20. 
		numElm, numNodes = makeMesh() # Global seed is 20. 
"""

from abaqus import mdb
import abaqusConstants as aq
import mesh

def makeMesh2D(globalSeed=20):
	import mesh
	part.setMeshControls(elemShape=aq.TRI, regions=(allSet.faces)) # Set to triangle shape
	part.setElementType(elemTypes=(mesh.ElemType(elemCode=aq.DC2D8, elemLibrary=aq.STANDARD), 
		mesh.ElemType(elemCode=aq.DC2D6, elemLibrary=aq.STANDARD)), regions=(allSet)) #
	nodes, elements = 0, 0 # Do I need this line?
	while True:
		part.seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=globalSeed)
		part.generateMesh()
		modelObject.rootAssembly.regenerate()
		nodes = len(modelObject.rootAssembly.instances['PART1'].nodes)
		elements = len(modelObject.rootAssembly.instances['PART1'].elements)
		if nodes < 60000:
			globalSeed = globalSeed * 0.80
		elif nodes > 95000:
			globalSeed = globalSeed * 1.20
		else:
			break
		
	
	return elements, nodes

# WARNING: Slow convergence happens FAR too often. 
def makeMesh3D(modelObject, modelRootAssembly, meshSeed=45, df=0.05):
	import mesh
	import random
	modelRootAssembly.setMeshControls(elemShape=aq.TET, regions=(modelRootAssembly.sets['assemblyAll'].cells), technique=aq.FREE)
	modelRootAssembly.setElementType(elemTypes=(mesh.ElemType(elemCode=aq.C3D20R, elemLibrary=aq.STANDARD), 
		mesh.ElemType(elemCode=aq.C3D15, elemLibrary=aq.STANDARD), mesh.ElemType(elemCode=aq.C3D10, elemLibrary=aq.STANDARD)),
		regions=(modelRootAssembly.sets['assemblyAll']))
	modelRootAssembly.setElementType(elemTypes=(mesh.ElemType(elemCode=aq.DC3D20, elemLibrary=aq.STANDARD),
		mesh.ElemType(elemCode=aq.DC3D15, elemLibrary=aq.STANDARD), mesh.ElemType(elemCode=aq.DC3D10, elemLibrary=aq.STANDARD)),
		regions=(modelRootAssembly.sets['assemblyAll']))
	nodes, elements = 0, 0
	countTot = 0
	dfs = [0.045, 0.05, 0.055, 0.06, 0.0650, 0.007, 0.0075, 0.008]
	#dfs = [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04]
	#meshs = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
	df = random.choice(dfs)
	#meshSeed = random.choice(meshs)
	totalCount = 0
	while True:
		totalCount = totalCount + 1
		print("number of mesh iterations " + str(totalCount))
		modelRootAssembly.seedPartInstance(deviationFactor=df, minSizeFactor=0.1, 
			regions=(modelRootAssembly.instances['matrixFull-1'], ), size=meshSeed)
		modelRootAssembly.generateMesh(regions=( modelRootAssembly.instances['matrixFull-1'], ))
		modelObject.rootAssembly.regenerate()
		nodes = len(modelObject.rootAssembly.instances['matrixFull-1'].nodes)
		elements = len(modelObject.rootAssembly.instances['matrixFull-1'].elements)
		
		break
		
		#if elements < 400000:
		#	df = random.choice(dfs)
		#	meshSeed = random.choice(meshs)
		#elif elements > 4000000:
		#	df = random.choice(dfs)
		#	meshSeed = random.choice(meshs)
		#else:
		#	break
		
		"""
		if elements < 35000:
			df = random.choice(dfs)
			meshSeed = meshSeed * 0.90
		elif elements < 75000:
			meshSeed = meshSeed * 0.95
		elif elements > 300000:
			meshSeed = meshSeed * 1.2
			df = random.choice(dfs)
		elif elements > 200000:
			meshSeed = meshSeed * 1.25
			df = random.choice(dfs)
		elif elements > 162000:
			meshSeed = meshSeed * 1.1
		else:
			break
		
		countTot = countTot + 1
		if countTot == 7:
			meshSeeds = [27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50, 52, 55]
			meshSeed = random.choice(meshSeeds)
			countTot = 0
			df = random.choice(dfs)
			
		#if nodes > 100000:
		#	meshSeeds = [25, 27.5, 30, 32.5, 35, 37.5, 40]
		#	meshSeed = random.choice(meshSeeds)
		#	df = random.choice(dfs)
		"""
		
	
	
	
	return elements, nodes, df, round(meshSeed)

### FIX
# Scoping and references!!!
# Need for extracting data
def makeElementSet(fullMatrixPart, modelRootAssembly):
	bottomFace = modelRootAssembly.instances['matrixFull-1'].faces.pointsOn[3]
	topFace = modelRootAssembly.instances['matrixFull-1'].faces.pointsOn[1]
	fullMatrixPart.Set(faces=fullMatrixPart.faces.findAt(topFace), name='top')
	fullMatrixPart.Set(faces=fullMatrixPart.faces.findAt(bottomFace), name='bot')


########### Info for testing Mesh
"""
import numpy
from abaqus import mdb
import abaqusConstants as aq 
from hAssembly import *
from hCoordinates import *
from hJob import *
from hMaterial import *
from hMesh import *
from hModel import *
from hPart import *
from hProperty import *
from hStep import *

### Increase distance delta in coordinate generation by interface length! 
interfacePortion = 0.10

materials = getMaterialList() # Load in material Data
matrix = "ESBR" # Choose the first experiment from TCNanoFillers
fillers = ["Alumina", "ZincOxide"] # Two fillers associated with first experiment

modelObject, modelName = createModel(2) # Create model database "Model-2"
side, radius, portions, dP, dM, cP, cM = defExperiment(modelObject, matrix, fillers[0]) 
defineMaterial(modelObject, "Interface", dM, (cP + cM)/2.0) # Define interface conductivity... Note that this will be generated randomly
seed = numpy.random.randint(10000) # Random seed for coordinate generation
radius, number = invPHR(portions[2], dP, radius, dM, side, False) # Returns specific radius size and number of inclusions for closest PHR value.
xVals, yVals, zVals, warningPoints, number = getPoints3D(seed, side, radius, number, interfacePortion, 0.05) # returns coordinates for inclusion locations. 

part = createMatrix(modelObject, side, False) # Create the matrix
edges1, vertices1, face1 = assignGeomSequence(part) # Create references to important sets in our matrix
part2 = createSphereParticle(modelObject, radius, side) # Create Particle part
edges2, vertices2, face2 = assignGeomSequence(part2) # Create references to important sets in particle 
part3 = createSphereParticle(modelObject, (radius + radius*interfacePortion), side, "Interface") # Create interface part
edges3, vertices3, face3 = assignGeomSequence(part3) # Create references to important sets in interface

matrixSet, particleSet, interfaceSet = create3DInitialSets(part, part2, side, part3, True) # create sets for particle, matrix, and interface
createSection(modelObject, part, matrix, matrixSet) # Create section for matrix material
createSection(modelObject, part2, fillers[0], particleSet) # Create section for filler material
createSection(modelObject, part3, "Interface", interfaceSet) # Create section for interface

modelRootAssembly = create3DMatrixInclusions(modelObject, number, xVals, yVals, zVals, True) # Create assembly and return references to assembly sets
define3DAssemblySets(modelRootAssembly, side)
temp1, temp2 = 328.15, 298.15 # Assign heat temperature to be used in experiment
heatStep3D(modelName, temp1, temp2) # apply heat BC
elements, nodes = makeMesh3D() # Draw mesh and return number of nodes and elements
makeElementSet(modelRootAssembly)
warningString, numEley = submitJob() # Submit job and take note of any warnings
avgHF, TC = getThermalProperties3D(radius, side)
"""

"""
elements = 100000
if elements < 35000:
	print("less than 35000")
elif elements < 75000:
	print("less than 75000 but greater than 35000")
elif elements > 300000:
	print("greater than 300000")
elif elements > 200000:
	print("greater than 200000 but less than 300000")
elif elements > 162000:
	print("greater than 162000 but less than 200000")
else:
	print("between 75000 and 162000")
"""