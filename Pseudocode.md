Goal: Identify and remove PCR duplicates from a SAM file of uniquely mapped reads by writing a python script to read a sorted sam file of uniquely mapped reads and remove all PCR duplicates, retaining only a single copy of each read and outputting a sam file.

Define the problem: PCR duplicates are identical sequencing reads that arise during PCR amplification. They should be removed because they could cause a bias in sequencing depth and affect analyses that rely on the sequencing counts. The goal of this project is to identify and remove PCR duplicates from a SAM file of uniquely mapped reads.

PCR duplicates will have the same:
- chromosome 
- left-most mapping position and 5' position (to account for soft clipping)
- strand
- UMI

```
#!/usr/bin/env python

import argparse
import gzip

set up argparse including input sam file, output sam file, umi file

initialize list to hold UMIs
open and read file:
    loop through each line in file
            strip newline characters and split by tab
                if line not in list:
                    add to list

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


```
get_pos(position, cigar, strand):
split cigar string into each section 
for each tuple:
    if tuple is 'S':
        set that as soft clipped
return position 

get_umi(column 1):
'''Function to create list of UMIs'''
return last element after splitting by ':'

check_strand(column 2):
if flag & 16 == 16, return neg, else return pos

is_duplicate:
'''Function to check if a record is a PCR duplicate'''
Check flag for reverse or not
return true if true, false if false
```


