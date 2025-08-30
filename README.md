# 2025-sourmash-gather-inquisition

Scripts, tools, and techniques to investigate sourmash gather results

## Usage: `inquisite.py`

Take the metagenome 'SRR606249', the query genome '47.fa.sig', and the
gather results against 'podar-ref.zip', and show relevant overlaps
between the query genome and genomes found by gather.

(In essence, this script performs a 'gather' on the intersection of
the query and the metagenome.)

```
% ./inquisite.py 47.fa.sig SRR606249.trim.sig.zip SRR606249.x.podar-ref.gather.csv podar-ref.zip

Loaded 64 sketches from '../sourmash/podar-ref.zip' based on gather file '../sourmash/SRR606249.x.podar-ref.gather.csv'

query: NC_009665.1 Shewanella baltica OS185, complete genome (5177 hashes)
metag: SRR606249

5167 hashes shared between query and metag (99.8% of query)

we find the following overlaps with gather matches:

rank: overlap name:                             total        remaining  lost
----- -------------                             ---------    ---------  -----
7     NC_011663.1 Shewanella baltica OS223,...  2528         2639       -2528
27    AL954747.1 Nitrosomonas europaea ATCC...  1            2639       
31   *NC_009665.1 Shewanella baltica OS185,...  5167         0          -2639
```

Each row printed out indicates an overlap between that match and the
(query & metagenome) intersection.

Columns: 

- 'total' is the total overlap between the (query & metagenome) intersection and that rank's match; it is independent of rank;
- 'remaining' is the number of hashes from the (query & metagenome) intersection remaining to be allocated at that point in the gather;
- The 'lost' number is the number of hashes from the (query &
  metagenome) intersection that are removed due to that match;

Here the '*' on line 31 indicates that this is identical to the query
signature.
