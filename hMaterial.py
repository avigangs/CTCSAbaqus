"""
# Materials
	
	defineMaterial creates a new material associated with the part. 
	This method could be expanded to take values for more complex simulations.
	
	defineMaterial(strName, density, conductivity) returns nothing.
		*Input:
			strName: String for the name of the material. "Steel".
			density: Numeric  value for the density of the material.
			conductivity: Numeric values for the conductivity of the material.
		*Output:
			None.
	
	EXAMPLE:
		defineMaterial("ESBR", 930, 0.2) # SI units
		defineMaterial("Alumina", 3950, 10) # SI units
		
	getMaterialList method returns experimental data for thermal conductivity of
	composites.
	
	materials = getMaterialList()
	
	The defExperiment method is used to define an experiment pair at the same
	time, instead of calling defineMaterial. 
	
	defExperiment(matrixMaterial, fillerMaterial)
		*Input: 
			matrixMaterial : String name of the matrix
			fillerMaterial : String name of particle
		*Output:
			side : side length of the matrix used
			radius : length of the particle radius used
			portions : PHR/volume portions associated with the experiment
"""
from abaqus import mdb
import abaqusConstants as aq

# Consider something that limits particle numbers to ~40ish or 25ish

# Input is the Material name as a string, density as a real number, and 
# conductivity as a real number. 
def defineMaterial(modelObject, strName, density, conductivity):
	modelObject.Material(name=strName)
	modelObject.materials[strName].Density(table=((density, ), ))
	modelObject.materials[strName].Conductivity(table=((conductivity, ), ))

# Is this appropriate to have all the data here? Ideally it would be split up 
# between strictly material and strictly experiment

# Hash including density and conductivity for experimental data along with side
# and radius.

# Note the units are in kg/micrometers. SI was giving issues during the mesh 
# seeding process.
def getMaterialList(): 
	materials = { 
		'ESBR' : { 'densityM' : 9.3e-016, 'conducM' : 200000.0, 'fillers' : { #TCNanoFillers
			'Alumina' : { 'densityF' : 3.950e-015, 'conducF' : 15000000.0, 'side' : 520, 'radius' : 37.5,
				'phr' : [10, 20, 40, 80, 100]}, 
			'ZincOxide' : { 'densityF' : 5.610e-015, 'conducF' : 25000000.0, 'side' : 176, 'radius' : 22.5,
				'phr' : [5, 10, 20, 40, 80, 100]}}}, 
		'EpoxyResin' : { 'densityM' : 1.3e-015, 'conducM' : 170000, 'fillers' : { #TCPolymericCompositesReview
			'SiliconOxide' : { 'densityF' : 2.65e-015, 'conducF' : 1400000.0, 'side' : 200, 'radius' : 20,
				'volPortion' : [0.45]}, 
			'AluminumNitrate' : { 'densityF' : 1.72e-015, 'conducF' : 2.5e+08, 'side' : 25, 'radius' : 1,
				'volPortion' : [0.007]},
			'MagnesiumOxide' : { 'densityF' : 3.58e-015, 'conducF' : 47500000.0, 'side' : 25, 'radius' : 1,
				'volPortion' : [0.007]}, 
			'Alumina' : { 'densityF' : 3.950e-015, 'conducF' : 25000000.0, 'side' : 50, 'radius' : 4,
				'volPortion' : [0.312]}}},
		'Polystyrene' : { 'densityM' : 1.05e-015, 'conducM' : 150000, 'fillers' : { # TCPolystryreneComposite
			'AlNLarge' : { 'densityF' : 1.72e-015, 'conducF' : 1.6e+08, 'side' : 2500, 'radius' : 200,
				'volPortion' : [0.02, 0.04, 0.06, 0.08, 0.12, 0.165, 0.205, 0.25]},
			'AlNSmall' : { 'densityF' : 1.72e-015, 'conducF' : 1.6e+08, 'side' : 300, 'radius' : 15,
				'volPortion' : [0.02, 0.04, 0.06, 0.08, 0.12, 0.165, 0.205, 0.25]}}}, 
		'SiliconRubber' : { 'densityM' : 1.5e-018, 'conducM' : 560000.0, 'fillers' : { #TCZincOxide
			'ZnOLarge' : { 'densityF' : 5.610e-015, 'conducF' : 60000000.0, 'side' : 1100, 'radius' : 77,
				'volPortion' : [0.083, 0.16, 0.185, 0.241, 0.266, 0.312]}, 
			'ZnOMedium' : { 'densityF' : 5.610e-015, 'conducF' : 60000000.0, 'side' : 600, 'radius' : 38,
				'volPortion' : [0.083, 0.16, 0.185, 0.241, 0.266, 0.312]},
			'ZnOSmall' : { 'densityF' : 5.610e-015, 'conducF' : 60000000.0, 'side' : 25, 'radius' : 1.5},
				'volPortion' : [0.083, 0.16, 0.185, 0.241, 0.266, 0.312]}}}
	
	return materials

# Helper method for assigning material attributes to model db material along with returning values for required side ,radius, and portions
# defThermalExp
def defExperiment(modelObject, matrixMaterial, fillerMaterial):
	mList = getMaterialList()
	dM, cM = mList[matrixMaterial]['densityM'], mList[matrixMaterial]['conducM']
	fillerReference = mList[matrixMaterial]['fillers'][fillerMaterial]
	dP, cP = fillerReference['densityF'], fillerReference['conducF']
	defineMaterial(modelObject, matrixMaterial, dM, cM)
	defineMaterial(modelObject, fillerMaterial, dP, cP)
	side = fillerReference['side']
	radius = fillerReference['radius']
	if fillerReference.has_key('phr'):
		portions = fillerReference['phr']
	else:
		portions = fillerReference['volPortion']
	
	return side, radius, portions, dP, dM, cP, cM