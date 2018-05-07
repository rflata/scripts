import argparse as ag

def readGenome(filename):
	genome = ''
	with open(filename, 'r') as f:
		for line in f:
			# ignore header line with genome information
			if not line[0] == '>':
				genome += line.rstrip()
	return genome

def readSnps(snps):
	dict = {}
	with open(snps, 'r') as s:
		for line in s:
			split = line.split('\t')
			dict[split[0]] = [split[1],split[2].rstrip()]
	return dict

def editRefSeq(dict,genome):
	ref = list(genome)
	for key,value in dict.items():
		if ref[int(key)-1] == value[0]:
			print('g.' + key + value[0] + '>' + value[1]+':' + ref[int(key)-1])
			ref[int(key)-1] = value[1]
			print('g.' + key + value[0] + '>' + value[1]+':' + ref[int(key)-1] + '\n')
		else:
			print('g.' + key + value[0] + '>' + value[1]+':' + 'No Match')
	return ref

def main():
	parser = ag.ArgumentParser(description='List of arguments')
	parser.add_argument('-refseq', '--referencesequence', dest='refseq', required=False)
	parser.add_argument('-snps', '--snps', dest='snps', required=False)
	parser.add_argument('-out', '--outputprefix', dest='out', required=False)
	parser.add_argument('-name', '--fastaname', dest='name', type = str, required=False, default='INSERT TEXT HERE')
	args = parser.parse_args()

	refseq = args.refseq
	
	genome = readGenome(refseq)
	#print(genome[:1000])
	snps = args.snps
	snps = readSnps(snps)
	#print(snps)
	newref = editRefSeq(snps,genome)
	output = args.out + '.fa'
	name = args.name
	with open(output, 'w') as out:
		out.write('>' + name + '\n')
		out.write(''.join(newref))
if __name__ == "__main__": main()