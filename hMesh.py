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
def makeMesh3D(modelObject, modelRootAssembly, meshSeed=35, df=0.05):
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
	#dfs = [0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075]
	#meshs = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
	#df = random.choice(dfs)
	#meshSeed = random.choice(meshs)
	#totalCount = 0
	while True:
		#totalCount = totalCount + 1
		#print("number of mesh iterations " + str(totalCount))
		modelRootAssembly.seedPartInstance(deviationFactor=df, minSizeFactor=0.1, 
			regions=(modelRootAssembly.instances['matrixFull-1'], ), size=meshSeed)
		modelRootAssembly.generateMesh(regions=( modelRootAssembly.instances['matrixFull-1'], ))
		modelObject.rootAssembly.regenerate()
		nodes = len(modelObject.rootAssembly.instances['matrixFull-1'].nodes)
		elements = len(modelObject.rootAssembly.instances['matrixFull-1'].elements)
		break
		"""
		if elements < 35000:
			newMeshSeed = [i for i in meshs if i <= 40]
			newdfs = [i for i in dfs if i <= 0.05]
			df = random.choice(newdfs)
			meshSeed = random.choice(newMeshSeed)
		elif elements < 75000:
			newMeshSeed = [i for i in meshs if i <= 65]
			newdfs = [i for i in dfs if i <= 0.07]
			df = random.choice(newdfs)
			meshSeed = random.choice(newMeshSeed)
		elif elements > 300000:
			newMeshSeed = [i for i in meshs if i >= 65]
			newdfs = [i for i in dfs if i >= 0.05]
			df = random.choice(newdfs)
			meshSeed = random.choice(newMeshSeed)
		elif elements > 200000:
			newMeshSeed = [i for i in meshs if i >= 25]
			newdfs = [i for i in dfs if i >= 0.04]
			df = random.choice(newdfs)
			meshSeed = random.choice(newMeshSeed)
		elif elements > 162000:
			meshSeed = meshSeed * 1.1
			df = df*1.1
		else:
			break
		
		countTot = countTot + 1
		if countTot == 7:
			countTot = 0
			df = random.choice(dfs)
			meshSeed = random.choice(meshs)
		
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

materials = getMaterialList()
matrix_materials = materials.keys()
epoxyResin = materials[matrix_materials[0]]
siliconRubber = materials[matrix_materials[1]]
polystyrene = materials[matrix_materials[2]]
esbr = materials[matrix_materials[3]]

epoxyResinFillers = epoxyResin['fillers'] # 4
siliconRubberFillers = siliconRubber['fillers'] # 3
polystyreneFillers = polystyrene['fillers'] # 2
esbrFillers = esbr['fillers']  # 2

epFillers = epoxyResinFillers.keys()
srFillers = siliconRubber['fillers'].keys() # 3
polyFillers = polystyrene['fillers'].keys()  # 2
eFillers = esbr['fillers'].keys()   # 2

modelObject, modelName = createModel(2)
side, radius, portions, dP, dM, cP, cM = defExperiment(modelObject, matrix_materials[0], epFillers[0])

key1 = matrix_materials[0]
key2 = epFillers[0]

phrs = epoxyResinFillers[epFillers[0]]['volPortion']
phr = phrs[0]


#radius, number = invPHRAlternate3D(phr, dP, radius, dM, side)
#calcPHR = round(calculatePHR3D(number, dP, radius, dM, side))

radius, number = invVolumeAlternate3D(phr, radius, side)
calcPHR = round(calculateVolume(number, radius, side), 3)

delta = 0.18

interfaceConductivity= numpy.random.sample(1) * (cP-cM) + cM # Between cM and cP
interfaceConductivity = int(interfaceConductivity[0])
#interfaceConductivity = int((cP+cM)/2.0)
# Define interface materials
defineMaterial(modelObject, "Interface", dM, interfaceConductivity)
intPortionLimit = getInterfacePortionLimit(side, radius, number, delta)

while intPortionLimit < 0:
	delta = delta + 0.1 * delta
	interfaceConductivity= numpy.random.sample(1) * (cP-cM) + cM # Between cM and cP
	interfaceConductivity = int(interfaceConductivity[0])
	#interfaceConductivity = int((cP+cM)/2.0)
	# Define interface materials
	defineMaterial(modelObject, "Interface", dM, interfaceConductivity)
	intPortionLimit = getInterfacePortionLimit(side, radius, number, delta)


interfacePortion = numpy.random.sample(1) * (intPortionLimit-delta) + delta # random delta to limit inclusive
interfacePortion = round(interfacePortion[0], 3)
xVals, yVals, zVals = getPoints3dDeterministic(side, radius, number)

part = createMatrix(modelObject, side, False) # Create the matrix
edges1, vertices1, face1 = assignGeomSequence(part) # Create references to important sets in our matrix
part2 = createSphereParticle(modelObject, radius, side) # Create Particle part
edges2, vertices2, face2 = assignGeomSequence(part2) # Create references to important sets in particle 
part3 = createSphereParticle(modelObject, (radius + radius*interfacePortion), side, "Interface") # Create interface part
edges3, vertices3, face3 = assignGeomSequence(part3) # Create references to important sets in interface
matrixSet, particleSet, interfaceSet = create3DInitialSets(part, part2, side, part3) # create sets for particle, matrix, and interface
createSection(modelObject, part, key1, matrixSet) # Create section for matrix material
createSection(modelObject, part2, key2, particleSet) # Create section for filler material
createSection(modelObject, part3, "Interface", interfaceSet) # Create section for interface
modelRootAssembly, fullMatrixPart = create3DMatrixInclusions(modelObject, part, part2, number, xVals, yVals, zVals, part3) # Create assembly and return references to assembly sets
assemblyTop, assemblyBottom, assemblyAll = define3DAssemblySets(modelRootAssembly, side)
temp1, temp2 = 328.15, 298.15 # Assign heat temperature to be used in experiment
heatStep3D(modelObject, assemblyBottom, assemblyTop, temp1, temp2) # apply heat BC
limitOutputHFL(modelObject, assemblyBottom, assemblyTop) # Limit ODB Output
elements, nodes, df, meshSeed = makeMesh3D(modelObject, modelRootAssembly, 1, 0.05)  # Draw mesh and return number of nodes and elements
makeElementSet(fullMatrixPart, modelRootAssembly)

print(delta)
print (intPortionLimit)
print(interfacePortion)
print(df)
print(meshSeed)

"""

