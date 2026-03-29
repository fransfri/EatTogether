# db.py
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "../datos/eatogether.db")

def obtener_conexion():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row        # filas accesibles como diccionarios
    return conn

def inicializar_bd():
    # Crear carpeta datos si no existe
    datos_dir = os.path.dirname(DB_FILE)
    if not os.path.exists(datos_dir):
        os.makedirs(datos_dir)
    
    with obtener_conexion() as db:
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS personas(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefono TEXT NOT NULL,
                        notas TEXT
                    )""")
        c.execute("""CREATE TABLE IF NOT EXISTS eventos(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        fecha_hora TEXT NOT NULL,
                        descripcion TEXT NOT NULL,
                        lugar TEXT,
                        estado TEXT
                    )""")
        c.execute("""CREATE TABLE IF NOT EXISTS menus(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        descripcion TEXT NOT NULL,
                        ingredientes TEXT NOT NULL,
                        precio TEXT NOT NULL
                    )""")
        c.execute("""CREATE TABLE IF NOT EXISTS evento_menus(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        evento_id INTEGER NOT NULL,
                        menu_id INTEGER NOT NULL,
                        UNIQUE(evento_id, menu_id),
                        FOREIGN KEY(evento_id) REFERENCES eventos(id) ON DELETE CASCADE,
                        FOREIGN KEY(menu_id) REFERENCES menus(id) ON DELETE CASCADE
                    )""")
        c.execute("""CREATE TABLE IF NOT EXISTS invitados(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        persona_id INTEGER NOT NULL,
                        evento_id INTEGER NOT NULL,
                        menu_id INTEGER NOT NULL,
                        FOREIGN KEY(persona_id) REFERENCES personas(id),
                        FOREIGN KEY(evento_id) REFERENCES eventos(id),
                        FOREIGN KEY(menu_id) REFERENCES menus(id)
                    )""")
        db.commit()