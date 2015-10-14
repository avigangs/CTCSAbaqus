""""
# Part
	This contains all the helper methods to create the parts needed to run the 
	2D or 3D thermal experiments. 
	
	createMatrix(modelObject, side, twoD) returns part.
		* Input: 
			modelObject: A reference to the model object database.
			side: Numeric value of the side length of the square matrix.
			twoD: Boolean value to determine whether matrix is 2D or 3D.
		* Output: 
			part : a reference to the part object.
		
	
	The assignGeomSequence method is used as a helper method since "clicking"
	edges, vertices, and faces is difficult without the help of a GUI. It 
	returns references to each of the important geometries which makes creating
	sets or assigning sections much easier to program.
	
	assignGeomSequence(part) returns edges, vertices, and face.
		* Input:
			part: Reference to part object
		* Output: 
			edges, vertices, face : References to the relevant geometries of the
				input part object.
			
	The createCircleInclusion method draws the appropriate number of circles 
	(number = len(xVals) = len(yVals)) inside the matrix. These inclusions will
	be assigned to the filler material different than the matrix to simulate a
	composite. (2D method) 
	
	createCircleInclusion(modelObject, radius, number, xVals, yVals) returns sets.
		* Input:
			radius: Numeric value of the radius for each particle inclusion
			number: Integer value of the number of circles drawn
			xVals: Array of x coordinates each centre of each circle.
			yVals: Array of y coordinates each centre of each circle.
		* Output:
			create2DSets(part, edges1, face1): Returns the method call that
				returns the important sets for the matrix. 
	
	create2DSets is used to create and return sets related to the matrix, particle,
	and the combination.
	
	create2DSets(part, edges1, face1) return matrixSet, fillerSet, allSet.
		* Input:
			part: reference to the part object.
			edges1: reference to GeomSequence edge of the part.
			face1: reference to the GeomSequence face of the part.
		* Output:
			matrixSet: Reference to the matrix set sans particle fillers.
			fillerSet: Reference to the set of all fillers/particles.
			allSet: Reference to the entire object, fillers + matrix.
	
	The createSphereParticle method creates the sphere particle which can serve
	for making the filler and the interface.
	
	createSphereParticle(modelObject, particleRadius, matrixSide, name1="Particle"
	returns part.
		* Input:
			modelObject: Reference to the model object database.
			particleRadius: The particle radius
			matrixSide: The side length of the matrix
			name1: Defaults to "particle", but name of the part.
		* Output:
			part: Reference to the created particle part.
	
	The create3DInitialSets method creates the sets for the 3D simulation. There
	is an option to add the interface, which returns an extra set reference.
	
	create3DInitialSets(matrixPart, particlePart, matrixSide, interfacePart)
	returns either matrixSet, particleSet, interfaceSet OR matrixSet, particleSet
		*Input:
			matrixPart: Reference to the matrix part object.
			particlePart: Reference to the particle part object.
			matrixSide: Numeric side length of matrix.
			interfacePart: Reference to the interface part object.
		*Output: (2 OPTIONS)
			If interfacePart exists:
			*matrixSet = Reference to matrix set object.
			*particleSet = Reference to particle set Object.
			*interfaceSet = Reference to interface set Object.
			If interfacePart == None:
			*No interfaceSet.
	
	Examples:
		See Example scripts.
"""

import abaqus
import abaqusConstants as aq

# NOTE: The three last methods in this file could all be "private" to 
# createMatrix since they would never be called on their own. This needs to be 
# addressed.

# This method draws the square with side length "side" that will serve as the 
# 2D Matrix. The part object is returned for reference.
def createMatrix(modelObject, side, twoD=True):
	sketch = modelObject.ConstrainedSketch(name='__profile__', sheetSize=500.0)
	sketch.setPrimaryObject(option=aq.STANDALONE) 
	# Draw a square with sides of length side.
	sketch.rectangle(point1=(0.0,0.0), point2=(side,side)) 
	# Boolean: Draws either 2D matrix for True or 3D Matrix for False
	if twoD:
		modelObject.Part(name='SolidMatrix', dimensionality=aq.TWO_D_PLANAR, 
			type=aq.DEFORMABLE_BODY) # Abaqus command to create the part.
		part = modelObject.parts['SolidMatrix'] # Reference variable to part.
		part.BaseShell(sketch=sketch)
	else:
		modelObject.Part(name='SolidMatrix', dimensionality=aq.THREE_D, 
			type=aq.DEFORMABLE_BODY)
		part = modelObject.parts['SolidMatrix']
		part.BaseSolidExtrude(depth=side, sketch=sketch)
	
	sketch.unsetPrimaryObject() 
	del modelObject.sketches['__profile__'] 
	return part

