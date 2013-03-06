#!/usr/bin/env python

import json
import sys
import prettytable

json_filename = sys.argv[1]

raw = json.load(open(json_filename))
filtered = []
for reviewer, count in raw.items():
    if reviewer in 'smokestack jenkins':
        continue
    filtered.append((count, reviewer))
filtered.sort(reverse=True)

table = prettytable.PrettyTable(('Reviewer', 'Reviews'))
total = 0
for k, v in filtered:
    table.add_row((v, k))
    total += k
print table
print '\nTotal reviews: %d' % total
