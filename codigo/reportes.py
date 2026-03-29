"""Consultas de reportes para eventos."""
from db import obtener_conexion


def mostrar_reportes():
    with obtener_conexion() as db:
        eventos = db.execute("SELECT * FROM eventos").fetchall()
        if not eventos:
            print("No hay eventos para reportar.")
            return
        for e in eventos:
            print("----------------------------------------")
            print(f"Evento: {e['nombre']} (ID {e['id']})")
            print(f"Fecha/Hora: {e['fecha_hora']}\nDescripción: {e['descripcion']}")
            print("Menús asociados:")
            for m in db.execute(
                """SELECT m.descripcion, m.precio 
                   FROM menus m
                   INNER JOIN evento_menus em ON m.id = em.menu_id
                   WHERE em.evento_id = ?""", 
                (e['id'],)
            ):
                print(f" -> {m['descripcion']} (Precio: {m['precio']})")
            print("Invitados:")
            sql = ("SELECT p.nombre persona, m.descripcion menu "
                   "FROM invitados i "
                   "JOIN personas p ON p.id=i.persona_id "
                   "JOIN menus m ON m.id=i.menu_id "
                   "WHERE i.evento_id = ?")
            for inv in db.execute(sql, (e['id'],)):
                print(f" -> {inv['persona']} | Menú: {inv['menu']}")
    print("----------------------------------------")