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
				'phr' : [10, 20, 40, 80, 100], 'meshSeed' : 10, 'df' : 0.0375, 'delta' : 0.15, 'minInt' : 0.15}, 
			'ZincOxide' : { 'densityF' : 5.610e-015, 'conducF' : 25000000.0, 'side' : 176, 'radius' : 22.5,
				'phr' : [5, 10, 20, 40, 80, 100], 'meshSeed' : 3.2, 'df' : 0.0125, 'delta' : 0.17, 'minInt' : 0.17}}}, 
		'EpoxyResin' : { 'densityM' : 1.3e-015, 'conducM' : 170000, 'fillers' : { #TCPolymericCompositesReview
			'SiliconOxide' : { 'densityF' : 2.65e-015, 'conducF' : 1400000.0, 'side' : 200, 'radius' : 20,
				'volPortion' : [0.43], 'meshSeed' : 4.5, 'df' : 0.05, 'delta' : 0.03, 'minInt' : 0.03}, 
			'AluminumNitrate' : { 'densityF' : 1.72e-015, 'conducF' : 2.5e+08, 'side' : 25, 'radius' : 1.5,
				'volPortion' : [0.007], 'meshSeed' : 0.5, 'df' : 0.0225, 'delta' : 0.20, 'minInt' : 0.15}, 
			'MagnesiumOxide' : { 'densityF' : 3.58e-015, 'conducF' : 47500000.0, 'side' : 25, 'radius' : 1.5,
				'volPortion' : [0.007], 'meshSeed' : 0.4, 'df' : 0.0225, 'delta' : 0.20, 'minInt' : 0.15}, 
			'Alumina' : { 'densityF' : 3.950e-015, 'conducF' : 25000000.0, 'side' : 50, 'radius' : 4,
				'volPortion' : [0.312], 'meshSeed' : 0.85, 'df' : 0.035, 'delta' : 0.07, 'minInt' : 0.10}}}, 
		'Polystyrene' : { 'densityM' : 1.05e-015, 'conducM' : 150000, 'fillers' : { # TCPolystryreneComposite
			'AlNLarge' : { 'densityF' : 1.72e-015, 'conducF' : 1.6e+08, 'side' : 2000, 'radius' : 150,
				'volPortion' : [0.02, 0.04, 0.06, 0.08, 0.12, 0.165, 0.205, 0.25], 'meshSeed' : 35, 'df' : 0.032, 'delta' : 0.08, 'minInt' : 0.10},
			'AlNSmall' : { 'densityF' : 1.72e-015, 'conducF' : 1.6e+08, 'side' : 200, 'radius' : 15,
				'volPortion' : [0.02, 0.04, 0.06, 0.08, 0.12, 0.165, 0.205, 0.25], 'meshSeed' : 9, 'df' : 0.0225, 'delta' : 0.08, 'minInt' : 0.10}}}, 
		'SiliconRubber' : { 'densityM' : 1.5e-018, 'conducM' : 560000.0, 'fillers' : { #TCZincOxide
			'ZnOLarge' : { 'densityF' : 5.610e-015, 'conducF' : 60000000.0, 'side' : 800, 'radius' : 77,
				'volPortion' : [0.083, 0.16, 0.185, 0.241, 0.266], 'meshSeed' : 19, 'df' : 0.0255, 'delta' : 0.08, 'minInt' : 0.08}, 
			'ZnOMedium' : { 'densityF' : 5.610e-015, 'conducF' : 60000000.0, 'side' : 480, 'radius' : 32,
				'volPortion' : [0.083, 0.16, 0.185, 0.241, 0.266], 'meshSeed' : 11, 'df' : 0.04, 'delta' : 0.10, 'minInt' : 0.10}, 
			'ZnOSmall' : { 'densityF' : 5.610e-015, 'conducF' : 60000000.0, 'side' : 25, 'radius' : 1.75,
				'volPortion' : [0.083, 0.16, 0.185, 0.241, 0.266], 'meshSeed' : 0.50, 'df' : 0.0250, 'delta' : 0.08, 'minInt' : 0.08}}}} 
	
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


def makeFileStructure():
	topLevel = "inpFiles"
	os.makedirs(topLevel)
	for key, val in z.iteritems():
		os.makedirs(topLevel+"/"+str(key))
		fillersx = z[key]['fillers']
		for key2, val2 in fillersx.iteritems():
			os.makedirs(topLevel+"/"+str(key)+"/"+str(key2))
			portio1 = 'phr'
			portio2 = 'volPortion'
			if portio1 in z[key]['fillers'][key2].keys():
				portionsy = z[key]['fillers'][key2][portio1]
			elif portio2 in z[key]['fillers'][key2].keys():
				portionsy = z[key]['fillers'][key2][portio2]
			else:
				break
			
			for val3 in portionsy:
				os.makedirs(topLevel+"/"+str(key)+"/"+str(key2)+"/"+str(val3))
				params = ["radius", "tc"]
				for val4 in params:
					os.makedirs(topLevel+"/"+str(key)+"/"+str(key2)+"/"+str(val3)+"/"+str(val4))


def checkExist():
	if not os.path.exists("inpFiles"):
		inpRoot = "inpFiles"
		os.makedirs(inpRoot)
	else:
		inpRoot = "inpFiles"+str(141)
		os.makedirs("inpFiles"+str(141))
