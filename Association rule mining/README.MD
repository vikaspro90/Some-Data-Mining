Association rules are useful for identifying dependencies of an item on another item in transaction data. The programs in this set are designed to follow a systematic approach in deducing association rules on a given dataset. First, they find the frequent itemsets and then they form rules form those itemsets.

The input to the main program must be 1s and 0s as specified in the sampleBinary.txt file. 1 indicates presence of that item in the transaction and 0 indicates absence. However, any classification dataset can be transformed into this format using various approaches. One simple approach is available in this repo. Check Usage.docx.

Three techniques have been employed for frequent itemset generation. Brute force, F(k-1) * F(k) and F(k-1) * F(k-1). Any one of them can be chosen while invoking the program.

Rule generation can either be done using confidence based pruning or generating the rules by brute force and then using lift as the filtering factor.

Detailed usage instructions can be found in Usage.docx.

Python and numPy on PyCharm IDE.
