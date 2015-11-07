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

modelObject, modelName = createModel(2)
seed = 15
side = 100
radius = 10
volume = 0.15
number = invVolumeSphere(radius, side, volume)
xCoords, yCoords, zCoords, warning, number = getPoints3D(seed, side, radius, number, 0.0, 0.15)

defineMaterial(modelObject, "Matrix", 9.3e-016, 200000.0)
defineMaterial(modelObject, "Inclusion", 3.950e-015, 15000000.0)

part = createMatrix(modelObject, side, False)
edges1, vertices1, face1 = assignGeomSequence(part) # Create references to important sets in our matrix

part2 = createSphereParticle(modelObject, radius, side) # Create Particle part
edges2, vertices2, face2 = assignGeomSequence(part2) # Create references to important sets in particle 

matrixSet, particleSet = create3DInitialSets(part, part2, side)


createSection(modelObject, part, "Matrix", matrixSet) # Create section for matrix material
createSection(modelObject, part2, "Inclusion", particleSet) # Create section for filler material

modelRootAssembly, fullMatrixPart = create3DMatrixInclusions(modelObject, part, part2, number, xCoords, yCoords, zCoords) # Create assembly and return references to assembly sets
assemblyTop, assemblyBottom, assemblyAll = define3DAssemblySets(modelRootAssembly, side)
temp1, temp2 = 328.15, 298.15 # Assign heat temperature to be used in experiment
heatStep3D(modelObject, assemblyBottom, assemblyTop, temp1, temp2) # apply heat BC
elements, nodes, df, meshSeed = makeMesh3D(modelObject, modelRootAssembly, 10, 0.05)  # Draw mesh and return number of nodes and elements
makeElementSet(fullMatrixPart, modelRootAssembly)
odbfileName = modelName
warningString, noElementsWarning = submitJob(modelName, odbfileName)  # Submit job and take note of any warnings
avgHF, TC = getThermalProperties3D(radius, side, temp1, temp2, odbfileName) # Extract relevant information about thermal properties


print(TC)