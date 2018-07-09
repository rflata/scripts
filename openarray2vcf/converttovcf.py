import pandas as pd
import numpy as np
import argparse as ag
#import time

#Argument parser
parser = ag.ArgumentParser(description='List of arguments')
parser.add_argument('-input', '--inputfile', dest='input', required=True)
parser.add_argument('-out', '--outputfile', dest='out', required=True)
args = parser.parse_args()

#Getting system time
#timestr = time.strftime("%Y%m%d-%H%M%S")

#Converts the output from Taqman Genotyper to VCF format
#Currently only supports CYP2D6
df = pd.read_csv(args.input, comment='#')
df.columns = df.columns.str.replace(' ','_')

df = df[~df['Gene_Symbol'].str.contains('remove', na=False)]

df = df[df.Sample_ID != 'NTC']

#df = df[df['Assay_Name_or_ID'].str.contains('42126611', na=False)]

df['combined']= df['Allele_1_Call'] + '/' + df['Allele_2_Call']
pivot = df.pivot(index='Sample_ID',columns='Assay_Name_or_ID',values='combined')

pivot = pivot.T
pivot = pivot.reset_index()
pivot = pivot.fillna(value='./.')

#pivot.insert(0,'#CHROM',22)
pivot.columns.values[0]='POS'
pivot.sort_values(by=['POS'])
#print(pivot)
pivot[['#CHROM', 'POS', 'ID', 'REF', 'ALT']] = pivot['POS'].str.split('/',expand=True)


tmp = pivot['#CHROM']
vcf = pivot.drop('#CHROM', 1)
vcf.insert(0,'#CHROM',tmp)

tmp = pivot['ID']
vcf = vcf.drop('ID', 1)
vcf.insert(2,'ID',tmp)

tmp = vcf['REF']
vcf = vcf.drop('REF', 1)
vcf.insert(3,'REF',tmp)

tmp = vcf['ALT']
vcf = vcf.drop('ALT', 1)
vcf.insert(4,'ALT',tmp)

vcf.insert(5,'QUAL','.')
vcf.insert(6,'FILTER','PASS')
vcf.insert(7,'INFO','.')
vcf.insert(8,'FORMAT','GT')

vcf.replace('NOAMP/NOAMP','./.',inplace=True)
vcf.replace('UND/UND','./.',inplace=True)

#print(vcf)

with open('header.txt') as header, open(args.out,'w') as openarray:
	for line in header:
		openarray.write(line)
with open(args.out,'a') as openarray:
	vcf.to_csv(openarray, index=False, sep='\t')

