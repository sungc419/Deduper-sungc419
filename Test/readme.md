## Test Edge Cases for PCR Duplicates

The sorted input sam file `Test/test_input_cheryl.sam` is written to test for the following situations/edge cases:

1. UMI not in list
2. UMI match but chrom does not match
3. chrom/UMI matches, but position doesn't match
4. chrom/UMI/position match, but strand doesn't match
5. CIGAR
    1) S on both sides
    2) S on left side only
    3) S on right side only
    4) works correctly for D, I, M, =, X, H, 

The output sam file `Test/expected_output_cheryl.sam` provides the expected output for these cases. 