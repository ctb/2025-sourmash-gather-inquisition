# 2025-sourmash-gather-inquisition

Scripts, tools, and techniques to investigate sourmash gather results

## Usage

Take the metagenome 'SRR606249', the query genome '47.fa.sig', and the
gather results against 'podar-ref.zip', and show relevant overlaps
between the query genome and genomes found by gather.

```
% ./inquisite.py 47.fa.sig SRR606249.trim.sig.zip SRR606249.x.podar-ref.gather.csv podar-ref.zip

Loaded 64 sketches from '../sourmash/podar-ref.zip' based on gather file '../sourmash/SRR606249.x.podar-ref.gather.csv'

query: NC_009665.1 Shewanella baltica OS185, complete genome (5177 hashes)
metag: SRR606249

5167 hashes shared between query and metag (99.8% of query)

we find the following overlaps with gather matches:

rank: overlap name:                             total        remaining
----- -------------                             ---------    ----------
7     NC_011663.1 Shewanella baltica OS223,...   2528         2639        
27    AL954747.1 Nitrosomonas europaea ATCC...   1            2639        
31   *NC_009665.1 Shewanella baltica OS185,...   5167         0           
```
