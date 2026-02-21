import customtkinter as ctk
from tkinter import ttk, messagebox
from biblioteca_personal import BibliotecaPersonal
from libro import Libro


class SistemaGestion(ctk.CTk):
    """Ventana principal del sistema de gestion"""

    def __init__(self) -> None:
        super().__init__()
        self.title("Sistema de Gestión de Biblioteca")
        self.geometry("1300x700")
        ctk.set_appearance_mode("dark")

        self.biblioteca = BibliotecaPersonal()

    # =====================================================
    # Metodo del menu principal
    # =====================================================
    def menu_principal(self) -> None:
        """Construye toda la interfaz grafica"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------- LADO IZQUIERDO: REGISTRO DE LIBROS ----------
        self.sidebar = ctk.CTkFrame(self, width=500, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            self.sidebar,
            text="GESTIÓN DE LIBROS",
            font=("Roboto", 20, "bold"),
        ).pack(pady=20, padx=20)

        # Campos de entrada
        self.ent_isbn = ctk.CTkEntry(self.sidebar, placeholder_text="ISBN")
        self.ent_isbn.pack(fill="x", padx=20, pady=5)

        self.ent_titulo = ctk.CTkEntry(self.sidebar, placeholder_text="Título")
        self.ent_titulo.pack(fill="x", padx=20, pady=5)

        self.ent_autor = ctk.CTkEntry(self.sidebar, placeholder_text="Autor")
        self.ent_autor.pack(fill="x", padx=20, pady=5)

        self.ent_anio = ctk.CTkEntry(self.sidebar, placeholder_text="Año")
        self.ent_anio.pack(fill="x", padx=20, pady=5)

        self.ent_cat = ctk.CTkEntry(self.sidebar, placeholder_text="Categoría")
        self.ent_cat.pack(fill="x", padx=20, pady=5)

        # Selector de insercion
        ctk.CTkLabel(
            self.sidebar,
            text="Método de Inserción:",
            font=("Roboto", 12),
        ).pack(pady=(10, 0))

        self.cbo_insercion = ctk.CTkComboBox(
            self.sidebar,
            values=["Al Final", "Al Inicio", "Ordenado (Título)"],
        )
        self.cbo_insercion.set("Al Final")
        self.cbo_insercion.pack(fill="x", padx=20, pady=5)

        # Botones del CRUD
        ctk.CTkButton(
            self.sidebar,
            text="Agregar Libro",
            command=self.agregar_libro,
        ).pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkButton(
            self.sidebar,
            text="Actualizar Seleccionado",
            command=self.actualizar_libro,
        ).pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            self.sidebar,
            text="Eliminar Seleccionado",
            fg_color="#c0392b",
            command=self.eliminar_libro,
        ).pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            self.sidebar,
            text="Limpiar Campos",
            fg_color="#34495e",
            command=self.limpiar_campos,
        ).pack(fill="x", padx=20, pady=10)

        # ---------- LADO DERECHO ----------
        self.main_view = ctk.CTkFrame(self)
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Seccion de busqueda
        self.search_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.cbo_criterio = ctk.CTkComboBox(
            self.search_frame,
            values=["ISBN", "Autor", "Categoría"],
            width=120,
        )
        self.cbo_criterio.set("ISBN")
        self.cbo_criterio.pack(side="left", padx=5)

        self.ent_buscar = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Término a buscar...",
            width=200,
        )
        self.ent_buscar.pack(side="left", padx=5)

        ctk.CTkButton(
            self.search_frame,
            text="Buscar",
            width=80,
            command=self.buscar_libro,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.search_frame,
            text="Ver Todos",
            width=80,
            fg_color="#555",
            command=self.consultar_libros,
        ).pack(side="left")

        self.switch_inverso = ctk.CTkSwitch(
            self.search_frame,
            text="Orden inverso",
            command=self.consultar_libros,
        )
        self.switch_inverso.pack(side="right", padx=10)

        # Tabla de libros
        self.tree = ttk.Treeview(
            self.main_view,
            columns=("isbn", "titulo", "autor", "anio", "cat"),
            show="headings",
        )

        for col, txt in [
            ("isbn", "ISBN"),
            ("titulo", "Título"),
            ("autor", "Autor"),
            ("anio", "Año"),
            ("cat", "Categoría"),
        ]:
            self.tree.heading(col, text=txt)

        self.tree.pack(expand=True, fill="both", padx=20, pady=20)
        self.tree.bind("<<TreeviewSelect>>", self.rellenar_campos)

    # =====================================================
    # CRUD
    # =====================================================
    def agregar_libro(self) -> None:
        """Agrega un libro a la biblioteca"""
        try:
            libro = Libro(
                self.ent_titulo.get(),
                self.ent_autor.get(),
                self.ent_anio.get(),
                self.ent_isbn.get(),
                self.ent_cat.get(),
            )

            metodo = self.cbo_insercion.get()

            if metodo == "Al Inicio":
                self.biblioteca.insertar_al_inicio(libro)
            elif metodo == "Ordenado (Título)":
                self.biblioteca.insertar_ordenado(libro)
            else:
                self.biblioteca.insertar_al_final(libro)

            self.consultar_libros()
            self.limpiar_campos()

        except ValueError as e:
            messagebox.showerror("Error de Datos", str(e))

    def consultar_libros(self) -> None:
        """Muestra todos los libros en la tabla"""
        self.tree.delete(*self.tree.get_children())

        libros = (
            self.biblioteca.mostrar_todos_inverso()
            if self.switch_inverso.get()
            else list(self.biblioteca)
        )

        self.llenar_tabla(libros)

    def buscar_libro(self) -> None:
        """Busca libros segun el criterio seleccionado"""
        termino = self.ent_buscar.get().strip()
        criterio = self.cbo_criterio.get()

        if not termino:
            return

        try:
            if criterio == "ISBN":
                res = self.biblioteca.buscar_por_isbn(termino)
                libros = [res] if res else []
            elif criterio == "Autor":
                libros = self.biblioteca.buscar_por_autor(termino)
            else:
                libros = self.biblioteca.buscar_por_categoria(termino)

            self.tree.delete(*self.tree.get_children())

            if libros:
                self.llenar_tabla(libros)
            else:
                messagebox.showinfo("Búsqueda", f"No hay resultados para: {termino}")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_libro(self) -> None:
        """Actualiza el libro seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un libro de la tabla.")
            return

        isbn = str(self.tree.item(seleccion[0])["values"][0])

        try:
            self.biblioteca.actualizar_libro(
                isbn,
                self.ent_titulo.get(),
                self.ent_autor.get(),
                self.ent_anio.get(),
                self.ent_cat.get(),
            )

            self.consultar_libros()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Libro actualizado correctamente.")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_libro(self) -> None:
        """Elimina el libro seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            return

        isbn = str(self.tree.item(seleccion[0])["values"][0])

        if messagebox.askyesno("Confirmar", f"¿Eliminar el libro con ISBN {isbn}?"):
            try:
                self.biblioteca.eliminar_por_isbn(isbn)
                self.consultar_libros()
                self.limpiar_campos()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    # =====================================================
    # Helpers
    # =====================================================
    def llenar_tabla(self, lista_libros: list[Libro]) -> None:
        """Llena la tabla asegurando que el ISBN mantenga su formato de texto"""
        for l in lista_libros:
            self.tree.insert(
                "",
                "end",
                values=(str(l.isbn), l.titulo, l.autor, l.anio, l.categoria),
            )

    def rellenar_campos(self, event) -> None:
        """Rellena los campos al seleccionar un libro"""
        seleccion = self.tree.selection()
        if seleccion:
            v = self.tree.item(seleccion[0])["values"]
            self.limpiar_campos()
            self.ent_isbn.insert(0, v[0])
            self.ent_isbn.configure(state="disabled")
            self.ent_titulo.insert(0, v[1])
            self.ent_autor.insert(0, v[2])
            self.ent_anio.insert(0, v[3])
            self.ent_cat.insert(0, v[4])

    def limpiar_campos(self) -> None:
        """Limpia todos los campos del formulario"""
        self.ent_isbn.configure(state="normal")
        for ent in [
            self.ent_isbn,
            self.ent_titulo,
            self.ent_autor,
            self.ent_anio,
            self.ent_cat,
        ]:
            ent.delete(0, "end")

    def ejecutar(self) -> None:
        """Inicia la aplicacion"""
        self.menu_principal()
        self.mainloop()


if __name__ == "__main__":
    app = SistemaGestion()
    app.ejecutar()