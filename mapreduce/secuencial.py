#!/usr/bin/env python3
import sys, csv, time
from collections import defaultdict

inicio = time.time()
tot, cnt = defaultdict(float), defaultdict(int)
with open(sys.argv[1], newline="") as f:
    next(f, None)                                # encabezado
    for row in csv.reader(f):
        try:
            tot[row[2]] += int(row[5]) * float(row[6])
            cnt[row[2]] += 1
        except (ValueError, IndexError):
            continue
for t in sorted(tot):
    print(f"{t}\t{tot[t] / cnt[t]:.2f}")
print(f"tiempo secuencial: {time.time() - inicio:.2f}s", file=sys.stderr)