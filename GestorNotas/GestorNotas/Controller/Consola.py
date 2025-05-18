import tkinter as tk
from tkinter import messagebox
from Model.GestorUsuarios import GestorUsuarios
from Model.Nota import Nota

gestor = GestorUsuarios()

# ---------------------- INTERFAZ GRÁFICA ----------------------
def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Gestor de Notas - Inicio")
    ventana.geometry("300x200")

    def login():
        nombre = entry_nombre.get()
        contrasena = entry_contrasena.get()
        usuario = gestor.iniciar_sesion_interfaz(nombre, contrasena)
        if usuario:
            messagebox.showinfo("Éxito", "Sesión iniciada correctamente")
            ventana.destroy()
            mostrar_menu(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrecta")

    def registrar():
        nombre = entry_nombre.get()
        contrasena = entry_contrasena.get()
        if gestor.registrar_usuario_interfaz(nombre, contrasena):
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
        else:
            messagebox.showerror("Error", "Usuario ya existe")

    tk.Label(ventana, text="Nombre de usuario").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    tk.Label(ventana, text="Contraseña").pack()
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack()

    tk.Button(ventana, text="Iniciar sesión", command=login).pack(pady=5)
    tk.Button(ventana, text="Registrarse", command=registrar).pack()

    ventana.mainloop()


def mostrar_menu(usuario):
    ventana_menu = tk.Tk()
    ventana_menu.title("Gestor de Notas - Menú Principal")
    ventana_menu.geometry("400x300")

    def crear_nota():
        nueva = tk.Toplevel(ventana_menu)
        nueva.title("Crear Nota")

        tk.Label(nueva, text="Título").pack()
        entrada_titulo = tk.Entry(nueva)
        entrada_titulo.pack()

        tk.Label(nueva, text="Nota (0.0 a 5.0)").pack()
        entrada_contenido = tk.Entry(nueva)
        entrada_contenido.pack()

        def guardar():
            titulo = entrada_titulo.get().strip()
            contenido_str = entrada_contenido.get().strip().replace(",", ".")
            if not titulo or not contenido_str:
                messagebox.showerror("Error", "Los campos no pueden estar vacíos")
                return
            try:
                contenido = float(contenido_str)
                if 0.0 <= contenido <= 5.0:
                    nota = Nota(titulo, contenido)
                    usuario.notas.agregar_nota(nota)
                    messagebox.showinfo("Nota creada", "✅ Nota guardada con éxito")
                    nueva.destroy()
                else:
                    messagebox.showerror("Error", "La nota debe estar entre 0.0 y 5.0")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

        tk.Button(nueva, text="Guardar", command=guardar).pack(pady=5)

    def ver_notas():
        notas = usuario.notas
        actual = notas.head
        texto = ""
        if actual:
            while True:
                n = actual.nota
                texto += f"{n.titulo}: {n.contenido} ({n.fecha_creacion})\n"
                actual = actual.next
                if actual == notas.head:
                    break
        else:
            texto = "No hay notas registradas."

        messagebox.showinfo("Notas", texto)

    def eliminar_nota():
        elim = tk.Toplevel(ventana_menu)
        elim.title("Eliminar Nota")

        tk.Label(elim, text="Título de la nota a eliminar").pack()
        entrada = tk.Entry(elim)
        entrada.pack()

        def eliminar():
            titulo = entrada.get().strip()
            if titulo:
                usuario.notas.eliminar_nota(titulo)
                messagebox.showinfo("Eliminar", f"Intento de eliminación de '{titulo}' completado.")
                elim.destroy()
            else:
                messagebox.showerror("Error", "Debe ingresar un título válido")

        tk.Button(elim, text="Eliminar", command=eliminar).pack(pady=5)

    def editar_nota():
        editar = tk.Toplevel(ventana_menu)
        editar.title("Editar Nota")

        tk.Label(editar, text="Título de la nota a editar").pack()
        entrada_titulo = tk.Entry(editar)
        entrada_titulo.pack()

        tk.Label(editar, text="Nuevo contenido (0.0 a 5.0)").pack()
        entrada_nuevo = tk.Entry(editar)
        entrada_nuevo.pack()

        def actualizar():
            titulo = entrada_titulo.get().strip()
            nuevo_str = entrada_nuevo.get().strip().replace(",", ".")
            if not titulo or not nuevo_str:
                messagebox.showerror("Error", "Los campos no pueden estar vacíos")
                return
            try:
                nuevo = float(nuevo_str)
                if 0.0 <= nuevo <= 5.0:
                    usuario.notas.editar_nota(titulo, nuevo)
                    messagebox.showinfo("Editar", "✅ Nota actualizada")
                    editar.destroy()
                else:
                    messagebox.showerror("Error", "La nota debe estar entre 0.0 y 5.0")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

        tk.Button(editar, text="Actualizar", command=actualizar).pack(pady=5)

    def cambiar_contrasena():
        contrasena_window = tk.Toplevel(ventana_menu)
        contrasena_window.title("Cambiar Contraseña")

        tk.Label(contrasena_window, text="Nueva Contraseña").pack()
        entrada_contrasena = tk.Entry(contrasena_window, show="*")
        entrada_contrasena.pack()

        def guardar_contrasena():
            nueva_contrasena = entrada_contrasena.get()
            if nueva_contrasena:
                usuario.contrasena = nueva_contrasena
                messagebox.showinfo("Éxito", "Contraseña cambiada con éxito")
                contrasena_window.destroy()
            else:
                messagebox.showerror("Error", "Debe ingresar una contraseña válida")

        tk.Button(contrasena_window, text="Guardar", command=guardar_contrasena).pack(pady=5)

    def cerrar():
        ventana_menu.destroy()
        iniciar_interfaz()

    tk.Label(ventana_menu, text=f"Bienvenido, {usuario.nombre_usuario}", font=("Arial", 14)).pack(pady=10)
    tk.Button(ventana_menu, text="Crear Nota", command=crear_nota).pack(pady=5)
    tk.Button(ventana_menu, text="Ver Notas", command=ver_notas).pack(pady=5)
    tk.Button(ventana_menu, text="Eliminar Nota", command=eliminar_nota).pack(pady=5)
    tk.Button(ventana_menu, text="Editar Nota", command=editar_nota).pack(pady=5)
    tk.Button(ventana_menu, text="Cambiar Contraseña", command=cambiar_contrasena).pack(pady=5)
    tk.Button(ventana_menu, text="Cerrar Sesión", command=cerrar).pack(pady=20)

    ventana_menu.mainloop()


# ---------------------- MODO CONSOLA ----------------------

def iniciar_consola():
    print("Bienvenido al Gestor de Notas (Modo Consola)")
    while True:
        opcion = input("¿Deseas (i)niciar sesión o (r)egistrarte? ").strip().lower()
        if opcion in ("i", "r"):
            nombre = input("Nombre de usuario: ").strip()
            contrasena = input("Contraseña: ").strip()
            if opcion == "r":
                if gestor.registrar_usuario_interfaz(nombre, contrasena):
                    print("✅ Usuario registrado.")
                else:
                    print("❌ Usuario ya existe.")
            usuario = gestor.iniciar_sesion_interfaz(nombre, contrasena)
            if usuario:
                print(f"\nBienvenido, {usuario.nombre_usuario} 👋")
                break
            else:
                print("❌ Usuario o contraseña incorrecta.")
        else:
            print("Opción inválida.")

    while True:
        print("\nOpciones:")
        print("1. Crear Nota")
        print("2. Ver Notas")
        print("3. Editar Nota")
        print("4. Eliminar Nota")
        print("5. Cambiar Contraseña")
        print("6. Cerrar Sesión")
        eleccion = input("Selecciona una opción: ").strip()

        if eleccion == "1":
            titulo = input("Título de la nota: ").strip()
            try:
                contenido = float(input("Contenido (0.0 a 5.0): ").replace(",", "."))
                if 0.0 <= contenido <= 5.0:
                    nota = Nota(titulo, contenido)
                    usuario.notas.agregar_nota(nota)
                    print("✅ Nota guardada.")
                else:
                    print("❌ Nota fuera de rango.")
            except ValueError:
                print("❌ Ingresa un número válido.")

        elif eleccion == "2":
            actual = usuario.notas.head
            if not actual:
                print("No hay notas.")
            else:
                print("\nNotas registradas:")
                while True:
                    n = actual.nota
                    print(f"- {n.titulo}: {n.contenido} ({n.fecha_creacion})")
                    actual = actual.next
                    if actual == usuario.notas.head:
                        break

        elif eleccion == "3":
            titulo = input("Título de la nota a editar: ").strip()
            try:
                nuevo = float(input("Nuevo valor (0.0 a 5.0): ").replace(",", "."))
                if 0.0 <= nuevo <= 5.0:
                    usuario.notas.editar_nota(titulo, nuevo)
                    print("✅ Nota actualizada.")
                else:
                    print("❌ Nota fuera de rango.")
            except ValueError:
                print("❌ Número inválido.")

        elif eleccion == "4":
            titulo = input("Título de la nota a eliminar: ").strip()
            usuario.notas.eliminar_nota(titulo)
            print("✅ Intento de eliminación realizado.")

        elif eleccion == "5":
            nueva = input("Nueva contraseña: ").strip()
            usuario.contrasena = nueva
            print("✅ Contraseña actualizada.")

        elif eleccion == "6":
            print("👋 Sesión cerrada.")
            break

        else:
            print("❌ Opción inválida.")


# ---------------------- EJECUCIÓN PRINCIPAL ----------------------

if __name__ == "__main__":
    modo = input("¿Deseas usar la interfaz gráfica (g) o consola (c)? ").strip().lower()
    if modo == "g":
        iniciar_interfaz()
    elif modo == "c":
        iniciar_consola()
    else:
        print("Opción no válida. Ejecuta nuevamente.")
