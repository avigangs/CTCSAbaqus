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

# Get material list
materials = getMaterialList() # Load in material Data
matrix = "EpoxyResin" # Choose the first experiment from TCNanoFillers
fillers = ["Alumina"] # Two fillers associated with first experiment
filler = fillers[0]
print('Matrix\tFiller\tPortion\tRadius\tNumber\tSide\tIntSize\tDelta\tCalcPor\tIntCond\tSeed\tNodes\tElements\tDevFac\tMeshSeed\tq\tdT\tk\tNoElmWarn\tWarn\n')
seed = None

# make model
modelObject, modelName = createModel(2)

# define materials
side, radius, portions, dP, dM, cP, cM = defExperiment(modelObject, matrix, filler)

# which phr
vol = portions[0]
#densityMatrix = materials[matrix]['densityM']
#densityFiller = materials[matrix]['fillers']['Alumina']['densityF']
#sideMatrix = materials[matrix]['fillers']['Alumina']['side']

# get coordinates, interface Max, random interface size, etc.
radius, number = invVolumeAlternate3D(vol, radius, side)
delta = 0.15
intPortionLimit = getInterfacePortionLimit(side, radius, number)
#interfacePortion = numpy.random.sample(1) * (intPortionLimit-0.15) + 0.15 # random 0.1 to limit inclusive
#interfacePortion = round(interfacePortion[0], 3)
interfacePortion = intPortionLimit / 2.0
xVals, yVals, zVals = getPoints3dDeterministic(side, radius, number)

## define range for interface conductivity # Either constant or varying depending on other constants
# run rest of simulation
#interfaceConductivity= numpy.random.sample(1) * (cP-cM) + cM # Between cM and cP
#interfaceConductivity = int(interfaceConductivity[0])
interfaceConductivity = (cP + cM) / 2.0

# Define interface materials
defineMaterial(modelObject, "Interface", dM, interfaceConductivity) # Define interface conductivity... Note that this will be generated randomly

# Check PHR values
calcVol = calculateVolume(number, radius, side)

part = createMatrix(modelObject, side, False) # Create the matrix
edges1, vertices1, face1 = assignGeomSequence(part) # Create references to important sets in our matrix
part2 = createSphereParticle(modelObject, radius, side) # Create Particle part
edges2, vertices2, face2 = assignGeomSequence(part2) # Create references to important sets in particle 
part3 = createSphereParticle(modelObject, (radius + radius*interfacePortion), side, "Interface") # Create interface part
edges3, vertices3, face3 = assignGeomSequence(part3) # Create references to important sets in interface
matrixSet, particleSet, interfaceSet = create3DInitialSets(part, part2, side, part3) # create sets for particle, matrix, and interface

createSection(modelObject, part, matrix, matrixSet) # Create section for matrix material
createSection(modelObject, part2, filler, particleSet) # Create section for filler material
createSection(modelObject, part3, "Interface", interfaceSet) # Create section for interface

warningPoints = ""

modelRootAssembly, fullMatrixPart = create3DMatrixInclusions(modelObject, part, part2, number, xVals, yVals, zVals, part3) # Create assembly and return references to assembly sets
assemblyTop, assemblyBottom, assemblyAll = define3DAssemblySets(modelRootAssembly, side)
temp1, temp2 = 328.15, 298.15 # Assign heat temperature to be used in experiment
heatStep3D(modelObject, assemblyBottom, assemblyTop, temp1, temp2) # apply heat BC
limitOutputHFL(modelObject, assemblyBottom, assemblyTop) # Limit ODB Output
elements, nodes, df, meshSeed = makeMesh3D(modelObject, modelRootAssembly, 10, 0.05)  # Draw mesh and return number of nodes and elements
makeElementSet(fullMatrixPart, modelRootAssembly)
print(str(seed) + " " +str(number) + " " + str(radius) + " " + str(df) + " " + str(meshSeed) + " " + str(elements) + " " +str(nodes) + " " + warningPoints)
fileName = "job1341"
jobFi = createJob(modelName, fileName)
generateINP(fileName)

#odbfileName = modelName
#warningString, noElementsWarning = submitJob(modelName, odbfileName)  # Submit job and take note of any warnings
#avgHF, TC = getThermalProperties3D(radius, side, temp1, temp2, odbfileName) # Extract relevant information about thermal properties

#print(dataString(matrix, fillers[1], portions[3], radius, number, side, interfacePortion, delta, calcPHR, interfaceConductivity, seed, nodes, elements, df, meshSeed, avgHF, temp1, temp2, TC, warningString, warningPoints, noElementsWarning)) # Write the data to file