""" delta = 25 seems very safe for low errors
MESH MAP delta 0.2 with 64 particle possibility
epoxyResin Alumina seed 1 control 0.05 particles 27 elements 0.8 millionish 0 errors intertfacePortion 0.058 
epoxyResin Alumina seed 0.95 control 0.04 particles 27 elements 1 millionish 3 errors interfacePortion 0.145
epoxyResin Alumina seed 0.9 control 0.0375 particles 27 elements 1.2 millionish 5 errors interfacePortion 0.145
epoxyResin Alumina seed 0.85 control 0.035 particles 27 elements 1.4 millionish 5 errors interfacePortion 0.145
epoxyResin Alumina seed 0.80 control 0.0325 particles 27 elements 1.5 millionish 5 errors interfacePortion 0.145
epoxyResin Alumina seed 0.80 control 0.0325 particles 27 elements 1.5 millionish 5 errors interfacePortion 0.145
epoxyResin Alumina seed 0.75 control 0.030 particles 27 elements 1.8 millionish 14 errors interfacePortion 0.145
epoxyResin Alumina seed 1 control 0.05 particles 27 elements 0.8 millionish 33 errors interfacePortion 0.109
epoxyResin Alumina seed 0.95 control 0.045 particles 27 elements 1 millionish 3 errors interfacePortion 0.109
epoxyResin Alumina seed 0.90 control 0.045 particles 27 elements 1.1 millionish 10 errors interfacePortion 0.109
epoxyResin Alumina seed 0.85 control 0.0425 particles 27 elements 1.3 millionish 28 errors interfacePortion 0.109
epoxyResin Alumina seed 1 control 0.05 particles 27 elements 0.8 millionish 2 errors interfacePortion 0.131
epoxyResin Alumina seed 0.95 control 0.045 particles 27 elements 1 millionish 2 errors interfacePortion 0.131
epoxyResin Alumina seed 0.90 control 0.0425 particles 27 elements 1.2 millionish 0 errors interfacePortion 0.131
epoxyResin Alumina seed 1 control 0.05 particles 27 elements 1 millionish 106700 errors interfacePortion 0.08

delta = 18 (safer.. also make interface portion the same as delta)
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