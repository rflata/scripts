import pandas as pd
import numpy as np
import argparse as ag

#Argument parser
parser = ag.ArgumentParser(description='List of arguments')
parser.add_argument('-input', '--inputfile', dest='input', required=True)
parser.add_argument('-out', '--outputfile', dest='out', required=True)
args = parser.parse_args()

skip = 0
with open(args.input, 'r') as input:
	for line in input:
		if '##' in line:
			skip += 1

csv = pd.read_table(args.input, skiprows = skip)
csv = csv.transpose()
csv = csv.drop(['FILTER','FORMAT','INFO','QUAL','#CHROM'])
csv = csv.replace('1/1',2).replace('0/0',0).replace('1/0',1).replace('0/1',1).replace('./.','NOAMP')

with open(args.out,'w') as out:
	csv.to_csv(out)