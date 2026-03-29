"""Funciones CRUD para invitados."""
from db import obtener_conexion


def listar_invitados(evento_id=None):
    with obtener_conexion() as db:
        sql = ("SELECT i.id, p.nombre persona, m.descripcion menu, i.persona_id,"
               " i.evento_id, i.menu_id"
               " FROM invitados i"
               " JOIN personas p ON p.id = i.persona_id"
               " JOIN menus m ON m.id = i.menu_id")
        params = ()
        if evento_id is not None:
            sql += " WHERE i.evento_id = ?"
            params = (evento_id,)
        for r in db.execute(sql, params):
            print(f"ID: {r['id']} | Persona: {r['persona']} | Menú: {r['menu']}")


def agregar_invitado(persona_id, evento_id, menu_id):
    with obtener_conexion() as db:
        db.execute(
            "INSERT INTO invitados(persona_id, evento_id, menu_id) VALUES(?,?,?)",
            (persona_id, evento_id, menu_id),
        )
        db.commit()


def obtener_invitado(idi):
    with obtener_conexion() as db:
        cur = db.execute("SELECT * FROM invitados WHERE id = ?", (idi,))
        return cur.fetchone()


def editar_invitado(idi, menu_id):
    with obtener_conexion() as db:
        db.execute("UPDATE invitados SET menu_id = ? WHERE id = ?", (menu_id, idi))
        db.commit()


def eliminar_invitado(idi):
    with obtener_conexion() as db:
        db.execute("DELETE FROM invitados WHERE id = ?", (idi,))
        db.commit()