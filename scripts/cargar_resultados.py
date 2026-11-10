import os, sys
import psycopg2

ruta = sys.argv[1] if len(sys.argv) > 1 else "/data/output/resultado/part-00000"
c = psycopg2.connect(
    host=os.environ.get("DB_HOST", "db"),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)
n = 0
with c, c.cursor() as cur:
    cur.execute("""CREATE TABLE IF NOT EXISTS resultados (
                     tienda VARCHAR(10) PRIMARY KEY,
                     ticket_promedio NUMERIC(12,2) NOT NULL)""")
    with open(ruta) as f:
        for line in f:
            p = line.strip().split("\t")
            if len(p) != 2:
                continue
            cur.execute("""INSERT INTO resultados (tienda, ticket_promedio) VALUES (%s, %s)
                           ON CONFLICT (tienda) DO UPDATE SET ticket_promedio = EXCLUDED.ticket_promedio""",
                        (p[0], float(p[1])))
            n += 1
c.close()
print(f"{n} registros cargados")