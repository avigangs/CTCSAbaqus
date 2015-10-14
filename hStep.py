"""
# Step
	heatStep method creates a heat transfer step and assigns boundary conditions
	to the top and bottom faces of the matrix. 
	
	heatStep(temp1, temp2) returns nothing.
		*Input: 
			temp1: The temperature BC applied at bottom face of the matrix.
			temp2: The temperature BC applied at top face of the matrix.
		*Output:
			Nothing.
	
	EXAMPLE:
		heatStep2d(modelObject, aB, aT, 328.15, 298.15) # Temperature in Kelvin
"""

import abaqus
import abaqusConstants as aq


def heatStep2D(modelObject, assemblyBottom, assemblyTop, temp1, temp2):
	modelObject.HeatTransferStep(amplitude=aq.RAMP, name='applyHeat', 
		previous='Initial', response=aq.STEADY_STATE)
	modelObject.TemperatureBC(amplitude=aq.UNSET, createStepName='applyHeat',
		distributionType=aq.UNIFORM, fieldName='', fixed=aq.OFF, magnitude=temp1,
		name='Bottom', region=assemblyBottom)
	modelObject.TemperatureBC(amplitude=aq.UNSET, createStepName='applyHeat', 
		distributionType=aq.UNIFORM, fieldName='', fixed=aq.OFF, magnitude=temp2,
		name='Top', region=assemblyTop)


def heatStep3D(modelObject, assemblyBottom, assemblyTop, temp1, temp2):
	modelObject.HeatTransferStep(amplitude=aq.RAMP, name='Step-1', 
		previous='Initial', response=aq.STEADY_STATE)
	modelObject.TemperatureBC(amplitude=aq.UNSET, createStepName='Step-1',
		distributionType=aq.UNIFORM, fieldName='', fixed=aq.OFF,
		magnitude=temp1, name='BC-1', region=assemblyBottom)
	modelObject.TemperatureBC(amplitude=aq.UNSET, createStepName='Step-1', 
		distributionType=aq.UNIFORM, fieldName='', fixed=aq.OFF, 
		magnitude=temp2, name='BC-2', region=assemblyTop)