"""
# Property
	This method creates sections and assigns appropriate materials to each
	section.
	
	createSection(modelObject, part, strName, setName) returns nothing.
		*Input: 
			modelObject: reference to mdb.
			part : reference to part object.
			strName: String value for the name of the section.
			setName: A reference to the set to be assigned. 
		*Output:
			None.
	
	EXAMPLE:
		createSection(modelObject, part1, "ESBR", matrixSet)
		createSection(modelObject, part2, "Alumina", fillerSet)
		# assigns the ESBR material to the matrix and the Alumina material 
		# to the particles.
"""

import abaqus
import abaqusConstants as aq

def createSection(modelObject, part, strName, setName):
	modelObject.HomogeneousSolidSection(material=strName, name=strName, 
		thickness=None)
	part.SectionAssignment(offset=0.0, offsetField='', offsetType=aq.MIDDLE_SURFACE, 
		region=setName, sectionName=strName, thicknessAssignment=aq.FROM_SECTION)
