#! /bin/bash

while IFS=$'\t' read sample v; do
	bcftools view -R coords.txt -c1 $v|bcftools norm -d any|bcftools sort -Oz -o /home/rflata/projects/simcyp/snps/single/$sample.vcf.gz
	tabix /home/rflata/projects/simcyp/snps/single/$sample.vcf.gz
	
	/software/runes/current/bin/create-warehouse-file.sh \
	-c /software/runes/conf/runes.prod.ini \
	-i /home/rflata/projects/simcyp/snps/single/$sample.vcf.gz \
	-o /home/rflata/projects/simcyp/snps/csv/$sample.csv 

done < /home/rflata/sample.locations/chelsea.txt

FILE=/home/rflata/projects/simcyp/snps/single/*.vcf.gz
bcftools merge $FILE -m all -0|bcftools view -a|bcftools annotate -x INFO,^FORMAT/GT -Oz -o cc.merge.vcf.gz

tabix cc.merge.vcf.gz

java -jar ~/misc/snpEff/snpEff/SnpSift.jar \
    annotate \
    -v \
    ~/vcf/clinvar/clinvar.vcf.gz \
    ~/projects/simcyp/snps/cc.merge.vcf.gz \
    > ~/projects/simcyp/snps/cc.merge.annotate.vcf
bgzip -f cc.merge.annotate.vcf
tabix cc.merge.annotate.vcf.gz

bcftools annotate -a ~/vcf/dbsnp/00-common_all.vcf.gz -c ID cc.merge.annotate.vcf.gz -Oz -o cc.allsamples.vcf.gz
tabix cc.allsamples.vcf.gz