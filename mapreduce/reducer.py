#!/usr/bin/env python3
import sys

actual, total, n = None, 0.0, 0
for line in sys.stdin:
    try:
        k, v = line.rstrip("\n").split("\t")
        v = float(v)
    except ValueError:
        continue
    if k != actual:
        if actual is not None:
            print(f"{actual}\t{total / n:.2f}")
        actual, total, n = k, 0.0, 0
    total += v
    n += 1
if actual is not None:
    print(f"{actual}\t{total / n:.2f}")