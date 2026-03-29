"""Operaciones CRUD sobre la tabla personas."""
from db import obtener_conexion


def listar_personas():
    with obtener_conexion() as db:
        for row in db.execute("SELECT id, nombre, email, telefono, notas FROM personas"):
            print(f"ID: {row['id']} | Nombre: {row['nombre']} | Email: {row['email']} | Tel: {row['telefono']}")


def agregar_persona(nombre, email, telefono, notas=""):
    with obtener_conexion() as db:
        db.execute(
            "INSERT INTO personas(nombre,email,telefono,notas) VALUES(?,?,?,?)",
            (nombre, email, telefono, notas),
        )
        db.commit()


def obtener_persona(idp):
    with obtener_conexion() as db:
        cur = db.execute("SELECT * FROM personas WHERE id = ?", (idp,))
        return cur.fetchone()


def editar_persona(idp, nombre, email, telefono, notas=""):
    with obtener_conexion() as db:
        db.execute(
            "UPDATE personas SET nombre=?, email=?, telefono=?, notas=? WHERE id=?",
            (nombre, email, telefono, notas, idp),
        )
        db.commit()


def eliminar_persona(idp):
    with obtener_conexion() as db:
        db.execute("DELETE FROM invitados WHERE persona_id = ?", (idp,))
        db.execute("DELETE FROM personas WHERE id = ?", (idp,))
        db.commit()