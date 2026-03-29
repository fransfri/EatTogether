from db import inicializar_bd
from personas import listar_personas, agregar_persona, obtener_persona, editar_persona, eliminar_persona
from eventos import listar_eventos, agregar_evento, obtener_evento, editar_evento, eliminar_evento
from menus import listar_menus, agregar_menu, obtener_menu, editar_menu, eliminar_menu
from invitados import (listar_invitados, agregar_invitado,
                        obtener_invitado, editar_invitado, eliminar_invitado)
from reportes import mostrar_reportes


def input_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("El valor no puede estar vacío.")


def mostrar_menu_principal():
    print('''
1. Eventos
2. Personas
3. Invitados
4. Reportes
5. Menús
6. Salir
''')

# --- wrappers de interfaz sobre los módulos de datos ---

# Personas

def cmd_listar_personas():
    listar_personas()


def cmd_agregar_persona():
    nombre = input_nonempty("Nombre completo: ")
    email = input_nonempty("Email: ")
    telefono = input_nonempty("Teléfono: ")
    agregar_persona(nombre, email, telefono)
    print("Persona agregada.")


def cmd_editar_persona():
    listar_personas()
    try:
        idp = int(input("ID de la persona a editar: "))
    except ValueError:
        print("ID inválido.")
        return
    persona = obtener_persona(idp)
    if not persona:
        print("Persona no encontrada.")
        return
    nombre = input_nonempty(f"Nombre ({persona['nombre']}): ")
    email = input_nonempty(f"Email ({persona['email']}): ")
    telefono = input_nonempty(f"Teléfono ({persona['telefono']}): ")
    editar_persona(idp, nombre, email, telefono)
    print("Persona actualizada.")


