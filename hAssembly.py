"""
# Assembly
	All the required methods for assembling the parts to run the simulations.
	
	makeAssembly2D(modelObject, part) returns assemblyTop, assemblyBottom.
		*Input:
			modelObject: reference to model object database.
			part: reference to part object.
		*Output:
			assemblyTop: A reference to the assembly set of the top face 
			assemblyBottom: A reference to the assembly set of the bottom face.
	
	The create3DMatrix inclusions can work for simulations involving interface
	by including the interface part.
	
	create3DMatrixInclusions(modelObject, matPart, parPart, number, xV, yV, zV, intPart)
	returns modelRootAssembly.
		*Input:
			modelObject: reference to model object database.
			matPart: reference to matrix part
			parPart: reference to the particle part
			number: number of particles
			xV: array of x coordinates
			yV: array of y coordinates
			zV: array of z coordinates
			intPart: reference to the interface part.
		*Output:
			modelRootAssembly: reference to the assembly object.

	define3DAssemblySets(modelRootAssembly, matrixSide) returns assemblyTop, 
	assemblyBottom, assemblyAll
		*Input:
			modelRootAssembly: reference to assembly object.
			matrixSide: side length of the matrix
		*Output:
			assemblyTop: reference to assembly set for top
			assemblyBot: reference to assembly set for bottom
			assemblyAll: reference to assembly set for All
"""

import abaqus
import abaqusConstants as aq

def makeAssembly2D(modelObject, part):
	modelObject.rootAssembly.DatumCsysByDefault(aq.CARTESIAN)
	modelObject.rootAssembly.Instance(dependent=ON, name='PART1', part=part)
	# Create a reference to the assembly sets
	assemblyTop = modelObject.rootAssembly.instances['PART1'].sets['Top']
	assemblyBottom = modelObject.rootAssembly.instances['PART1'].sets['Bottom']
	return assemblyTop, assemblyBottom

def create3DMatrixInclusions(modelObject, matPart, parPart, number, xVals,
	yVals, zVals, intPart=None):
	modelRootAssembly = modelObject.rootAssembly
	if intPart is None:
		modelRootAssembly.Instance(dependent=aq.OFF, name='SolidMatrix-1',
			part=matPart)
		for zz in range(number): # Create each particle
			modelRootAssembly.Instance(dependent=aq.OFF, 
				name='Particle-'+str(zz+1), part=parPart)

		for yy in range(number): # Translate each particle
			modelRootAssembly.translate(instanceList=('Particle-'+str(yy+1), ),
				vector=(xVals[yy], yVals[yy], zVals[yy]))
		
		# make tuple of particle instances
		tupleInstances = tuple([(modelRootAssembly.instances['Particle-'+str(nn+1)])
			for nn in range(number)]) 

		modelRootAssembly.InstanceFromBooleanCut(cuttingInstances=(tupleInstances),
			instanceToBeCut=modelRootAssembly.instances['SolidMatrix-1'],
			name='matrixEmpty', originalInstances=aq.SUPPRESS)
		for xx in range(number): # Resume particles
			modelRootAssembly.features['Particle-'+str(xx+1)].resume()

		allInstances = tupleInstances + (modelRootAssembly.instances['matrixEmpty-1'],)
		modelRootAssembly.InstanceFromBooleanMerge(domain=aq.GEOMETRY,
			instances=(allInstances), keepIntersections=aq.ON, name='matrixFull',
			originalInstances=aq.DELETE) # make the final assembly
		modelRootAssembly.makeIndependent(instances=(modelRootAssembly.instances['matrixFull-1'], ))
	else: 
		for zz in range(number): # Create each particle
			modelRootAssembly.Instance(dependent=aq.ON, name='Particle-'+str(zz+1),
				part=parPart)

		for zz in range(number): # Create each interface
			modelRootAssembly.Instance(dependent=aq.ON, name='Interface-'+str(zz+1),
				part=intPart)

		for yy in range(number): # Translate each interface + particle
			modelRootAssembly.translate(instanceList=('Particle-'+str(yy+1), 
				'Interface-'+str(yy+1)), vector=(xVals[yy], yVals[yy], zVals[yy]))
		

		for xx in range(number): # Cut each particle from each interface
			modelRootAssembly.InstanceFromBooleanCut(cuttingInstances=(modelRootAssembly.instances['Particle-'+str(xx+1)], ),
				instanceToBeCut=modelRootAssembly.instances['Interface-'+str(xx+1)],
				name='InterfaceParticle-'+str(xx+1), originalInstances=aq.SUPPRESS)
		
		# Resume each particle
		for xx in range(number):
			modelRootAssembly.features['Particle-'+str(xx+1)].resume()
		
		# Merge each particle and interface set
		for xx in range(number):
			modelRootAssembly.InstanceFromBooleanMerge(domain=aq.GEOMETRY,
				instances=(modelRootAssembly.instances['Particle-'+str(xx+1)],
				modelRootAssembly.instances['InterfaceParticle-'+str(xx+1)+'-1']),
				keepIntersections=aq.ON, name='MergedParticleInterface-'+str(xx+1),
				originalInstances=aq.DELETE)
		
		# Enable Matrix part
		modelRootAssembly.Instance(dependent=aq.ON, name='SolidMatrix-1', 
			part=matPart)
		
		# Cut each merged particle from the matrix
		tupleMergedParticles = tuple([(modelRootAssembly.instances['MergedParticleInterface-'+str(nn+1)+'-1'])
			for nn in range(number)]) 
		modelRootAssembly.InstanceFromBooleanCut(cuttingInstances=(tupleMergedParticles),
			instanceToBeCut=modelRootAssembly.instances['SolidMatrix-1'],
			name='matrixEmpty', originalInstances=aq.SUPPRESS)
		
		# Resume each cut merged Particle
		for xx in range(number):
			modelRootAssembly.features['MergedParticleInterface-'+str(xx+1)+'-1'].resume()
		
		# Merge each merged particle with the empty matrix
		allInstances = tupleMergedParticles + (modelRootAssembly.instances['matrixEmpty-1'],)
		modelRootAssembly.InstanceFromBooleanMerge(domain=aq.GEOMETRY,
			instances=(allInstances), keepIntersections=aq.ON, name='matrixFull',
			originalInstances=aq.SUPPRESS) # make the final assembly
		modelRootAssembly.makeIndependent(instances=(modelRootAssembly.instances['matrixFull-1'], ))
	return modelRootAssembly


def define3DAssemblySets(modelRootAssembly, matrixSide):
	bottomFace = modelRootAssembly.instances['matrixFull-1'].faces.pointsOn[3]
	topFace = modelRootAssembly.instances['matrixFull-1'].faces.pointsOn[1]
	matrixInstance = modelRootAssembly.instances['matrixFull-1']
	modelRootAssembly.Set(faces=matrixInstance.faces.findAt(topFace), name='assemblyTop')
	modelRootAssembly.Set(faces=matrixInstance.faces.findAt(bottomFace), name='assemblyBot')
	modelRootAssembly.Set(cells=matrixInstance.cells, name='assemblyAll')
	assemblyTop = modelRootAssembly.sets['assemblyTop']
	assemblyBottom = modelRootAssembly.sets['assemblyBot']
	assemblyAll = modelRootAssembly.sets['assemblyAll']
	return assemblyTop, assemblyBottom, assemblyAll