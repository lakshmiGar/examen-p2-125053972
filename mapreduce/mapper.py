#!/usr/bin/env python3
import sys, csv

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("id,"):      # ignora encabezado
        continue
    try:
        row = next(csv.reader([line]))
        tienda = row[2]
        ingreso = int(row[5]) * float(row[6])   # cantidad * precio_unitario
        print(f"{tienda}\t{ingreso}")
    except (ValueError, IndexError, StopIteration):
        continue                                # línea mal formada: se salta