# Edit to return name for use in Assembly
def createSphereParticle(modelObject, particleRadius, matrixSide, name1="Particle"):
	# *Create sphere to act as filler
	sketch = modelObject.ConstrainedSketch(name='__profile__', sheetSize=500.0)
	# side length matrix to negative side length matrix 
	sketch.ConstructionLine(point1=(0.0,-matrixSide), point2=(0.0,matrixSide))
	sketch.FixedConstraint(entity=sketch.geometry.findAt((0.0,0.0),))
	# Draw arc , negative radius to radius
	sketch.ArcByCenterEnds(center=(0.0,0.0), direction=aq.CLOCKWISE, 
		point1=(0.0, particleRadius), point2=(0.0,-particleRadius)) 
	 # Close arc , same as above.
	sketch.Line(point1=(0.0, particleRadius), point2=(0.0, -particleRadius))
	# negative radius add radius * 0.1
	sketch.VerticalConstraint(addUndoState=False, 
		entity=sketch.geometry.findAt((0.0,-particleRadius+particleRadius*0.1),))
	# Finish sphere
	modelObject.Part(dimensionality=aq.THREE_D, name=name1, 
		type=aq.DEFORMABLE_BODY)
	modelObject.parts[name1].BaseSolidRevolve(angle=360.0, 
		flipRevolveDirection=aq.OFF, sketch=sketch)
	del sketch
	part = modelObject.parts[name1]
	return part

# This method creates references to the GeomSequence objects derived from the 
# argument "part". In the 2D Model we only have one part so this method is used
# once, but 3D Model needs multiple GeomSequences.
def assignGeomSequence(part):
	edges = part.edges
	vertices = part.vertices
	face = part.faces
	return edges, vertices, face


# NOTE: The following method does too much!

# This method creates the partitions and circular inclusions which finishes our
# simple 2D Model. It also makes the sets associated to the matrix, the 
# inclusions, and then the entire model.  
def createCircleInclusion(modelObject, part, radius, number, xVals, yVals):
	#edges1, vertices1, face1 = assignGeomSequence(part) NEEDED???
	t = part.MakeSketchTransform(sketchPlane=face1[0], sketchPlaneSide=aq.SIDE1,
		origin=(0,0,0))
	sketch = modelObject.ConstrainedSketch(name='__profile__', sheetSize=500, 
		gridSpacing=10, transform=t)
	geometry = sketch.geometry
	sketch.setPrimaryObject(option=aq.SUPERIMPOSE)
	part.projectReferencesOntoSketch(sketch=sketch, filter=aq.COPLANAR_EDGES)
	for cir in range(0, number): # Draw 'number' circles with radius 'radius'
		sketch.CircleByCenterPerimeter(center=(xVals[cir],yVals[cir]), 
			point1=(xVals[cir], yVals[cir] + radius)) # command to draw circle
		
	pickedFaces = face1.getSequenceFromMask(mask=('[#1 ]', ), ) # Select all
	part.PartitionFaceBySketch(faces=pickedFaces, sketch=sketch)
	sketch.unsetPrimaryObject()
	del modelObject.sketches['__profile__']
	return create2DSets(part, edges1, face1) # Return references to the sets. 

# Create sets and regions for top and bottom values and for the filler and matrix
# These are referenced in various stages like assembly or mesh. 
def create2DSets(part, edges1, face1):
	part.Set(name='Top', edges=edges1.findAt(((side/2.0,side,0),))) 
	part.Set(name='Bottom', edges=edges1.findAt(((side/2.0,0,0),)))
	# Select the bottom corner, selecting the entire matrix
	part.Set(faces=face1.findAt(((1,1, 0.0), )), name='Matrix') 
	for zz in range(number): # Creates a set for each circle
		part.Set(name='filler'+str(zz), faces=face1.findAt(((xVals[zz], yVals[zz], 0),)))
	
	#Creates an array of strings like filler0, filler1, filler2, etc.
	fillerlist = [part.sets['filler'+str(yy)] for yy in range(number)] 
	# Merges all the individual filler sets into one.
	part.SetByBoolean(name='Fillers', sets=fillerlist) 
	# Merge an "All" set 
	part.SetByBoolean(name='All', sets=[part.sets['Fillers'], part.sets['Matrix']]) 
	# Create references to the sets
	matrixSet = part.sets['Matrix']
	fillerSet = part.sets['Fillers']
	allSet = part.sets['All']
	return matrixSet, fillerSet, allSet

def create3DInitialSets(matrixPart, particlePart, matrixSide, interfacePart=None):
	matrixPart.Set(cells=matrixPart.cells.findAt(((matrixSide,matrixSide,matrixSide),)), 
		name='allMatrix')
	particlePart.Set(cells=particlePart.cells.findAt(particlePart.cells[0].pointOn), 
		name='particleAll')
	matrixSet = matrixPart.sets['allMatrix']
	particleSet = particlePart.sets['particleAll']
	if interfacePart is not None:
		interfacePart.Set(cells=interfacePart.cells.findAt(interfacePart.cells[0].pointOn), 
			name='interfaceAll')
		interfaceSet = interfacePart.sets['interfaceAll']
		return matrixSet, particleSet, interfaceSet
	else:
		return matrixSet, particleSet
	