def cmd_eliminar_persona():
    listar_personas()
    try:
        idp = int(input("ID de la persona a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return
    eliminar_persona(idp)
    print("Persona eliminada (y sus invitaciones).")

# Eventos

def cmd_listar_eventos():
    listar_eventos()


def cmd_agregar_evento():
    nombre = input_nonempty("Nombre del evento: ")
    fecha_hora = input_nonempty("Fecha y hora (YYYY-MM-DD HH:MM): ")
    descripcion = input_nonempty("Descripción: ")
    agregar_evento(nombre, fecha_hora, descripcion)
    print("Evento agregado.")


def cmd_editar_evento():
    listar_eventos()
    try:
        ide = int(input("ID del evento a editar: "))
    except ValueError:
        print("ID inválido.")
        return
    evento = obtener_evento(ide)
    if not evento:
        print("Evento no encontrado.")
        return
    nombre = input_nonempty(f"Nombre ({evento['nombre']}): ")
    fecha_hora = input_nonempty(f"Fecha y hora ({evento['fecha_hora']}): ")
    descripcion = input_nonempty(f"Descripción ({evento['descripcion']}): ")
    editar_evento(ide, nombre, fecha_hora, descripcion)
    print("Evento actualizado.")


def cmd_eliminar_evento():
    listar_eventos()
    try:
        ide = int(input("ID del evento a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return
    eliminar_evento(ide)
    print("Evento y sus datos asociados eliminados.")

# Menús

def cmd_listar_menus(filtro_evento=None):
    listar_menus(filtro_evento)


def cmd_agregar_menu():
    listar_eventos()
    try:
        ide = int(input("ID del evento al que pertenece el menú: "))
    except ValueError:
        print("ID inválido.")
        return
    if not obtener_evento(ide):
        print("Evento no encontrado.")
        return
    descripcion = input_nonempty("Descripción del menú: ")
    ingredientes = input_nonempty("Ingredientes (comma-separated): ")
    precio = input_nonempty("Precio por persona: ")
    agregar_menu(ide, descripcion, ingredientes, precio)
    print("Menú agregado.")


def cmd_editar_menu():
    listar_menus()
    try:
        idm = int(input("ID del menú a editar: "))
    except ValueError:
        print("ID inválido.")
        return
    menu = obtener_menu(idm)
    if not menu:
        print("Menú no encontrado.")
        return
    descripcion = input_nonempty(f"Descripción ({menu['descripcion']}): ")
    ingredientes = input_nonempty(f"Ingredientes ({menu['ingredientes']}): ")
    precio = input_nonempty(f"Precio ({menu['precio']}): ")
    editar_menu(idm, descripcion, ingredientes, precio)
    print("Menú actualizado.")


def cmd_eliminar_menu():
    listar_menus()
    try:
        idm = int(input("ID del menú a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return
    eliminar_menu(idm)
    print("Menú eliminado (invitados actualizados).")

# Invitados

def cmd_listar_invitados(filtro_evento=None):
    listar_invitados(filtro_evento)


def cmd_agregar_invitado():
    listar_personas()
    try:
        idp = int(input("ID de la persona a invitar: "))
    except ValueError:
        print("ID inválido.")
        return
    if not obtener_persona(idp):
        print("Persona no encontrada.")
        return
    listar_eventos()
    try:
        ide = int(input("ID del evento: "))
    except ValueError:
        print("ID inválido.")
        return
    if not obtener_evento(ide):
        print("Evento no encontrado.")
        return
    print("Menús disponibles para el evento:")
    listar_menus(filtro_evento=ide)
    try:
        idm = int(input("ID del menú elegido: "))
    except ValueError:
        print("ID inválido.")
        return
    menu = obtener_menu(idm)
    if not menu or menu['evento_id'] != ide:
        print("Menú inválido para ese evento.")
        return
    agregar_invitado(idp, ide, idm)
    print("Invitado agregado.")


def cmd_editar_invitado():
    listar_invitados()
    try:
        idi = int(input("ID del invitado a editar: "))
    except ValueError:
        print("ID inválido.")
        return
    inv = obtener_invitado(idi)
    if not inv:
        print("Invitado no encontrado.")
        return
    print("Menús disponibles para el evento:")
    listar_menus(filtro_evento=inv['evento_id'])
    try:
        idm = int(input("ID del nuevo menú: "))
    except ValueError:
        print("ID inválido.")
        return
    menu = obtener_menu(idm)
    if not menu or menu['evento_id'] != inv['evento_id']:
        print("Menú inválido para ese evento.")
        return
    editar_invitado(idi, idm)
    print("Invitado actualizado.")


def cmd_eliminar_invitado():
    listar_invitados()
    try:
        idi = int(input("ID del invitado a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return
    eliminar_invitado(idi)
    print("Invitado eliminado.")

# submenus same as before calling cmd_ functions

def submenu_personas():
    while True:
        print("\nPersonas: 1.agregar 2.editar 3.eliminar 4.listar 5.volver")
        op = input("Opción: ")
        if op == '1':
            cmd_agregar_persona()
        elif op == '2':
            cmd_editar_persona()
        elif op == '3':
            cmd_eliminar_persona()
        elif op == '4':
            cmd_listar_personas()
        elif op == '5':
            break
        else:
            print("Opción inválida.")

def submenu_eventos():
    while True:
        print("\nEventos: 1.agregar 2.editar 3.eliminar 4.listar 5.volver")
        op = input("Opción: ")
        if op == '1':
            cmd_agregar_evento()
        elif op == '2':
            cmd_editar_evento()
        elif op == '3':
            cmd_eliminar_evento()
        elif op == '4':
            cmd_listar_eventos()
        elif op == '5':
            break
        else:
            print("Opción inválida.")

def submenu_menus():
    while True:
        print("\nMenús: 1.agregar 2.editar 3.eliminar 4.listar 5.volver")
        op = input("Opción: ")
        if op == '1':
            cmd_agregar_menu()
        elif op == '2':
            cmd_editar_menu()
        elif op == '3':
            cmd_eliminar_menu()
        elif op == '4':
            cmd_listar_menus()
        elif op == '5':
            break
        else:
            print("Opción inválida.")

def submenu_invitados():
    while True:
        print("\nInvitados: 1.agregar 2.editar 3.eliminar 4.listar 5.volver")
        op = input("Opción: ")
        if op == '1':
            cmd_agregar_invitado()
        elif op == '2':
            cmd_editar_invitado()
        elif op == '3':
            cmd_eliminar_invitado()
        elif op == '4':
            cmd_listar_invitados()
        elif op == '5':
            break
        else:
            print("Opción inválida.")


def main():
    inicializar_bd()
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == '1':
            submenu_eventos()
        elif opcion == '2':
            submenu_personas()
        elif opcion == '3':
            submenu_invitados()
        elif opcion == '4':
            mostrar_reportes()
        elif opcion == '5':
            submenu_menus()
        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


from interfaz import EatTogetherApp
from ttkthemes import ThemedTk
from db import inicializar_bd

if __name__ == '__main__':
    inicializar_bd()
    root = ThemedTk(theme="arc")
    app = EatTogetherApp(root)
    root.mainloop()

