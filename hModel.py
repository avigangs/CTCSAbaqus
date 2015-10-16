"""
# Model 
	This method creates a new model database in Abaqus, then returns both the
	model object and the model name for easy reference. The input argument "num"
	is simply a convention I have to name the dozens of models being created
	iteratively. If you wish to view multiple models then change num on each
	iteration, otherwise leave num fixed to overwrite each model. 
	
	Note: There are optional parameters for the mdb.Model(...) command if 
	additional constraints are required in your model.
	
	createModel(num) returns modelObject, modelName
		* Input: 
			num: Integer that sets a number for each model, ex: Model-1,
				Model-2, Model-3...
		* Output: 
			modelObject : The mdb model object containing all the methods
				required to build the model for simulation. 
			modelName : String containing the name of the model. "Model-1", 
				"Model-2", etc.
			
	
	EXAMPLE: 
	# Creates model database named "Model-1" accessed by referencing firstModel
		firstModel, modelOneName = createModel(1) 
	# Creates a new material associated with this model.
		firstModel.Material(name="Steel")  
"""

from abaqus import mdb
import abaqusConstants as aq


def createModel(num):
	modelName = 'Model-'+ str(num) 
	# Abaqus command to create a new model database.
	mdb.Model(name=modelName, modelType=aq.STANDARD_EXPLICIT)
	# Create reference variable for the model object.
	modelObject = mdb.models[modelName] 
	return modelObject, modelName


def dir1():
	return dir()
