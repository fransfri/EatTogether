"""Módulo de manejo de menús."""
from db import obtener_conexion


def listar_menus():
    """Lista todos los menús disponibles."""
    with obtener_conexion() as db:
        for r in db.execute("SELECT id, descripcion, ingredientes, precio FROM menus"):
            print(f"ID: {r['id']} | Descripción: {r['descripcion']} | Ingredientes: {r['ingredientes']} | Precio p/p: {r['precio']}")


def agregar_menu(descripcion, ingredientes, precio):
    """Agrega un menú independiente (sin vinculación a evento)."""
    with obtener_conexion() as db:
        db.execute(
            "INSERT INTO menus(descripcion, ingredientes, precio) VALUES(?,?,?)",
            (descripcion, ingredientes, precio),
        )
        db.commit()


def obtener_menu(idm):
    """Obtiene los datos de un menú específico."""
    with obtener_conexion() as db:
        cur = db.execute("SELECT * FROM menus WHERE id = ?", (idm,))
        return cur.fetchone()


def editar_menu(idm, descripcion, ingredientes, precio):
    """Edita los datos de un menú."""
    with obtener_conexion() as db:
        db.execute(
            "UPDATE menus SET descripcion=?, ingredientes=?, precio=? WHERE id=?",
            (descripcion, ingredientes, precio, idm),
        )
        db.commit()


def eliminar_menu(idm):
    """Elimina un menú y todas sus asignaciones a eventos."""
    with obtener_conexion() as db:
        db.execute("DELETE FROM invitados WHERE menu_id = ?", (idm,))
        db.execute("DELETE FROM evento_menus WHERE menu_id = ?", (idm,))
        db.execute("DELETE FROM menus WHERE id = ?", (idm,))
        db.commit()


def obtener_menus_evento(evento_id):
    """Obtiene los menús asignados a un evento."""
    with obtener_conexion() as db:
        return db.execute(
            """SELECT m.id, m.descripcion, m.ingredientes, m.precio 
               FROM menus m
               INNER JOIN evento_menus em ON m.id = em.menu_id
               WHERE em.evento_id = ?""",
            (evento_id,)
        ).fetchall()


def asignar_menu_evento(evento_id, menu_id):
    """Asigna un menú a un evento."""
    with obtener_conexion() as db:
        try:
            db.execute(
                "INSERT INTO evento_menus(evento_id, menu_id) VALUES(?,?)",
                (evento_id, menu_id),
            )
            db.commit()
            return True
        except:
            return False  # Ya estaba asignado


def desasignar_menu_evento(evento_id, menu_id):
    """Desasigna un menú de un evento."""
    with obtener_conexion() as db:
        db.execute(
            "DELETE FROM evento_menus WHERE evento_id = ? AND menu_id = ?",
            (evento_id, menu_id),
        )
        db.commit()


def obtener_menus_mas_elegidos():
    """Obtiene los menús más elegidos ordenados por cantidad de asignaciones."""
    with obtener_conexion() as db:
        return db.execute(
            """SELECT m.descripcion, COUNT(em.menu_id) as veces_elegido
               FROM menus m
               LEFT JOIN evento_menus em ON m.id = em.menu_id
               GROUP BY m.id, m.descripcion
               ORDER BY veces_elegido DESC, m.descripcion ASC"""
        ).fetchall()