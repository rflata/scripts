import argparse as ag

parser = ag.ArgumentParser(description='List of arguments')
parser.add_argument('-input', '--inputfile', dest='input', required=True)
parser.add_argument('-out', '--outputfile', dest='out', required=True)
args = parser.parse_args()

with open(args.input) as binary, open(args.out,"w") as bases: 
	for line in binary:
		if '#' in line:
			bases.write(line)
		if "#" not in line:
			split = line.split('\t')
			alt = split[4].strip('"').split(',')
			ref = split[3]
			#print(split[8:])
			calls = split[6:]
			#print(calls)
			x = 0
			for i in calls:
				if i.rstrip() == '0|0':
					calls[x] = ref + '|' + ref
					#print(calls[x])
				if i.rstrip() == '0|1':
					calls[x] = ref + '|' + alt[0]
				if i.rstrip() == '1|0':
					calls[x] = alt[0] + '|' + ref
				if i.rstrip() == '1|1':
					calls[x] = alt[0] + '|' + alt[0]
				if i.rstrip() == '0|2':
					calls[x] = ref + '|' + alt[1]
				if i.rstrip() == '2|0':
					calls[x] = alt[1] + '|' + ref
				if i.rstrip() == '2|2':
					calls[x] = alt[1] + '|' + alt[1]
				if i.rstrip() == '1|2':
					calls[x] = alt[0] + '|' + alt[1]
				print(calls[x] + ' ' + str(x))
				x += 1
			bases.write('\t'.join(split[:8]) + '\t')
			bases.write('\t'.join(calls) + '\n')
		