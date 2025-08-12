# 2025-sourmash-rank-specific-hashes

## Calculate specific and total k-mers on a taxonomic tree

Pick your victims (this is a subset for testing!):
```
sourmash tax grep f__Shewanellaceae -t gtdb-rs226.lineages.csv -o f__Shewanellaceae.lineages.csv
```

Extract sketches:
```
sourmash sig cat --picklist f__Shewanellaceae.lineages.csv:ident:ident gtdb-rs226-reps.k21.sig.zip -o f__Shewanellaceae.sig.zip
```

Build an LCA index:
```
sourmash lca index f__Shewanellaceae.lineages.csv f__Shewanellaceae.lca.json f__Shewanellaceae.sig.zip -k 21 --split-identifiers
```

Verify:
```
sourmash sig summarize f__Shewanellaceae.lca.json
```

Make nodes:
```
./make-nodes.py f__Shewanellaceae.lca.json -o f__Shewanellaceae.taxburst.html
```

et voila, open `f__Shewanellaceae.taxburst.html`.

For each node there will be a 'total count' and a 'hashes specific to
this rank'; the latter should be those k-mers shared among two or more
sub-ranks of that rank.

Link: [f__Shewanellaceae.taxburst.html](https://farm.cse.ucdavis.edu/~ctbrown/f__Shewanellaceae.taxburst.html)
