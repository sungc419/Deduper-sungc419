#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --job-name=Dedup
#SBATCH --cpus-per-task=8 
#SBATCH --time=12:00:00
#SBATCH --out=/projects/bgmp/csung/bioinfo/Bi624/Deduper-sungc419/slurm/slurm%j.out
#SBATCH --err=/projects/bgmp/csung/bioinfo/Bi624/Deduper-sungc419/slurm/slurm%j.err

# TEST FILES:

# Cheryl's test file:
# /usr/bin/time -v ./Sung_deduper.py -u STL96.txt -f Test/test_input_cheryl.sam -o Test/test_output_cheryl.sam

# Test file provided by assignment:
# /usr/bin/time -v ./Sung_deduper.py -u STL96.txt -f Test/test.sam -o Test/test_output.sam

# ACTUAL FILE:

samtools sort -O sam -T tmp. -o /projects/bgmp/csung/bioinfo/Bi624/Deduper-sungc419/C1_SE_uniqAlign_sorted.sam /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam

/usr/bin/time -v ./Sung_deduper.py -u STL96.txt -f /projects/bgmp/csung/bioinfo/Bi624/Deduper-sungc419/C1_SE_uniqAlign_sorted.sam -o Sung_deduped.sam
