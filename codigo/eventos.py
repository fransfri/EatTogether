"""Funciones para la tabla eventos."""
from db import obtener_conexion


def listar_eventos():
    with obtener_conexion() as db:
        for r in db.execute("SELECT id, nombre, fecha_hora, descripcion, lugar, estado FROM eventos"):
            print(f"ID: {r['id']} | Nombre: {r['nombre']} | Fecha/Hora: {r['fecha_hora']} | Lugar: {r['lugar']} | Estado: {r['estado']}")


def agregar_evento(nombre, fecha_hora, descripcion, lugar="", estado="Planificación"):
    with obtener_conexion() as db:
        db.execute(
            "INSERT INTO eventos(nombre,fecha_hora,descripcion,lugar,estado) VALUES(?,?,?,?,?)",
            (nombre, fecha_hora, descripcion, lugar, estado),
        )
        db.commit()


def obtener_evento(ide):
    with obtener_conexion() as db:
        cur = db.execute("SELECT * FROM eventos WHERE id = ?", (ide,))
        return cur.fetchone()


def editar_evento(ide, nombre, fecha_hora, descripcion, lugar="", estado="Planificación"):
    with obtener_conexion() as db:
        db.execute(
            "UPDATE eventos SET nombre=?, fecha_hora=?, descripcion=?, lugar=?, estado=? WHERE id=?",
            (nombre, fecha_hora, descripcion, lugar, estado, ide),
        )
        db.commit()


def eliminar_evento(ide):
    with obtener_conexion() as db:
        db.execute("DELETE FROM menus WHERE evento_id = ?", (ide,))
        db.execute("DELETE FROM invitados WHERE evento_id = ?", (ide,))
        db.execute("DELETE FROM eventos WHERE id = ?", (ide,))
        db.commit()