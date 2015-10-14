# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)  #create outer cube
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(100.0, 100.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=100.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0) #create inner cube
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(40.0, 40.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-2'].BaseSolidExtrude(depth=40.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].Material(name='ESBR')        #create materials and sections
mdb.models['Model-1'].materials['ESBR'].Density(table=((9.3e-16, ), ))
mdb.models['Model-1'].materials['ESBR'].Conductivity(table=((20000.0, ), ))
mdb.models['Model-1'].Material(name='alumina')
mdb.models['Model-1'].materials['alumina'].Density(table=((3.95e-15, ), ))
mdb.models['Model-1'].materials['alumina'].Conductivity(table=((10000000.0, ), 
    ))
mdb.models['Model-1'].HomogeneousSolidSection(material='ESBR', name='ESBR', 
    thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='alumina', name=
    'alumina', thickness=None)
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0,  #assign sections
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models['Model-1'].parts['Part-1'].cells.findAt(((100.0, 
    66.666667, 66.666667), ), )), sectionName='ESBR', thicknessAssignment=
    FROM_SECTION)
mdb.models['Model-1'].parts['Part-2'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models['Model-1'].parts['Part-2'].cells.findAt(((40.0, 26.666667, 
    26.666667), ), )), sectionName='alumina', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)   #create instances
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-2-1', 
    part=mdb.models['Model-1'].parts['Part-2'])
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-2-1', ),  #translate inner cube to center
    vector=(30.0, 30.0, 30.0))
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanCut(cuttingInstances=( #cut using geometry with the inner cube cutting the outer
    mdb.models['Model-1'].rootAssembly.instances['Part-2-1'], ), 
    instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], 
    name='Part-3', originalInstances=SUPPRESS)
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-2-2',  #create another instance of the inner cube
    part=mdb.models['Model-1'].parts['Part-2'])
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-2-2', ),  #translate it again
    vector=(30.0, 30.0, 30.0))
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,  #merge instances keeping internal boundaries
    instances=(mdb.models['Model-1'].rootAssembly.instances['Part-3-1'], 
	mdb.models['Model-1'].rootAssembly.instances['Part-2-2']), 
	keepIntersections=ON, name='Part-4', originalInstances=SUPPRESS)
mdb.models['Model-1'].HeatTransferStep(amplitude=RAMP, name='Step-1', previous= #create step and assign boundary conditions
    'Initial', response=STEADY_STATE)
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'NT', 'HFL'))
mdb.models['Model-1'].TemperatureBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, magnitude=298.0, name=
    'BC-1', region=Region(
    faces=mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].faces.findAt(
    ((33.333333, 100.0, 66.666667), ), )))
mdb.models['Model-1'].TemperatureBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, magnitude=328.0, name=
    'BC-2', region=Region(
    faces=mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].faces.findAt(
    ((66.666667, 0.0, 66.666667), ), )))
mdb.models['Model-1'].parts['Part-4'].setMeshControls(elemShape=TET, regions= #assign mesh controls and mesh element type
    mdb.models['Model-1'].parts['Part-4'].cells.findAt(((30.0005, 56.666667, 
    56.666667), ), ((100.0, 66.666667, 66.666667), ), ), technique=FREE)
mdb.models['Model-1'].parts['Part-4'].setElementType(elemTypes=(ElemType(
    elemCode=C3D20R, elemLibrary=STANDARD), ElemType(elemCode=C3D15, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D10, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['Part-4'].cells.findAt(((30.0005, 
    56.666667, 56.666667), ), ((100.0, 66.666667, 66.666667), ), ), ))
mdb.models['Model-1'].parts['Part-4'].setElementType(elemTypes=(ElemType(
    elemCode=DC3D20, elemLibrary=STANDARD), ElemType(elemCode=DC3D15, 
    elemLibrary=STANDARD), ElemType(elemCode=DC3D10, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['Part-4'].cells.findAt(((30.0005, 
    56.666667, 56.666667), ), ((100.0, 66.666667, 66.666667), ), ), ))
mdb.models['Model-1'].parts['Part-4'].seedPart(deviationFactor=0.1,  #mesh part
    minSizeFactor=0.1, size=10.0)
mdb.models['Model-1'].parts['Part-4'].generateMesh()
mdb.models['Model-1'].rootAssembly.regenerate()        #create and run job
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, queue=None, scratch='', type=ANALYSIS, userSubroutine='', 
    waitHours=0, waitMinutes=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
mdb.jobs['Job-1']._Message(STARTED, {'phase': BATCHPRE_PHASE, 
    'clientHost': 'MWS1377', 'handle': 0, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(ODB_FILE, {'phase': BATCHPRE_PHASE, 
    'file': 'W:\\threeD\\Job-1.odb', 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(COMPLETED, {'phase': BATCHPRE_PHASE, 
    'message': 'Analysis phase complete', 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STARTED, {'phase': STANDARD_PHASE, 
    'clientHost': 'MWS1377', 'handle': 9732, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STEP, {'phase': STANDARD_PHASE, 'stepId': 1, 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(ODB_FRAME, {'phase': STANDARD_PHASE, 'step': 0, 
    'frame': 0, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STATUS, {'totalTime': 0.0, 'attempts': 0, 
    'timeIncrement': 1.0, 'increment': 0, 'stepTime': 0.0, 'step': 1, 
    'jobName': 'Job-1', 'severe': 0, 'iterations': 0, 'phase': STANDARD_PHASE, 
    'equilibrium': 0})
mdb.jobs['Job-1']._Message(MEMORY_ESTIMATE, {'phase': STANDARD_PHASE, 
    'jobName': 'Job-1', 'memory': 55.6812744140625})
mdb.jobs['Job-1']._Message(ODB_FRAME, {'phase': STANDARD_PHASE, 'step': 0, 
    'frame': 1, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STATUS, {'totalTime': 1.0, 'attempts': 1, 
    'timeIncrement': 1.0, 'increment': 1, 'stepTime': 1.0, 'step': 1, 
    'jobName': 'Job-1', 'severe': 0, 'iterations': 1, 'phase': STANDARD_PHASE, 
    'equilibrium': 1})
mdb.jobs['Job-1']._Message(END_STEP, {'phase': STANDARD_PHASE, 'stepId': 1, 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(COMPLETED, {'phase': STANDARD_PHASE, 
    'message': 'Analysis phase complete', 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(JOB_COMPLETED, {'time': 'Fri Jul 10 15:19:00 2015', 
    'jobName': 'Job-1'})
