#! /usr/bin/env python
import sys
import argparse
import sourmash
from collections import defaultdict

import taxburst

from sourmash.lca.lca_db import LCA_Database
from sourmash.lca import lca_utils


def main():
    p = argparse.ArgumentParser()
    p.add_argument('lca_db')
    p.add_argument('-o', '--taxburst-html', required=True)
    args = p.parse_args()

    db = LCA_Database.load(args.lca_db)

    specific_counts = defaultdict(int)
    total_counts = defaultdict(int)
    
    for hashval, idx_set in db._hashval_to_idx.items():
        lins = []
        for idx in idx_set:
            lid = db._idx_to_lid[idx]
            lin = db._lid_to_lineage[lid]
            if lin[-1].rank == 'strain':
                lin = lin[:-1]  # get rid of strain for now.
            lins.append(lin)

        # find the LCA rank for this k-mer
        tree = lca_utils.build_tree(lins)
        lca, reason = lca_utils.find_lca(tree)
        specific_counts[lca] += 1

        while lin:
            total_counts[lin] += 1
            lin = lin[:-1]

    total_items = list(total_counts.items())
    total_items.sort(key=lambda x: -len(x[0]))
    for k, total in total_items:
        specific = specific_counts.get(k, 0)
        display = lca_utils.display_lineage(k)
        print(display, total, specific)

    # make taxburst node dicts
    nodes_by_tax = {}
    for lin, total in total_items:
        rank = lin[-1].rank
        name = lin[-1].name
        specific = specific_counts.get(lin, 0)

        print('XXX', rank, name, specific)

        node = dict(name=name, rank=rank, count=total, specific=specific)
        nodes_by_tax[lin] = node

    # assign children
    children_by_lin = defaultdict(list)
    top_nodes = []
    for lin, node in nodes_by_tax.items():
        if len(lin) == 1: # top node, no parents
            top_nodes.append(node)
            continue

        parent_lin = lin[:-1]
        children_by_lin[parent_lin].append(node)

    # now go back through and assign children to parent.
    for lin, node in nodes_by_tax.items():
        children = children_by_lin[lin]
        node["children"] = children

    # test the resulting structure:
    taxburst.checks.check_structure(top_nodes)
    taxburst.checks.check_all_counts(top_nodes, fail_on_error=True)

    # define attr
    xtra = { 'specific': "display='hashes specific to this rank'" }

    content = taxburst.generate_html(top_nodes, name=args.lca_db,
                                     extra_attributes=xtra)
    with open(args.taxburst_html, 'wt') as fp:
        fp.write(content)
    print(f"wrote output to '{args.taxburst_html}'")


if __name__ == '__main__':
    sys.exit(main())
