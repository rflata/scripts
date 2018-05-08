#!/bin/bash

input=$1
output=$2

FILE=~/projects/openarray/individual/*.vcf.gz
ASTRO=/home/rflata/astrolabe-0.8.3/run-astrolabe.sh
CONFIG=/home/rflata/astrolabe-0.8.3/astrolabe.ini
OUTPUT=~/projects/openarray/astrolabe

echo "Converting csv to vcf..."
python converttovcf.py -input $input -out $output

echo "Calling genotypes..."
for sample in `~/misc/bcftools-1.6/bcftools query -l $output`; do
	echo $sample
	bcftools view $output -Oz -s $sample -o ~/projects/openarray/individual/$sample.vcf.gz
	echo ~/projects/openarray/individual/$sample.vcf.gz
	$ASTRO -conf $CONFIG -ref GRCh38 -targets CYP2D6 -inputVCF ~/projects/openarray/individual/$sample.vcf.gz -skipVcfQC -filter PASS -outFile $OUTPUT/$sample.astrolabe.tsv -verboseFile $OUTPUT/verbose/$sample.verbose.txt
done

grep "" ~/projects/openarray/astrolabe/*.astrolabe.tsv > ~/projects/openarray/astrolabe/batchgenotypes.txt
grep "" ~/projects/openarray/astrolabe/verbose/*.verbose.txt > ~/projects/openarray/astrolabe/Verbose.txt

python Striphashlines.py ~/projects/openarray/astrolabe/batchgenotypes.txt ~/projects/openarray/astrolabe/batchgenotypes.filtered.csv

echo "DONE"