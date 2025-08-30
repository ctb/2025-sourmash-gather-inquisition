#! /usr/bin/env python
import sourmash
import sys
import argparse
import csv


from sourmash import picklist


def load_one_sig(filename, *, ksize=31, moltype='DNA', scaled=None):
    db = sourmash.load_file_as_index(filename)
    db = db.select(ksize=ksize, moltype=moltype, scaled=scaled)
    assert len(db) == 1
    sig = list(db.signatures())[0]

    with sig.update() as sig:
        sig.minhash = sig.minhash.downsample(scaled=scaled)

    return sig


def load_specific_sig(db, *, oksize=31, moltype='DNA'):
    db = sourmash.load_file_as_index(filename)
    db = db.select(ksize=ksize, moltype='DNA')
    assert len(db) == 1
    sig = list(db.signatures())[0]

    return sig


def main():
    p = argparse.ArgumentParser()
    p.add_argument('query_sig')
    p.add_argument('metagenome_sig')
    p.add_argument('gather_csv')
    p.add_argument('sourmash_db')
    p.add_argument('--use-match-name', help='the gather file uses "match_name" instead of "name"', action='store_true')
    p.add_argument('-s', '--scaled', default=1000, type=int)
    p.add_argument('-k', '--ksize', default=31, type=int)
    p.add_argument('-m', '--moltype', default='DNA')
    args = p.parse_args()

    query_sig = load_one_sig(args.query_sig,
                             ksize=args.ksize,
                             scaled=args.scaled,
                             moltype=args.moltype)
    metag_sig = load_one_sig(args.metagenome_sig,
                             ksize=args.ksize,
                             scaled=args.scaled,
                             moltype=args.moltype)

    # get just the sketches of interest (those in the gather output)
    pl_type = 'gather'
    if args.use_match_name:
        pl_type = 'prefetch'
    
    pl = picklist.SignaturePicklist(pl_type, pickfile=args.gather_csv)
    pl.load()

    db = sourmash.load_file_as_index(args.sourmash_db)
    db = db.select(picklist=pl, ksize=args.ksize, moltype=args.moltype)

    print(f"Loaded {len(db)} sketches from '{args.sourmash_db}' based on gather file '{args.gather_csv}'")

    name_to_sig = {}
    for dbsig in db.signatures():
        with dbsig.update() as dbsig:
            dbsig.minhash = dbsig.minhash.downsample(scaled=args.scaled)
        name_to_sig[dbsig.name] = dbsig

    assert len(name_to_sig) == len(db)

    name_col = 'name'
    if args.use_match_name:
        name_col = 'match_name'
    with open(args.gather_csv, 'r', newline='') as fp:
        r = csv.DictReader(fp)
        rows = list(r)

    print('')
    print(f"query: {query_sig.name} ({len(query_sig.minhash)} hashes)")
    print(f"metag: {metag_sig.name}")
    query_mh = query_sig.minhash
    metag_mh = metag_sig.minhash

    # isect_mh is the overlap of the query and the metagenome.
    isect_mh = query_mh & metag_mh.flatten()
    f_match_orig = len(isect_mh) / len(query_mh)
    print('')
    print(f"{len(isect_mh)} hashes shared between query and metag ({f_match_orig*100:.1f}% of query)")

    leftover_mh = isect_mh.to_mutable()

    #
    # iterate over all gather matches
    #

    overlaps = []
    total_mh = None
    for rank, row in enumerate(rows):
        name = row[name_col]
        match_sig = name_to_sig[name]
        match_mh = match_sig.minhash

        is_same = " "
        if query_sig == match_sig:
            is_same = "*"

        overlap_mh = isect_mh & match_mh

        # no overlap? skip out on this match.
        if not overlap_mh:
            continue

        # track sum overlap with query/metag intersection
        if total_mh is None:    # initialize
            total_mh = overlap_mh.to_mutable()
        else:
            total_mh += overlap_mh

        delta = len(leftover_mh)
        leftover_mh.remove_many(overlap_mh)
        delta -= len(leftover_mh)

        overlap = len(overlap_mh)
        leftover = len(leftover_mh)
        if overlap:
            overlaps.append((rank, name, overlap, leftover, delta, is_same))

    #overlaps.sort(key=lambda x: -x[1])

    print('')
    print(f"we find the following overlaps with gather matches:")
    print('')
    print(f"rank: overlap name:                             total        remaining  lost")
    print( "----- -------------                             ---------    ---------  -----")
    for (rank, name, overlap, leftover, delta, is_same) in overlaps:
        if len(name) > 40:
            name = name[:37] + '...'
        if delta:
            delta_str = f"-{delta}"
        else:
            delta_str = ""
        print(f"{rank:<4} {is_same}{name:<40}  {overlap:<12} {leftover:<10} {delta_str}")


if __name__ == '__main__':
    sys.exit(main())
