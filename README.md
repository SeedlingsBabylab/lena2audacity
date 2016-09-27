# lena2audacity


## usage

```
$: python lena2aud.py  input_lena5min.csv  output.txt  top_n  subregion_size [--only-output-ranked]
```

input_lena5min.csv: this is the file with all the lena5min sections in it.

output.txt: this is the audacity labels output file that will be created. make sure it ends in .txt

top_n: the number of top regions to rank

subregion_size: the size of the non-overlapping subregions that will be ranked, in units of 5 min. So if you want subregions to be an hour long (i.e. 60 min), then you should put 12. If you want 30 min subregions, then put 6

If you include the --only-output-ranked flag, then only the top_n ranked subregions_size segments will be in the audacity output

regions are ranked based on their CVC sum