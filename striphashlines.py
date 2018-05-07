import sys
import os
file = sys.argv[1]
out = sys.argv[2]
print(file)
print(out)
with open(file) as astrolabe, open(out, 'w') as stripped:
	for line in astrolabe:
		if '#' not in line:
			l = line.split("\t")
			print(os.path.basename(l[0]))
			l[0] = os.path.basename(l[0])
			split = l[0].split('.')
			l[0] = split[0]
			##l = line.replace("SLCO1B1","")
			##print(l[:2])
			stripped.write(','.join(l[:2])+ ","+ l[4] + "\n")
