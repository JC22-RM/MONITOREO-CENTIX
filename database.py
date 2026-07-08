import sqlite3

conexion = sqlite3.connect("incidencias.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
INSERT OR IGNORE INTO usuarios
(id,usuario,password)
VALUES
(1,'admin','123456')
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")