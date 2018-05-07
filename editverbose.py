with open('/home/rflata/astrolabe_output/verbose/Verbose.txt') as snps, open('/home/rflata/astrolabe_output/verbose/formattedverbose.txt', 'w') as formatted:
    for line in snps:
        if 'Reportable' not in line:
            line = line.replace("/home/rflata/astrolabe_output/verbose/","")
            line = line.replace(".verbose.txt:SLCO1B1","")
            line = line.replace("SLCO1B1","")
            formatted.write(line)
with open('/home/rflata/astrolabe_output/verbose/formattedverbose.txt') as formatted, open('/home/rflata/astrolabe_output/verbose/finalsnps.txt','w') as final:
    for line in formatted:
        line = line.split('\t')
        final.write(line[0] + ';' + line[10] + ';' + line[12])
with open('/home/rflata/astrolabe_output/verbose/finalsnps.txt') as final, open('/home/rflata/astrolabe_output/verbose/rformat.txt','w') as r:
    r.write('Samples,' + 'Hap1,' + 'Hap2,' + 'SNP' + '\n')
    for line in final:
        line = line.strip('\n')
        line = line.strip('\r')
        split = line.split(';')
        ##print(split)
        i = 0
        for i in range(len(split)):
            if split[i] != split[0]:
                split[0] = split[0].replace('*',',').replace('/','')
                if ':2' in split[i]:
                    r.write(split[0] + ',' + split[i].replace(':2','') + '\n')
                r.write(split[0] + ',' + split[i].replace(':1','').replace(':2','') + '\n')
            ##print(i)
        