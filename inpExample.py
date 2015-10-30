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

import os

## RUN TO DO TC FIRST THEN GO BACK THROUGH FOR RADIUS SINCE THIS WILL BE MUCH MUCH QUICKER

inpRoot = "E:\\inpFiles"
workingDir = 'W:\\Research\\CTCSAbaqus'
os.makedirs(inpRoot)

# Create manifest
manifile = inpRoot+"/manifest.txt"
f = open(manifile, "w")
f.write('ID\tMatrix\tFiller\tPortion\tCalcPortion\tRadius\tNumber\tSide\tDelta\tIntSize\tIntCond\tNodes\tElements\tDevFac\tMeshSeed\tdT\n')
f.close()

# Get material list
materials = getMaterialList() # Load in material Data

for key1, val in materials.iteritems():
	#Matrix levelF
	os.makedirs(inpRoot+"/"+str(key1))
	fillers = materials[key1]['fillers']
	for key2, val2 in fillers.iteritems():
		#Filler level
		os.makedirs(inpRoot+"/"+str(key1)+"/"+str(key2))
		portio1 = 'phr'
		portio2 = 'volPortion'
		if portio1 in materials[key1]['fillers'][key2].keys():
			portions = materials[key1]['fillers'][key2][portio1]
		elif portio2 in materials[key1]['fillers'][key2].keys():
			portions = materials[key1]['fillers'][key2][portio2]
		else:
			break
		for val3 in portions:
			# Portion level
			os.makedirs(inpRoot+"/"+str(key1)+"/"+str(key2)+"/"+str(val3))
			params = ["radius", "tc"]
			for val4 in params:
				# Parameter level
				os.makedirs(inpRoot+"/"+str(key1)+"/"+str(key2)+"/"+str(val3)+"/"+str(val4))
				
				
				# make model
				modelObject, modelName = createModel(2)

				# define materials
				side, radius, portions, dP, dM, cP, cM = defExperiment(modelObject, key1, key2)
				phr = val3 ###
				# get coordinates, interface Max, random interface size, etc.
				radius, number = invPHRAlternate3D(phr, dP, radius, dM, side)
				delta = 0.15
				intPortionLimit = getInterfacePortionLimit(side, radius, number, delta)
				interfacePortion = numpy.random.sample(1) * (intPortionLimit-0.15) + 0.15 # random 0.15 to limit inclusive
				interfacePortion = round(interfacePortion[0], 3)
				xVals, yVals, zVals = getPoints3dDeterministic(side, radius, number)

				interfaceConductivity= numpy.random.sample(1) * (cP-cM) + cM # Between cM and cP
				interfaceConductivity = int(interfaceConductivity[0])
				# Define interface materials
				defineMaterial(modelObject, "Interface", dM, interfaceConductivity)

				# Check PHR values
				calcPHR = round(calculatePHR3D(number, dP, radius, dM, side))

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
				elements, nodes, df, meshSeed = makeMesh3D(modelObject, modelRootAssembly)  # Draw mesh and return number of nodes and elements
				makeElementSet(fullMatrixPart, modelRootAssembly)

				## define range for interface conductivity # Either constant or varying depending on other constants
				for i in range(3):
					interfaceConductivity= numpy.random.sample(1) * (cP-cM) + cM # Between cM and cP
					interfaceConductivity = int(interfaceConductivity[0])
					# Define interface materials
					defineMaterial(modelObject, "Interface", dM, interfaceConductivity) 
					
					fileName = key1 + key2 + str(i+1)
					jobFi = createJob(modelName, fileName)
					afile = open(manifile, "a")
					afile.write(str(i+1)+"\t"+key1+"\t"+key2+"\t"+str(phr)+"\t"+str(calcPHR)+"\t"+str(radius)+"\t"+str(side)+"\t"+str(delta)+"\t"+str(interfacePortion)+"\t"+str(interfaceConductivity)+"\t"+str(nodes)+"\t"+str(elements)+"\t"+str(df)+"\t"+str(meshSeed)+"\t"+str(temp1-temp2)+"\n")
					afile.close()
					os.chdir(inpRoot+"/"+str(key1)+"/"+str(key2)+"/"+str(val3)+"/"+str(val4))
					generateINP(fileName)
					os.chdir(workingDir)
					del mdb.jobs[fileName]

#odbfileName = modelName
#warningString, noElementsWarning = submitJob(modelName, odbfileName)  # Submit job and take note of any warnings
#avgHF, TC = getThermalProperties3D(radius, side, temp1, temp2, odbfileName) # Extract relevant information about thermal properties

#print(dataString(matrix, fillers[1], portions[3], radius, number, side, interfacePortion, delta, calcPHR, interfaceConductivity, seed, nodes, elements, df, meshSeed, avgHF, temp1, temp2, TC, warningString, warningPoints, noElementsWarning)) # Write the data to file
