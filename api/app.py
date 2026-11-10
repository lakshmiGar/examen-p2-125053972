import os, time
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)

def conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

def run(sql, params=(), fetch=True):
    c = conn()
    try:
        with c, c.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch else cur.rowcount
    finally:
        c.close()

def init_db():
    for _ in range(30):
        try:
            run("""CREATE TABLE IF NOT EXISTS resultados (
                     tienda VARCHAR(10) PRIMARY KEY,
                     ticket_promedio NUMERIC(12,2) NOT NULL)""", fetch=False)
            return
        except psycopg2.OperationalError:
            time.sleep(2)
    raise RuntimeError("No se pudo conectar a la base de datos")

SEL = "SELECT tienda, ticket_promedio::float AS ticket_promedio FROM resultados"

@app.get("/resultados")
def listar():
    return jsonify(run(SEL + " ORDER BY tienda"))

@app.get("/resultados/<tienda>")
def obtener(tienda):
    rows = run(SEL + " WHERE tienda = %s", (tienda,))
    return (jsonify(rows[0]), 200) if rows else (jsonify(error="no encontrado"), 404)

@app.post("/resultados")
def crear():
    d = request.get_json(force=True)
    try:
        run("INSERT INTO resultados (tienda, ticket_promedio) VALUES (%s, %s)",
            (d["tienda"], d["ticket_promedio"]), fetch=False)
    except psycopg2.IntegrityError:
        return jsonify(error="ya existe"), 409
    return jsonify(d), 201

@app.put("/resultados/<tienda>")
def actualizar(tienda):
    d = request.get_json(force=True)
    n = run("UPDATE resultados SET ticket_promedio = %s WHERE tienda = %s",
            (d["ticket_promedio"], tienda), fetch=False)
    return (jsonify(tienda=tienda, **d), 200) if n else (jsonify(error="no encontrado"), 404)

@app.delete("/resultados/<tienda>")
def borrar(tienda):
    n = run("DELETE FROM resultados WHERE tienda = %s", (tienda,), fetch=False)
    return ("", 204) if n else (jsonify(error="no encontrado"), 404)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)