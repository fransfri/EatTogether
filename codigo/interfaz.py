import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import re
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from db import inicializar_bd
from personas import listar_personas, agregar_persona, obtener_persona, editar_persona, eliminar_persona
from eventos import listar_eventos, agregar_evento, obtener_evento, editar_evento, eliminar_evento
from menus import listar_menus, agregar_menu, obtener_menu, editar_menu, eliminar_menu, obtener_menus_mas_elegidos
from invitados import listar_invitados, agregar_invitado, obtener_invitado, editar_invitado, eliminar_invitado
from reportes import mostrar_reportes


class EatTogetherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EatTogether - Gestión de Eventos")
        self.root.geometry("1400x800")  # Ventana más grande
        self.root.configure(bg="#f0f0f0")

        # Validaciones
        self.validate_email = lambda email: re.match(r"[^@]+@[^@]+\.[^@]+", email)
        self.validate_date = lambda date_str: datetime.strptime(date_str, "%Y-%m-%d %H:%M")

        # Íconos (usar texto por simplicidad, o cargar imágenes)
        self.icon_add = "➕"
        self.icon_edit = "✏️"
        self.icon_delete = "🗑️"
        self.icon_eventos = "📅"
        self.icon_personas = "👥"
        self.icon_menus = "🍽️"
        self.icon_invitados = "🎉"
        self.icon_reportes = "📊"
        self.icon_backup = "💾"

        # Estilos - interfaz más grande
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=8)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 14))
        style.configure("Treeview.Heading", font=("Arial", 15, "bold"))

        # Sidebar
        self.sidebar = tk.Frame(root, bg="#2c3e50", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.sidebar_title = tk.Label(self.sidebar, text="Menú", bg="#2c3e50", fg="white", font=("Arial", 16, "bold"))
        self.sidebar_title.pack(pady=20)

        self.btn_inicio = ttk.Button(self.sidebar, text="🏠 Inicio", command=self.show_inicio)
        self.btn_inicio.pack(fill=tk.X, padx=10, pady=5)

        self.btn_eventos = ttk.Button(self.sidebar, text=f"{self.icon_eventos} Eventos", command=self.show_eventos)
        self.btn_eventos.pack(fill=tk.X, padx=10, pady=5)

        self.btn_personas = ttk.Button(self.sidebar, text=f"{self.icon_personas} Personas", command=self.show_personas)
        self.btn_personas.pack(fill=tk.X, padx=10, pady=5)

        self.btn_invitados = ttk.Button(self.sidebar, text=f"{self.icon_invitados} Invitados", command=self.show_invitados)
        self.btn_invitados.pack(fill=tk.X, padx=10, pady=5)

        self.btn_reportes = ttk.Button(self.sidebar, text=f"{self.icon_reportes} Reportes", command=self.show_reportes)
        self.btn_reportes.pack(fill=tk.X, padx=10, pady=5)

        self.btn_menus = ttk.Button(self.sidebar, text=f"{self.icon_menus} Menús", command=self.show_menus)
        self.btn_menus.pack(fill=tk.X, padx=10, pady=5)

        self.btn_backup = ttk.Button(self.sidebar, text=f"{self.icon_backup} Backup", command=self.backup_db)
        self.btn_backup.pack(fill=tk.X, padx=10, pady=5)

        # Área principal
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Inicializar vista
        self.show_inicio()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_inicio(self):
        self.clear_content()
        
        # Agregar header con fecha actual
        header = tk.Frame(self.content_frame, bg="#f0f0f0")
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header, text="EatTogether", font=("Arial", 32, "bold"), bg="#f0f0f0").pack(anchor="w")
        tk.Label(header, text="Resumen general de tu servicio de catering", font=("Arial", 14), fg="gray", bg="#f0f0f0").pack(anchor="w")
        
        # Tarjetas de estadísticas
        stats_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        stats_frame.pack(fill=tk.X, pady=20)
        
        eventos = self.get_eventos()
        personas = self.get_personas()
        menus = self.get_menus()
        invitados = self.get_invitados()
        
        # Tarjeta Eventos
        card_frame = tk.Frame(stats_frame, bg="white", relief=tk.RAISED, bd=1)
        card_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        tk.Label(card_frame, text="EVENTOS", font=("Arial", 10, "bold"), fg="gray", bg="white").pack(pady=5)
        evento_frame = tk.Frame(card_frame, bg="white")
        evento_frame.pack(pady=10)
        tk.Label(evento_frame, text="📅", font=("Arial", 24), bg="white").pack(side=tk.LEFT, padx=5)
        tk.Label(evento_frame, text=str(len(eventos)), font=("Arial", 20, "bold"), bg="white").pack(side=tk.LEFT, padx=10)
        
        # Tarjeta Personas
        card_frame = tk.Frame(stats_frame, bg="white", relief=tk.RAISED, bd=1)
        card_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        tk.Label(card_frame, text="PERSONAS", font=("Arial", 10, "bold"), fg="gray", bg="white").pack(pady=5)
        persona_frame = tk.Frame(card_frame, bg="white")
        persona_frame.pack(pady=10)
        tk.Label(persona_frame, text="👥", font=("Arial", 24), bg="white").pack(side=tk.LEFT, padx=5)
        tk.Label(persona_frame, text=str(len(personas)), font=("Arial", 20, "bold"), bg="white").pack(side=tk.LEFT, padx=10)
        
        # Tarjeta Menús
        card_frame = tk.Frame(stats_frame, bg="white", relief=tk.RAISED, bd=1)
        card_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        tk.Label(card_frame, text="MENÚS", font=("Arial", 10, "bold"), fg="gray", bg="white").pack(pady=5)
        menu_frame = tk.Frame(card_frame, bg="white")
        menu_frame.pack(pady=10)
        tk.Label(menu_frame, text="🍽️", font=("Arial", 24), bg="white").pack(side=tk.LEFT, padx=5)
        tk.Label(menu_frame, text=str(len(menus)), font=("Arial", 20, "bold"), bg="white").pack(side=tk.LEFT, padx=10)
        
        # Tarjeta Invitaciones
        card_frame = tk.Frame(stats_frame, bg="white", relief=tk.RAISED, bd=1)
        card_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        tk.Label(card_frame, text="INVITACIONES", font=("Arial", 10, "bold"), fg="gray", bg="white").pack(pady=5)
        invitado_frame = tk.Frame(card_frame, bg="white")
        invitado_frame.pack(pady=10)
        tk.Label(invitado_frame, text="🎉", font=("Arial", 24), bg="white").pack(side=tk.LEFT, padx=5)
        tk.Label(invitado_frame, text=str(len(invitados)), font=("Arial", 20, "bold"), bg="white").pack(side=tk.LEFT, padx=10)
        
        # Sección de menús más elegidos
        popular_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        popular_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        tk.Label(popular_frame, text="🍽️ Menús Más Elegidos", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(0, 10))
        
        # Crear treeview para mostrar los menús más elegidos
        tree_frame = tk.Frame(popular_frame, bg="white", relief=tk.RAISED, bd=1)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.popular_tree = ttk.Treeview(tree_frame, columns=("Menu", "Veces Elegido"), show="headings", height=10)
        self.popular_tree.heading("Menu", text="Menú")
        self.popular_tree.heading("Veces Elegido", text="Veces Elegido")
        self.popular_tree.column("Menu", width=400)
        self.popular_tree.column("Veces Elegido", width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.popular_tree.yview)
        self.popular_tree.configure(yscrollcommand=scrollbar.set)
        
        self.popular_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Llenar la lista con los menús más elegidos
        self.load_popular_menus()

    def load_popular_menus(self):
        """Carga los menús más elegidos en el treeview."""
        for item in self.popular_tree.get_children():
            self.popular_tree.delete(item)
        
        popular_menus = obtener_menus_mas_elegidos()
        for menu in popular_menus:
            self.popular_tree.insert("", tk.END, values=(menu['descripcion'], menu['veces_elegido']))

    def show_eventos(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Gestión de Eventos", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Barra de búsqueda
        search_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Buscar por nombre:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.eventos_search = tk.Entry(search_frame)
        self.eventos_search.pack(side=tk.LEFT, padx=5)
        self.eventos_search.bind("<KeyRelease>", self.filter_eventos)

        # Botones CRUD
        btn_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text=f"{self.icon_add} Agregar", command=self.add_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"{self.icon_edit} Editar", command=self.edit_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"{self.icon_delete} Eliminar", command=self.delete_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🍽️ Asignar Menús", command=self.asignar_menus_evento).pack(side=tk.LEFT, padx=5)

        # Treeview con scrollbar
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.eventos_tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Fecha/Hora", "Descripción"), show="headings")
        self.eventos_tree.heading("ID", text="ID")
        self.eventos_tree.heading("Nombre", text="Nombre")
        self.eventos_tree.heading("Fecha/Hora", text="Fecha/Hora")
        self.eventos_tree.heading("Descripción", text="Descripción")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.eventos_tree.yview)
        self.eventos_tree.configure(yscrollcommand=scrollbar.set)
        self.eventos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_eventos()

    def filter_eventos(self, event=None):
        query = self.eventos_search.get().lower()
        for item in self.eventos_tree.get_children():
            self.eventos_tree.delete(item)
        eventos = self.get_eventos()
        for e in eventos:
            if query in e['nombre'].lower():
                self.eventos_tree.insert("", tk.END, values=(e['id'], e['nombre'], e['fecha_hora'], e['descripcion']))

    def list_eventos(self):
        for item in self.eventos_tree.get_children():
            self.eventos_tree.delete(item)
        # Aquí usamos el módulo, pero adaptamos para GUI
        # Como listar_eventos imprime, necesitamos obtener datos
        # Modificamos para devolver lista
        # Por simplicidad, asumimos que modificamos los módulos para devolver datos en lugar de imprimir
        # Para este ejemplo, hardcodeo o uso una función auxiliar
        # En realidad, necesito modificar los módulos para que listar_* devuelvan listas
        # Para rapidez, creemos funciones auxiliares aquí
        eventos = self.get_eventos()
        for e in eventos:
            self.eventos_tree.insert("", tk.END, values=(e['id'], e['nombre'], e['fecha_hora'], e['descripcion']))

    def get_eventos(self):
        from db import obtener_conexion
        with obtener_conexion() as db:
            return db.execute("SELECT id, nombre, fecha_hora, descripcion FROM eventos").fetchall()

    def add_evento(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Evento")
        dialog.geometry("450x520")
        dialog.resizable(False, False)

        # Nombre
        tk.Label(dialog, text="Nombre del evento *").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        nombre_entry = tk.Entry(dialog, width=35)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        # Fecha
        tk.Label(dialog, text="Fecha *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        fecha_frame = tk.Frame(dialog)
        fecha_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(fecha_frame, text="Año:").grid(row=0, column=0)
        year_spin = tk.Spinbox(fecha_frame, from_=1900, to=2100, width=5)
        year_spin.grid(row=0, column=1)
        year_spin.delete(0, tk.END); year_spin.insert(0, "2026")

        tk.Label(fecha_frame, text="Mes:").grid(row=0, column=2)
        month_spin = tk.Spinbox(fecha_frame, from_=1, to=12, width=3)
        month_spin.grid(row=0, column=3)
        month_spin.delete(0, tk.END); month_spin.insert(0, "1")

        tk.Label(fecha_frame, text="Día:").grid(row=0, column=4)
        day_spin = tk.Spinbox(fecha_frame, from_=1, to=31, width=3)
        day_spin.grid(row=0, column=5)
        day_spin.delete(0, tk.END); day_spin.insert(0, "1")

        # Estado
        tk.Label(dialog, text="Estado *").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        estado_var = tk.StringVar(dialog)
        estado_var.set("Planificación")
        estado_menu = tk.OptionMenu(dialog, estado_var, "Planificación", "Confirmado", "Completado", "Cancelado")
        estado_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Hora
        tk.Label(dialog, text="Hora *").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
        hora_var = tk.StringVar(dialog)
        hora_var.set("12:00")
        hora_menu = tk.OptionMenu(dialog, hora_var, *horas)
        hora_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Lugar
        tk.Label(dialog, text="Lugar *").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        lugar_entry = tk.Entry(dialog, width=35)
        lugar_entry.grid(row=4, column=1, padx=10, pady=5)

        # Descripción
        tk.Label(dialog, text="Descripción *").grid(row=5, column=0, padx=10, pady=5, sticky="nw")
        desc_text = tk.Text(dialog, width=35, height=4)
        desc_text.grid(row=5, column=1, padx=10, pady=5)

        def on_ok():
            nombre = nombre_entry.get().strip()
            if not nombre or len(nombre) > 100:
                messagebox.showerror("Error", "Nombre inválido.")
                return
            try:
                year = int(year_spin.get())
                month = int(month_spin.get())
                day = int(day_spin.get())
                fecha_str = f"{year:04d}-{month:02d}-{day:02d}"
                datetime.strptime(fecha_str, "%Y-%m-%d")
            except:
                messagebox.showerror("Error", "Fecha inválida.")
                return
            hora = hora_var.get()
            fecha_hora = f"{fecha_str} {hora}"
            estado = estado_var.get()
            lugar = lugar_entry.get().strip()
            if not lugar:
                messagebox.showerror("Error", "Lugar es requerido.")
                return
            descripcion = desc_text.get("1.0", tk.END).strip()
            if not descripcion or len(descripcion) > 500:
                messagebox.showerror("Error", "Descripción inválida (máx 500 chars).")
                return
            agregar_evento(nombre, fecha_hora, descripcion, lugar, estado)
            messagebox.showinfo("Éxito", "Evento agregado.")
            self.list_eventos()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Guardar", command=on_ok, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=on_cancel, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def edit_evento(self):
        selected = self.eventos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un evento.")
            return

        item = self.eventos_tree.item(selected)
        ide = item['values'][0]
        evento = obtener_evento(ide)
        if not evento:
            messagebox.showerror("Error", "Evento no encontrado.")
            return

        # Convertir sqlite3.Row a diccionario para evitar .get() fallando
        try:
            evento = dict(evento)
        except Exception:
            pass

        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Evento")
        dialog.geometry("450x520")
        dialog.resizable(False, False)

        # Nombre
        tk.Label(dialog, text="Nombre del evento *").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        nombre_entry = tk.Entry(dialog, width=35)
        nombre_entry.insert(0, evento.get('nombre', ''))
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        # Fecha
        tk.Label(dialog, text="Fecha *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        fecha_frame = tk.Frame(dialog)
        fecha_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(fecha_frame, text="Año:").grid(row=0, column=0)
        year_spin = tk.Spinbox(fecha_frame, from_=1900, to=2100, width=5)
        year_spin.grid(row=0, column=1)

        tk.Label(fecha_frame, text="Mes:").grid(row=0, column=2)
        month_spin = tk.Spinbox(fecha_frame, from_=1, to=12, width=3)
        month_spin.grid(row=0, column=3)

        tk.Label(fecha_frame, text="Día:").grid(row=0, column=4)
        day_spin = tk.Spinbox(fecha_frame, from_=1, to=31, width=3)
        day_spin.grid(row=0, column=5)

        try:
            dt = datetime.strptime(evento.get('fecha_hora', ''), "%Y-%m-%d %H:%M")
            year_spin.delete(0, tk.END); year_spin.insert(0, str(dt.year))
            month_spin.delete(0, tk.END); month_spin.insert(0, str(dt.month))
            day_spin.delete(0, tk.END); day_spin.insert(0, str(dt.day))
        except Exception:
            year_spin.delete(0, tk.END); year_spin.insert(0, "2026")
            month_spin.delete(0, tk.END); month_spin.insert(0, "1")
            day_spin.delete(0, tk.END); day_spin.insert(0, "1")

        # Estado
        tk.Label(dialog, text="Estado *").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        estado_var = tk.StringVar(dialog)
        estado_var.set(evento.get('estado', 'Planificación'))
        estado_menu = tk.OptionMenu(dialog, estado_var, "Planificación", "Confirmado", "Completado", "Cancelado")
        estado_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Hora
        tk.Label(dialog, text="Hora *").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
        hora_var = tk.StringVar(dialog)
        try:
            dt = datetime.strptime(evento.get('fecha_hora', ''), "%Y-%m-%d %H:%M")
            hora_var.set(f"{dt.hour:02d}:{dt.minute:02d}")
        except Exception:
            hora_var.set("12:00")
        hora_menu = tk.OptionMenu(dialog, hora_var, *horas)
        hora_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Lugar
        tk.Label(dialog, text="Lugar *").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        lugar_entry = tk.Entry(dialog, width=35)
        lugar_entry.insert(0, evento.get('lugar', ''))
        lugar_entry.grid(row=4, column=1, padx=10, pady=5)

        # Descripción
        tk.Label(dialog, text="Descripción *").grid(row=5, column=0, padx=10, pady=5, sticky="nw")
        desc_text = tk.Text(dialog, width=35, height=4)
        desc_text.insert("1.0", evento.get('descripcion', ''))
        desc_text.grid(row=5, column=1, padx=10, pady=5)

        def on_ok():
            nombre = nombre_entry.get().strip()
            if not nombre or len(nombre) > 100:
                messagebox.showerror("Error", "Nombre inválido.")
                return
            try:
                year = int(year_spin.get())
                month = int(month_spin.get())
                day = int(day_spin.get())
                fecha_str = f"{year:04d}-{month:02d}-{day:02d}"
                datetime.strptime(fecha_str, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Error", "Fecha inválida.")
                return
            hora = hora_var.get()
            fecha_hora = f"{fecha_str} {hora}"
            estado = estado_var.get()
            lugar = lugar_entry.get().strip()
            if not lugar:
                messagebox.showerror("Error", "Lugar es requerido.")
                return
            descripcion = desc_text.get("1.0", tk.END).strip()
            if not descripcion or len(descripcion) > 500:
                messagebox.showerror("Error", "Descripción inválida (máx 500 chars).")
                return
            editar_evento(ide, nombre, fecha_hora, descripcion, lugar, estado)
            messagebox.showinfo("Éxito", "Evento actualizado.")
            self.list_eventos()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Guardar", command=on_ok, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=on_cancel, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def delete_evento(self):
        if getattr(self, '_is_deleting_evento', False):
            return
        self._is_deleting_evento = True
        try:
            selected = self.eventos_tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Selecciona un evento.")
                return
            # Evitamos que el cierre del messagebox con Enter vuelva a disparar el botón
            self.root.focus()
            if messagebox.askyesno("Confirmar", "¿Eliminar evento?"):
                item = self.eventos_tree.item(selected)
                ide = item['values'][0]
                eliminar_evento(ide)
                messagebox.showinfo("Éxito", "Evento eliminado.")
                self.list_eventos()
        finally:
            self._is_deleting_evento = False

    def asignar_menus_evento(self):
        """Permite asignar múltiples menús a un evento seleccionado."""
        selected = self.eventos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un evento.")
            return
        
        item = self.eventos_tree.item(selected)
        ide = item['values'][0]
        evento = obtener_evento(ide)
        
        if not evento:
            messagebox.showerror("Error", "Evento no encontrado.")
            return
        
        # Crear diálogo para seleccionar menús
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Asignar Menús - {evento['nombre']}")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text=f"Menús disponibles para: {evento['nombre']}", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame con checkbuttons para menús
        frame_menus = tk.Frame(dialog)
        frame_menus.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_menus)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas = tk.Canvas(frame_menus, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)
        
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        # Obtener menús
        menus = self.get_menus()
        from menus import obtener_menus_evento
        menus_evento = obtener_menus_evento(ide)
        menu_ids_evento = {m['id'] for m in menus_evento}
        
        # Variables para checkbuttons
        check_vars = {}
        for m in menus:
            var = tk.BooleanVar(value=(m['id'] in menu_ids_evento))
            check_vars[m['id']] = var
            
            texto = f"{m['descripcion']} - ${m['precio']}"
            tk.Checkbutton(inner_frame, text=texto, variable=var).pack(anchor="w", padx=10, pady=5)
        
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Botones
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def guardar():
            from menus import asignar_menu_evento, desasignar_menu_evento
            
            # Desasignar menús no seleccionados
            for m_id in menu_ids_evento:
                if not check_vars[m_id].get():
                    desasignar_menu_evento(ide, m_id)
            
            # Asignar menús seleccionados
            for m_id, var in check_vars.items():
                if var.get() and m_id not in menu_ids_evento:
                    asignar_menu_evento(ide, m_id)
            
            messagebox.showinfo("Éxito", "Menús asignados correctamente.")
            dialog.destroy()
            # Actualizar lista de menús populares si estamos en la vista de inicio
            try:
                if hasattr(self, 'popular_tree') and self.popular_tree.winfo_exists():
                    self.load_popular_menus()
            except:
                pass  # Ignorar si no estamos en la vista correcta
        
        tk.Button(btn_frame, text="Guardar Asignaciones", command=guardar, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

    # Similar para personas, menus, invitados, reportes
    # Por brevedad, implemento solo eventos aquí, pero el patrón es el mismo

    def show_personas(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Gestión de Personas", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Barra de búsqueda
        search_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Buscar por nombre:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.personas_search = tk.Entry(search_frame)
        self.personas_search.pack(side=tk.LEFT, padx=5)
        self.personas_search.bind("<KeyRelease>", self.filter_personas)

        btn_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text=f"{self.icon_add} Agregar", command=self.add_persona).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"{self.icon_edit} Editar", command=self.edit_persona).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"{self.icon_delete} Eliminar", command=self.delete_persona).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.personas_tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Email", "Teléfono"), show="headings")
        self.personas_tree.heading("ID", text="ID")
        self.personas_tree.heading("Nombre", text="Nombre")
        self.personas_tree.heading("Email", text="Email")
        self.personas_tree.heading("Teléfono", text="Teléfono")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.personas_tree.yview)
        self.personas_tree.configure(yscrollcommand=scrollbar.set)
        self.personas_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_personas()

    def filter_personas(self, event=None):
        query = self.personas_search.get().lower()
        for item in self.personas_tree.get_children():
            self.personas_tree.delete(item)
        personas = self.get_personas()
        for p in personas:
            if query in p['nombre'].lower():
                self.personas_tree.insert("", tk.END, values=(p['id'], p['nombre'], p['email'], p['telefono']))

    def list_personas(self):
        for item in self.personas_tree.get_children():
            self.personas_tree.delete(item)
        personas = self.get_personas()
        for p in personas:
            self.personas_tree.insert("", tk.END, values=(p['id'], p['nombre'], p['email'], p['telefono']))

    def get_personas(self):
        from db import obtener_conexion
        with obtener_conexion() as db:
            return db.execute("SELECT id, nombre, email, telefono FROM personas").fetchall()

    def add_persona(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nueva Persona")
        dialog.geometry("400x450")
        dialog.resizable(False, False)

        # Nombre
        tk.Label(dialog, text="Nombre *").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        nombre_entry = tk.Entry(dialog, width=30)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        # Email
        tk.Label(dialog, text="Email *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        email_entry = tk.Entry(dialog, width=30)
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        # Teléfono
        tk.Label(dialog, text="Teléfono *").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        telefono_entry = tk.Entry(dialog, width=30)
        telefono_entry.grid(row=2, column=1, padx=10, pady=5)

        # Notas
        tk.Label(dialog, text="Notas").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        notas_text = tk.Text(dialog, width=30, height=5)
        notas_text.grid(row=3, column=1, padx=10, pady=5)

        def on_ok():
            nombre = nombre_entry.get().strip()
            email = email_entry.get().strip()
            telefono = telefono_entry.get().strip()
            notas = notas_text.get("1.0", tk.END).strip()
            
            if not nombre or len(nombre) > 100:
                messagebox.showerror("Error", "Nombre inválido (máx 100 chars).")
                return
            if not email or not self.validate_email(email):
                messagebox.showerror("Error", "Email inválido.")
                return
            if not telefono or len(telefono) > 20:
                messagebox.showerror("Error", "Teléfono inválido (máx 20 chars).")
                return
            
            try:
                agregar_persona(nombre, email, telefono, notas)
                messagebox.showinfo("Éxito", "Persona agregada.")
                self.list_personas()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar: {str(e)}")

        def on_cancel():
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Guardar", command=on_ok, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=on_cancel, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def edit_persona(self):
        selected = self.personas_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una persona.")
            return
        item = self.personas_tree.item(selected)
        idp = item['values'][0]
        persona = obtener_persona(idp)

        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Persona")
        dialog.geometry("400x450")
        dialog.resizable(False, False)

        # Nombre
        tk.Label(dialog, text="Nombre *").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        nombre_entry = tk.Entry(dialog, width=30)
        nombre_entry.insert(0, persona['nombre'])
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        # Email
        tk.Label(dialog, text="Email *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        email_entry = tk.Entry(dialog, width=30)
        email_entry.insert(0, persona['email'])
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        # Teléfono
        tk.Label(dialog, text="Teléfono *").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        telefono_entry = tk.Entry(dialog, width=30)
        telefono_entry.insert(0, persona['telefono'])
        telefono_entry.grid(row=2, column=1, padx=10, pady=5)

        # Notas
        tk.Label(dialog, text="Notas").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        notas_text = tk.Text(dialog, width=30, height=5)
        if persona['notas']:
            notas_text.insert("1.0", persona['notas'])
        notas_text.grid(row=3, column=1, padx=10, pady=5)

        def on_ok():
            nombre = nombre_entry.get().strip()
            email = email_entry.get().strip()
            telefono = telefono_entry.get().strip()
            notas = notas_text.get("1.0", tk.END).strip()
            
            if not nombre or len(nombre) > 100:
                messagebox.showerror("Error", "Nombre inválido.")
                return
            if not email or not self.validate_email(email):
                messagebox.showerror("Error", "Email inválido.")
                return
            if not telefono or len(telefono) > 20:
                messagebox.showerror("Error", "Teléfono inválido.")
                return
            
            try:
                editar_persona(idp, nombre, email, telefono, notas)
                messagebox.showinfo("Éxito", "Persona actualizada.")
                self.list_personas()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {str(e)}")

        def on_cancel():
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Guardar", command=on_ok, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=on_cancel, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def delete_persona(self):
        selected = self.personas_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una persona.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar persona?"):
            item = self.personas_tree.item(selected)
            idp = item['values'][0]
            eliminar_persona(idp)
            messagebox.showinfo("Éxito", "Persona eliminada.")
            self.list_personas()

    def show_invitados(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Gestión de Invitados", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Barra de búsqueda
        search_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Buscar por persona:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.invitados_search = tk.Entry(search_frame)
        self.invitados_search.pack(side=tk.LEFT, padx=5)
        self.invitados_search.bind("<KeyRelease>", self.filter_invitados)

        btn_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="➕ Agregar", command=self.add_invitado).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✏️ Editar", command=self.edit_invitado).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.delete_invitado).pack(side=tk.LEFT, padx=5)

        # Treeview con scrollbar
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.invitados_tree = ttk.Treeview(tree_frame, columns=("ID", "Persona", "Evento", "Menú"), show="headings")
        self.invitados_tree.heading("ID", text="ID")
        self.invitados_tree.heading("Persona", text="Persona")
        self.invitados_tree.heading("Evento", text="Evento")
        self.invitados_tree.heading("Menú", text="Menú")
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.invitados_tree.yview)
        self.invitados_tree.configure(yscrollcommand=scrollbar.set)
        self.invitados_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_invitados()

    def list_invitados(self):
        for item in self.invitados_tree.get_children():
            self.invitados_tree.delete(item)
        invitados = self.get_invitados()
        for inv in invitados:
            persona = obtener_persona(inv['persona_id'])
            evento = obtener_evento(inv['evento_id'])
            menu = obtener_menu(inv['menu_id'])
            pnombre = persona['nombre'] if persona else "[eliminada]"
            enombre = evento['nombre'] if evento else "[eliminado]"
            mdesc = menu['descripcion'] if menu else "[eliminado]"
            self.invitados_tree.insert("", tk.END, values=(inv['id'], pnombre, enombre, mdesc))

    def filter_invitados(self, event=None):
        query = self.invitados_search.get().lower()
        for item in self.invitados_tree.get_children():
            self.invitados_tree.delete(item)
        invitados = self.get_invitados()
        for inv in invitados:
            persona = obtener_persona(inv['persona_id'])
            evento = obtener_evento(inv['evento_id'])
            menu = obtener_menu(inv['menu_id'])
            pnombre = persona['nombre'] if persona else "[eliminada]"
            enombre = evento['nombre'] if evento else "[eliminado]"
            mdesc = menu['descripcion'] if menu else "[eliminado]"
            if query in pnombre.lower():
                self.invitados_tree.insert("", tk.END, values=(inv['id'], pnombre, enombre, mdesc))

    def get_invitados(self):
        from db import obtener_conexion
        with obtener_conexion() as db:
            return db.execute("SELECT id, persona_id, evento_id, menu_id FROM invitados").fetchall()

    def add_invitado(self):
        personas = self.get_personas()
        if not personas:
            messagebox.showwarning("Advertencia", "No hay personas disponibles.")
            return
        persona_options = [f"{p['id']}: {p['nombre']}" for p in personas]
        persona_str = simpledialog.askstring("Agregar Invitado", f"Selecciona persona:\n" + "\n".join(persona_options))
        if not persona_str: return
        try:
            idp = int(persona_str.split(":")[0])
        except:
            return

        eventos = self.get_eventos()
        if not eventos:
            messagebox.showwarning("Advertencia", "No hay eventos disponibles.")
            return
        evento_options = [f"{e['id']}: {e['nombre']}" for e in eventos]
        evento_str = simpledialog.askstring("Agregar Invitado", f"Selecciona evento:\n" + "\n".join(evento_options))
        if not evento_str: return
        try:
            ide = int(evento_str.split(":")[0])
        except:
            return

        menus = self.get_menus_for_evento(ide)
        if not menus:
            messagebox.showwarning("Advertencia", "No hay menús para este evento.")
            return
        menu_options = [f"{m['id']}: {m['descripcion']}" for m in menus]
        menu_str = simpledialog.askstring("Agregar Invitado", f"Selecciona menú:\n" + "\n".join(menu_options))
        if not menu_str: return
        try:
            idm = int(menu_str.split(":")[0])
        except:
            return

        agregar_invitado(idp, ide, idm)
        messagebox.showinfo("Éxito", "Invitado agregado.")
        self.list_invitados()

    def get_menus_for_evento(self, ide):
        from menus import obtener_menus_evento
        return obtener_menus_evento(ide)

    def edit_invitado(self):
        selected = self.invitados_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un invitado.")
            return
        item = self.invitados_tree.item(selected)
        idi = item['values'][0]
        inv = obtener_invitado(idi)
        menus = self.get_menus_for_evento(inv['evento_id'])
        if not menus:
            messagebox.showwarning("Advertencia", "No hay menús disponibles.")
            return
        menu_options = [f"{m['id']}: {m['descripcion']}" for m in menus]
        menu_str = simpledialog.askstring("Editar Invitado", f"Selecciona nuevo menú:\n" + "\n".join(menu_options))
        if not menu_str: return
        try:
            idm = int(menu_str.split(":")[0])
        except:
            return
        editar_invitado(idi, idm)
        messagebox.showinfo("Éxito", "Invitado actualizado.")
        self.list_invitados()

    def delete_invitado(self):
        selected = self.invitados_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un invitado.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar invitado?"):
            item = self.invitados_tree.item(selected)
            idi = item['values'][0]
            eliminar_invitado(idi)
            messagebox.showinfo("Éxito", "Invitado eliminado.")
            self.list_invitados()

    def show_reportes(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Reportes", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        btn_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="📊 Generar Reporte", command=self.generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📄 Exportar TXT", command=self.export_txt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📄 Exportar PDF", command=self.export_pdf).pack(side=tk.LEFT, padx=5)

        # Text con scrollbar
        text_frame = tk.Frame(self.content_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        self.report_text = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.generate_report()

    def generate_report(self):
        self.report_text.delete(1.0, tk.END)
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        mostrar_reportes()
        sys.stdout = old_stdout
        self.report_text.insert(tk.END, buffer.getvalue())

    def export_txt(self):
        content = self.report_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Advertencia", "No hay contenido para exportar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Éxito", f"Reporte exportado a {file_path}")

    def export_pdf(self):
        content = self.report_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Advertencia", "No hay contenido para exportar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            for line in content.split('\n'):
                if line.strip():
                    p = Paragraph(line, styles['Normal'])
                    story.append(p)
                else:
                    story.append(Spacer(1, 12))
            doc.build(story)
            messagebox.showinfo("Éxito", f"Reporte exportado a {file_path}")

    def backup_db(self):
        import shutil
        file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database files", "*.db")])
        if file_path:
            shutil.copy("eatogether.db", file_path)
            messagebox.showinfo("Éxito", f"Backup creado en {file_path}")

    def show_menus(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Gestión de Menús", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Barra de búsqueda
        search_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Buscar por descripción:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.menus_search = tk.Entry(search_frame)
        self.menus_search.pack(side=tk.LEFT, padx=5)
        self.menus_search.bind("<KeyRelease>", self.filter_menus)

        btn_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text=f"{self.icon_add} Agregar", command=self.add_menu).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"{self.icon_edit} Editar", command=self.edit_menu).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"{self.icon_delete} Eliminar", command=self.delete_menu).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.menus_tree = ttk.Treeview(tree_frame, columns=("ID", "Descripción", "Ingredientes", "Precio"), show="headings")
        self.menus_tree.heading("ID", text="ID")
        self.menus_tree.heading("Descripción", text="Descripción")
        self.menus_tree.heading("Ingredientes", text="Ingredientes")
        self.menus_tree.heading("Precio", text="Precio")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.menus_tree.yview)
        self.menus_tree.configure(yscrollcommand=scrollbar.set)
        self.menus_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_menus()

    def filter_menus(self, event=None):
        query = self.menus_search.get().lower()
        for item in self.menus_tree.get_children():
            self.menus_tree.delete(item)
        menus = self.get_menus()
        for m in menus:
            if query in m['descripcion'].lower():
                self.menus_tree.insert("", tk.END, values=(m['id'], m['descripcion'], m['ingredientes'], m['precio']))

    def list_menus(self):
        for item in self.menus_tree.get_children():
            self.menus_tree.delete(item)
        menus = self.get_menus()
        for m in menus:
            self.menus_tree.insert("", tk.END, values=(m['id'], m['descripcion'], m['ingredientes'], m['precio']))

    def get_menus(self):
        from db import obtener_conexion
        with obtener_conexion() as db:
            return db.execute("SELECT id, descripcion, ingredientes, precio FROM menus").fetchall()

    def add_menu(self):
        # Crear ventana de diálogo personalizada
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Menú")
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        # Descripción
        tk.Label(dialog, text="Descripción *").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        descripcion_entry = tk.Entry(dialog, width=35)
        descripcion_entry.grid(row=0, column=1, padx=10, pady=5)

        # Ingredientes
        tk.Label(dialog, text="Ingredientes *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ingredientes_text = tk.Text(dialog, width=35, height=5)
        ingredientes_text.grid(row=1, column=1, padx=10, pady=5)

        # Precio
        tk.Label(dialog, text="Precio por persona *").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        precio_entry = tk.Entry(dialog, width=35)
        precio_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botones
        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=15)
        
        def guardar():
            descripcion = descripcion_entry.get()
            ingredientes = ingredientes_text.get("1.0", tk.END).strip()
            precio = precio_entry.get()
            
            if not descripcion or not ingredientes or not precio:
                messagebox.showwarning("Advertencia", "Completa todos los campos.")
                return
            
            from menus import agregar_menu
            agregar_menu(descripcion, ingredientes, precio)
            messagebox.showinfo("Éxito", "Menú agregado.")
            dialog.destroy()
            self.list_menus()
            # Actualizar lista de menús populares si estamos en la vista de inicio
            try:
                if hasattr(self, 'popular_tree') and self.popular_tree.winfo_exists():
                    self.load_popular_menus()
            except:
                pass  # Ignorar si no estamos en la vista correcta
        
        tk.Button(btn_frame, text="Guardar", command=guardar, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

    def edit_menu(self):
        selected = self.menus_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un menú.")
            return
        item = self.menus_tree.item(selected)
        idm = item['values'][0]
        menu = obtener_menu(idm)
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Menú")
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        # Descripción
        tk.Label(dialog, text="Descripción *").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        descripcion_entry = tk.Entry(dialog, width=35)
        descripcion_entry.insert(0, menu['descripcion'])
        descripcion_entry.grid(row=0, column=1, padx=10, pady=5)

        # Ingredientes
        tk.Label(dialog, text="Ingredientes *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ingredientes_text = tk.Text(dialog, width=35, height=5)
        ingredientes_text.insert("1.0", menu['ingredientes'])
        ingredientes_text.grid(row=1, column=1, padx=10, pady=5)

        # Precio
        tk.Label(dialog, text="Precio por persona *").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        precio_entry = tk.Entry(dialog, width=35)
        precio_entry.insert(0, menu['precio'])
        precio_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botones
        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=15)
        
        def guardar():
            descripcion = descripcion_entry.get()
            ingredientes = ingredientes_text.get("1.0", tk.END).strip()
            precio = precio_entry.get()
            
            if not descripcion or not ingredientes or not precio:
                messagebox.showwarning("Advertencia", "Completa todos los campos.")
                return
            
            from menus import editar_menu
            editar_menu(idm, descripcion, ingredientes, precio)
            messagebox.showinfo("Éxito", "Menú actualizado.")
            dialog.destroy()
            self.list_menus()
            # Actualizar lista de menús populares si estamos en la vista de inicio
            try:
                if hasattr(self, 'popular_tree') and self.popular_tree.winfo_exists():
                    self.load_popular_menus()
            except:
                pass  # Ignorar si no estamos en la vista correcta
        
        tk.Button(btn_frame, text="Actualizar", command=guardar, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg="white", fg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

    def delete_menu(self):
        selected = self.menus_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un menú.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar menú?"):
            item = self.menus_tree.item(selected)
            idm = item['values'][0]
            eliminar_menu(idm)
            messagebox.showinfo("Éxito", "Menú eliminado.")
            self.list_menus()
            # Actualizar lista de menús populares si estamos en la vista de inicio
            try:
                if hasattr(self, 'popular_tree') and self.popular_tree.winfo_exists():
                    self.load_popular_menus()
            except:
                pass  # Ignorar si no estamos en la vista correcta


if __name__ == "__main__":
    inicializar_bd()
    root = tk.Tk()
    app = EatTogetherApp(root)
    root.mainloop()