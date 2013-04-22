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

table = prettytable.PrettyTable(('Reviewer', 'Reviews (-2|-1|+1|+2)'))
total = 0
for k, v in filtered:
    r = '%d (%d|%d|%d|%d)' % (k['total'],
            k['votes']['-2'], k['votes']['-1'],
            k['votes']['1'], k['votes']['2'])
    table.add_row((v, r))
    total += k['total']
print table
print '\nTotal reviews: %d' % total
