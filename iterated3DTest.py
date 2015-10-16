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
trialsPer = 10 # Number of times to run each experiment
interfaceSize = 0.0
defDelta = 0.15

materials = getMaterialList() # Load in material Data
matrix = "ESBR" # Choose the first experiment from TCNanoFillers
fillers = ["Alumina", "ZincOxide"] # Two fillers associated with first experiment

fileName = matrix+fillers[0] + fillers[1] # Name file after matrix, filler materials
f = open(fileName, 'w')
f.write('Matrix\tFiller\tPortion\tRadius\tNumber\tSide\tIntSize\tDelta\tCalcPor\tIntCond\tSeed\tNodes\tElements\tDevFac\tMeshSeed\tq\tdT\tk\tNoElmWarn\tWarn\n')
exit
for i in range(len(materials[matrix]['fillers'])): # "For each filler material"
	for j in range(len(materials[matrix]['fillers'][fillers[i]]['phr'])): # "For each PHR/volume portion specified"
		for k in range(trialsPer): # "Run trialsPer times for each material/filler/PHR combination"
			modelObject, modelName = createModel(2) # Create model database "Model-2"
			side, radius, portions, dP, dM, cP, cM = defExperiment(modelObject, matrix, fillers[i]) # Define material attributes for specified matrix, fillers
			seed = numpy.random.randint(1000000) # Random seed for coordinate generation
			radius, number = invPHR(portions[j], dP, radius, dM, side, False) # Returns specific radius size and number of inclusions for closest PHR value.
			xVals, yVals, zVals, warningPoints, number = getPoints3D(seed, side, radius, number, interfacePortions[l], defDelta) # returns coordinates for inclusion locations. 
			calcPHR = calculatePHR3D(number, dP, radius, dM, side)
			part = createMatrix(modelObject, side, False) # Create the matrix
			edges1, vertices1, face1 = assignGeomSequence(part) # Create references to important sets in our matrix
			part2 = createSphereParticle(modelObject, radius, side) # Create Particle part
			edges2, vertices2, face2 = assignGeomSequence(part2) # Create references to important sets in particle 
			matrixSet, particleSet = create3DInitialSets(part, part2, side)
			createSection(modelObject, part, matrix, matrixSet) # Create section for matrix material
			createSection(modelObject, part2, fillers[i], particleSet) # Create section for filler material
			
			modelRootAssembly = create3DMatrixInclusions(modelObject, part, part2, number, xVals, yVals, zVals) # Create assembly and return references to assembly sets
			assemblyTop, assemblyBottom, assemblyAll = define3DAssemblySets(modelRootAssembly, side)
			temp1, temp2 = 328.15, 298.15 # Assign heat temperature to be used in experiment
			heatStep3D(modelObject, assemblyBottom, assemblyTop, temp1, temp2) # apply heat BC
			elements, nodes, df, meshSeed = makeMesh3D() # Draw mesh and return number of nodes and elements
			makeElementSet(modelRootAssembly)
			warningString, noElementsWarning = submitJob() # Submit job and take note of any warnings
			avgHF, TC = getThermalProperties3D(radius, side) # Extract relevant information about thermal properties
			f.write(dataString(matrix, fillers[i], portions[j], radius, number, side, interfaceSize, defDelta, calcPHR, "nil", seed, nodes, elements, df, meshSeed, avgHF, temp1, temp2, TC, warningString, warningPoints, noElementsWarning)) # Write the data to file
			del mdb.jobs["Job-1"]
			del mdb.models[modelName]
		
	

f.close()