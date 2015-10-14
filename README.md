# Thermal Properties of MicroStructures


This is an example of how to run multiple iterations of a given experiment and write the results to file. 
The idea is to load in the relevant material data, choose which experiment to simulate, then generate the
matrix with inclusions and subject it to heat boundary conditions. Since the inclusions are randomly generated
then run the same simulation multiple times then the average should yield an accurate answer.

```python
import numpy
execfile('helperTwoD.py')
trialsPer = 3 # Number of times to run each experiment

materials = getMaterialList() # Load in material Data
matrix = "ESBR" # Choose the first experiment from TCNanoFillers
fillers = ["Alumina", "ZincOxide"] # Two fillers associated with first experiment

fileName = matrix+fillers[0] + fillers[1] # Name file after matrix, filler materials
f = open(fileName, 'w')
f.write('Matrix\tFiller\tPortion\tRadius\tNumber\tSide\tSeed\tNodes\tq\tdT\tk\tWarn\n')

for i in range(len(materials[matrix]['fillers'])): # "For each filler material"
	modelObject, modelName = createModel(1) # Create model database "Model-1"
	side, radius, portions, dP, dM = defExperiment(matrix, fillers[i]) # Define material attributes for specified matrix, fillers
	
	for j in range(len(portions)): # "For each PHR/volume portion specified"
		for k in range(trialsPer): # "Run trialsPer times for each material/filler/PHR combination"
			seed = numpy.random.randint(1000) # Random seed for coordinate generation
			radius, number = invPHR(portions[j], dP, radius, dM, side) # Returns specific radius size and number of inclusions for closest PHR value.
			xVals, yVals, warningPoints = getPoints(seed, side, radius, number) # returns coordinates for inclusion locations. 
			part = createMatrix(side) # Create the matrix
			edges1, vertices1, face1 = assignGeomSequence(part) # Create references to important sets in our part
			matrixSet, fillerSet, allSet = createCircleInclusion(radius, number, xVals, yVals) # Draw inclusions in the matrix
			createSection(matrix, matrixSet) # Create section for matrix material
			createSection(fillers[i], fillerSet) # Create section for filler material
			assemblyTop, assemblyBottom = makeAssembly() # Create assembly and return references to assembly sets
			temp1, temp2 = 328.15, 298.15 # Assign heat temperature to be used in experiment
			heatStep(temp1, temp2) # apply heat BC
			elements, nodes = makeMesh() # Draw mesh and return number of nodes and elements
			warningString = submitJob() # Submit job and take note of any warnings
			avgHF, TC = getThermalProperties() # Extract relevant information about thermal properties
			f.write(dataString(matrix, fillers[i], portions[j])) # Write the data to file
	
f.close()
```

The above code yield something like the following:

|Matrix |Filler |Portion |Radius	|Number |Side|Seed|Nodes|q		|dT|k			  |Warn|
|-------|-------|--------|----------|-------|----|----|-----|-------|---|--------------|----|
|ESBR	|Alumina|10		|35.625		|1		|520 |73  |63961|11880  |30 |0.205934697452|    |
|ESBR	|Alumina|10		|33.84375	|1		|520 |393 |64213|11840  |30 |0.205238987547|    |
|ESBR	|Alumina|10		|32.1515625	|1		|520 |987 |63717|11870  |30 |0.205747231892|    |
|ESBR	|Alumina|20		|32.1515625	|2		|520 |19  |64405|12082  |30 |0.209427187135|    |
|ESBR	|Alumina|20		|32.1515625	|2		|520 |127 |64621|12142  |30 |0.210466024411|    |
|ESBR	|Alumina|20		|32.1515625	|2		|520 |712 |64325|12070  |30 |0.209219267061|    |
|ESBR	|Alumina|40		|31.50853125|4		|520 |173 |64381|12625  |30 |0.21884291495 |    |
|ESBR	|Alumina|40		|31.82361656|4		|520 |971 |64817|12748  |30 |0.220973009538|    |
|ESBR	|Alumina|40		|31.82361656|4		|520 |71  |64681|12612  |30 |0.218612506119|    |
|ESBR	|Alumina|80		|33.09656122|7		|520 |360 |65157|13927  |30 |0.241403366676|    |
|ESBR	|Alumina|80		|33.09656122|7		|520 |929 |64693|13878  |30 |0.240558376096|    |
|ESBR	|Alumina|80		|33.09656122|7		|520 |14  |64997|13812  |30 |0.239412858642|    |
|ESBR	|Alumina|100	|34.08945806|8		|520 |14  |64933|14087  |30 |0.244174824414|    |
|ESBR	|Alumina|100	|32.38498515|9		|520 |853 |65817|14398  |30 |0.249567367518|    |
|ESBR	|Alumina|100	|32.38498515|9		|520 |955 |65749|14373  |30 |0.249146389227|    |
|ESBR	|ZincOxide|5	|21.375		|1		|350 |487 |70445|17578  |30 |0.205082763439|    |
|ESBR	|ZincOxide|5	|20.30625	|1		|350 |364 |70477|17456  |30 |0.203658669484|    |
|ESBR	|ZincOxide|5	|19.2909375	|1		|350 |556 |70577|17490  |30 |0.20405327269 |    |
|ESBR	|ZincOxide|10	|18.32639062|2		|350 |707 |70645|17720  |30 |0.206741745656|    |
|ESBR	|ZincOxide|10	|17.77659890|2		|350 |863 |70737|17716  |30 |0.20669186    |    |
|ESBR	|ZincOxide|10	|17.77659890|2		|350 |648 |70889|17723  |30 |0.206773884713|    |
|ESBR	|ZincOxide|20	|17.59883291|4		|350 |34  |70413|18247  |30 |0.212886753524|    |
|ESBR	|ZincOxide|20	|17.59883291|4		|350 |935 |70621|18192  |30 |0.212243891912|    |
|ESBR	|ZincOxide|20	|17.59883291|4		|350 |836 |70185|18199  |30 |0.2123313335  |    |
|ESBR	|ZincOxide|40	|17.42284458|8		|350 |43  |71777|19366  |30 |0.225941554654|    | 
