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

materials = getMaterialList() # Load in material Data
matrix = "ESBR" # Choose the first experiment from TCNanoFillers
fillers = ["ZincOxide", "Alumina"] # Two fillers associated with first experiment

print('Matrix\tFiller\tPortion\tRadius\tNumber\tSide\tIntSize\tDelta\tCalcPor\tIntCond\tSeed\tNodes\tElements\tDevFac\tMeshSeed\tq\tdT\tk\tNoElmWarn\tWarn\n')

seed = None

interfacePortion = numpy.random.sample(1) * 1.15 + 0.10 # Between 0.15 and 0.45 greater than radius
interfacePortion = round(interfacePortion[0], 2)

delta = 0.15 

modelObject, modelName = createModel(2) 
side, radius, portions, dP, dM, cP, cM = defExperiment(modelObject, matrix, "Alumina")
radius = 46
number = 8
interfaceConductivity= numpy.random.sample(1) * (cP-cM) + cM # Between cM and cP
interfaceConductivity = int(interfaceConductivity[0])


defineMaterial(modelObject, "Interface", dM, interfaceConductivity) # Define interface conductivity... Note that this will be generated randomly

xVals, yVals, zVals = detCoordinatesAlumina() # returns coordinates for inclusion locations. 
calcPHR = round(calculatePHR3D(number, dP, radius, dM, side))

part = createMatrix(modelObject, side, False) # Create the matrix
edges1, vertices1, face1 = assignGeomSequence(part) # Create references to important sets in our matrix
part2 = createSphereParticle(modelObject, radius, side) # Create Particle part
edges2, vertices2, face2 = assignGeomSequence(part2) # Create references to important sets in particle 
part3 = createSphereParticle(modelObject, (radius + radius*interfacePortion), side, "Interface") # Create interface part
edges3, vertices3, face3 = assignGeomSequence(part3) # Create references to important sets in interface
matrixSet, particleSet, interfaceSet = create3DInitialSets(part, part2, side, part3) # create sets for particle, matrix, and interface

createSection(modelObject, part, matrix, matrixSet) # Create section for matrix material
createSection(modelObject, part2, "Alumina", particleSet) # Create section for filler material
createSection(modelObject, part3, "Interface", interfaceSet) # Create section for interface

warningPoints = ""

modelRootAssembly, fullMatrixPart = create3DMatrixInclusions(modelObject, part, part2, number, xVals, yVals, zVals, part3) # Create assembly and return references to assembly sets
assemblyTop, assemblyBottom, assemblyAll = define3DAssemblySets(modelRootAssembly, side)
temp1, temp2 = 328.15, 298.15 # Assign heat temperature to be used in experiment
heatStep3D(modelObject, assemblyBottom, assemblyTop, temp1, temp2) # apply heat BC
elements, nodes, df, meshSeed = makeMesh3D(modelObject, modelRootAssembly)  # Draw mesh and return number of nodes and elements
makeElementSet(fullMatrixPart, modelRootAssembly)
print(str(seed) + " " +str(number) + " " + str(radius) + " " + str(df) + " " + str(meshSeed) + " " + str(elements) + " " +str(nodes) + " " + warningPoints)
odbfileName = modelName
warningString, noElementsWarning = submitJob(modelName, odbfileName)  # Submit job and take note of any warnings
avgHF, TC = getThermalProperties3D(radius, side, temp1, temp2, odbfileName) # Extract relevant information about thermal properties

print(dataString(matrix, fillers[1], portions[0], radius, number, side, interfacePortion, delta, calcPHR, interfaceConductivity, seed, nodes, elements, df, meshSeed, avgHF, temp1, temp2, TC, warningString, warningPoints, noElementsWarning)) # Write the data to file
