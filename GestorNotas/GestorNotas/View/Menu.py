# Menú principal
class Menu:
  @staticmethod
  def menu():
    print("\n📌 --- Menú ---")
    print("1️⃣ Crear nota")
    print("2️⃣ Editar nota")
    print("3️⃣ Eliminar nota")
    print("4️⃣ Ver todas las notas")
    print("5️⃣ Cambiar contraseña")
    print("6️⃣ Cerrar sesión")
    return input("Seleccione una opción: ")
  
  
  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

def crear_nota(self):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    titulo_input = TextInput(hint_text="Título", multiline=False)
    contenido_input = TextInput(hint_text="Nota (0.0 a 5.0)", multiline=False)

    layout.add_widget(titulo_input)
    layout.add_widget(contenido_input)

    def guardar_nota(instance):
        titulo = titulo_input.text.strip()
        contenido_str = contenido_input.text.strip().replace(",", ".")

        if not titulo or not contenido_str:
            self.show_popup("Error", "Los campos no pueden estar vacíos")
            return

        try:
            contenido = float(contenido_str)
            if 0.0 <= contenido <= 5.0:
                nota = Nota(titulo, contenido)
                self.manager.usuario.notas.agregar_nota(nota)
                self.show_popup("Nota creada", "✅ Nota guardada con éxito")
                popup.dismiss()
            else:
                self.show_popup("Error", "La nota debe estar entre 0.0 y 5.0")
        except ValueError:
            self.show_popup("Error", "Ingrese un número válido")

    btn_guardar = Button(text="Guardar", size_hint=(1, None), height=40)
    btn_guardar.bind(on_release=guardar_nota)

    layout.add_widget(btn_guardar)

    popup = Popup(title="Crear Nota", content=layout,
                  size_hint=(None, None), size=(400, 300))
    popup.open()