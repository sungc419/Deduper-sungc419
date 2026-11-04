#!/usr/bin/env python

import argparse

def get_args():
    parser = argparse.ArgumentParser(description = "A program that extracts RoCCs with PhyloP score greater than or equal to 2.270 , merging neighboring RoCCs that are separated by 1 bp. It takes input bedgraph.gz file and outputs unsorted tsv file. User can set size threshold for RoCC.")
    parser.add_argument("-f", "--file", help="designates absolute file path to sorted sam file", required = True) 
    parser.add_argument("-o", "--outfile", help="designates absolute file path to deduplicated sam file", required = True)
    parser.add_argument("-u", "--umi", help="designates file containing the list of UMIs", required = True)
    return parser.parse_args()

args = get_args()
file = args.file
outfile = args.outfile
umi = args.umi

umi_set = set()
with open(umi, "r") as fh:
    for line in fh:
        line = line.strip()
        umi_set.add(line)

def get_umi(qname: str)-> str:
    '''Function that gets the UMI from the QNAME column in SAM file'''
    qnamelst = qname.strip().split(":")
    lastCol = qnamelst[7]
    return lastCol

def check_strand(flag: str)-> bool:
    '''Function that checks the bitwise flag column in SAM file'''
    if ((int(flag) & 16) == 16):
        rev_comp = True # negative strand
    else:
        rev_comp = False # positive strand
    return rev_comp

def split_cigar (cigar:str) -> str:
    '''Function that splits cigar string into a list of groups of numbers and letters in order'''
    cigarList = []
    i = 0

    while i < len(cigar):
        j = i
        if cigar[j].isdigit():
            while j < len(cigar) and cigar[j].isdigit():
                j+=1
            cigarList.append(cigar[i:j])
            i=j
        else:
            cigarList.append(cigar[i])
            i+=1
    return cigarList

def get_fivePrimePos (pos:str, rev_comp: bool, cigarList:list) -> int:
    '''Function that derives the 5'position from strand, cigar string, and 1-based leftmost mapping position.'''

    SecondItem = cigarList[1]
    lastItem = cigarList[-1]
    total = 0

    if not rev_comp: # fw strand (+), rev_comp == False
        if SecondItem =='S':
            fivePrimePos = int(pos) - int(cigarList[0])
        else:   
            fivePrimePos = int(pos)
    else: # rev comp strand (-), rev_comp == True
        for i in range(0, len(cigarList), 2):
            length =  int(cigarList[i])
            op = cigarList[i+1]
            if op in ('M','X','D','=','N'):
                total += length
        if lastItem =='S':
            fivePrimePos = int(pos) + int(cigarList[-2]) + total - 1
        else:
            fivePrimePos = int(pos) + total - 1
    return fivePrimePos  

setReads = set() # stores all reads?
unmatchedUMI = 0 # initializes variable for counting umi's not in list
matchedUMI = 0 # initializes variable for counting umi's in list
duplicate = 0

with open(file, "r") as input, open (outfile, "w") as output: 
    for line in input:
        if line.startswith("@"):
            output.write(line)
        else:
            lineSplit = line.strip().split("\t")
            qname = lineSplit[0]
            chrom = lineSplit[2]
            pos = lineSplit[3]
            flag = lineSplit[1]
            cigar = lineSplit[5]

            umi = get_umi(qname)
            rev_comp = check_strand(flag)
            cigarList = split_cigar(cigar) 
            fivePrimePos = get_fivePrimePos(pos, rev_comp, cigarList)   

            if umi not in umi_set:
                unmatchedUMI += 1  # add 1 if encounter unmatched UMI
                continue

            key = chrom, umi, rev_comp, fivePrimePos

            if key not in setReads:
                matchedUMI += 1
                setReads.add(key)
                output.write(line)
            else:
                duplicate += 1

#     print headerlines, unique reads/reads kept, # dupes, and # bad UMIs
with open("results.txt", "w") as f:
    f.write(f'The number of reads kept is {matchedUMI}.\n')
    f.write(f'The number of duplicates is {duplicate}.\n')
    f.write(f'The number of unmatched UMIs is {unmatchedUMI}.\n')




