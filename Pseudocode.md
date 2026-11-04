## Goal:
Develop a memory-efficient Python script to identify and remove PCR duplicates from a sorted SAM file of uniquely mapped reads, retaining only one copy of each read without loading the entire file into memory.

```
Input: sorted SAM file 
Output: deduplicated SAM file
```

## Define the problem:
PCR duplicates are identical sequencing reads produced during PCR amplification. Their presence can inflate estimates of sequencing depth and introduce bias into downstream analyses that rely on read counts. Removing these duplicates helps ensure that sequencing data more accurately reflect the underlying biological sample.

PCR duplicates will have the same:
- chromosome (RNAME or column 3)
- UMI (end of QNAME or column 1)
- 5' position, calculate with:
    1) 1 base left-most mapping position (POS or column 4)
    2) strand (+/-): either 5'->3' or 3'-> 5' (FLAG or column 2)
    3) CIGAR string (column 6) - either M, S, D, I, N, X 

## Pseudocode:
```
#!/usr/bin/env python

import argparse

set up argparse including input sam file, output sam file, umi file

initialize set to hold UMIs
open and read file:
    loop through each line in file
            strip newline characters 
                    add to set

open input file to read, open outputfile to write:
    loop through each line in file
        if line starts with @:
            write to output file
        else:
            strip newline characters and split by tab 
            if UMI in get_umi and chrom = current chrom (column 3):
                position = column 4
                strand = column 2
                cigar = column 6
            if not in not_duplicate:
                continue
            else:
                write out to file
            add counter for UMI

print out to file:
    # reads kept, # dupes, and # bad UMIs

```

Functions:
```
get_pos(position, cigar, strand):
split cigar string into each section 
for each tuple:
    if strand is forward:
        position - S (left)
    if strand if reverse:
        position + N + D + M + S (right)
return position 


get_umi(column 1):
'''Function to create set of UMIs'''
return last element after splitting by ':'


check_strand(column 2):
if flag & 16 == 16, 
return neg, else return pos





