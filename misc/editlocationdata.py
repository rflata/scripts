import numpy as np

with open('listofvariants.cyp2b6') as variants:
	for line in variants:
		var = line.split(',')

with open('/home/rflata/astrolabe/etc/GRCh38/CYP2B6/locationData.tsv') as lD, open('output.txt','w') as output:
	for line in lD:
		if '#' not in line:
			split = line.split('\t')
			loc = split[1].split(',')
			print(loc)
			int = np.intersect1d(loc, var)
			print(int)
			int = int.tolist()
			output.write(split[0] + '\t')
			output.write(','.join(int) + '\t' + split[2]+ '\t' + split[3])