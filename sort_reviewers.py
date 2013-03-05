#!/usr/bin/env python

import json
import sys

json_filename = sys.argv[1]

raw = json.load(open(json_filename))
filtered = []
for reviewer, count in raw.items():
    if reviewer in 'smokestack jenkins':
        continue
    filtered.append((count, reviewer))
print '\n'.join('%d %s' % x for x in sorted(filtered, reverse=True))
