def edit_event(self):
        # 1. Obtener el evento seleccionado en la tabla
        selected = self.events_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un evento para editar.")
            return

        item = self.events_tree.item(selected)
        ide = item['values'][0]
        evento = obtener_evento(ide)

        if not evento:
            messagebox.showerror("Error", "No se pudieron obtener los datos del evento.")
            return

        # 2. Crear la ventana emergente
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Evento")
        dialog.geometry("500x500")
        dialog.configure(bg="#f0f0f0")
        dialog.transient(self.root)
        dialog.grab_set()

        form_frame = tk.Frame(dialog, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # 3. Dibujar todos los campos usando las claves correctas de la base de datos
        # Nombre
        tk.Label(form_frame, text="Nombre:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        nombre_var = tk.StringVar(value=evento['nombre'])
        tk.Entry(form_frame, textvariable=nombre_var, font=("Arial", 10), width=30).grid(row=0, column=1, pady=5)

        # Fecha y Hora (¡Aquí suele estar el error de clave 'fecha_hora'!)
        tk.Label(form_frame, text="Fecha y Hora (YYYY-MM-DD HH:MM):", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        fecha_var = tk.StringVar(value=evento['fecha_hora'])
        tk.Entry(form_frame, textvariable=fecha_var, font=("Arial", 10), width=30).grid(row=1, column=1, pady=5)

        # Descripción
        tk.Label(form_frame, text="Descripción:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        desc_var = tk.StringVar(value=evento['descripcion'])
        tk.Entry(form_frame, textvariable=desc_var, font=("Arial", 10), width=30).grid(row=2, column=1, pady=5)

        # Lugar
        tk.Label(form_frame, text="Lugar:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        lugar_var = tk.StringVar(value=evento['lugar'])
        tk.Entry(form_frame, textvariable=lugar_var, font=("Arial", 10), width=30).grid(row=3, column=1, pady=5)

        # Estado
        tk.Label(form_frame, text="Estado:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        estado_var = tk.StringVar(value=evento['estado'])
        estados = ["Planificación", "Confirmado", "Realizado", "Cancelado"]
        estado_cb = ttk.Combobox(form_frame, textvariable=estado_var, values=estados, state="readonly", font=("Arial", 10), width=28)
        estado_cb.grid(row=4, column=1, pady=5)

        # 4. Función interna para guardar los cambios
        def guardar():
            nombre = nombre_var.get().strip()
            fecha = fecha_var.get().strip()
            desc = desc_var.get().strip()
            lugar = lugar_var.get().strip()
            estado = estado_var.get().strip()

            if not nombre or not fecha or not desc:
                messagebox.showerror("Error", "Nombre, Fecha y Descripción son obligatorios.", parent=dialog)
                return
            
            try:
                self.validate_date(fecha) # Valida el formato de la fecha
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD HH:MM", parent=dialog)
                return

            editar_evento(ide, nombre, fecha, desc, lugar, estado)
            messagebox.showinfo("Éxito", "Evento actualizado exitosamente.", parent=dialog)
            dialog.destroy()
            self.list_events() # Actualiza la tabla principal

        # 5. Dibujar los botones
        btn_frame = tk.Frame(dialog, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Guardar", command=guardar, bg="white", fg="black", font=("Arial", 12, "bold"), width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg="white", fg="black", font=("Arial", 12, "bold"), width=10).pack(side=tk.LEFT, padx=10)