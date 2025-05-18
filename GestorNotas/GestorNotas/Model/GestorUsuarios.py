from Model.Validar import Validar
from Model.Usuario import Usuario

# Gestor de Usuarios
class GestorUsuarios:
  def __init__(self):
    self.usuarios = {}
    self.validar = Validar()

  def registrar_usuario(self):
    nombre = self.validar.validar_entrada("Ingrese nombre de usuario: ", "usuario")
    if nombre in self.usuarios:
      print("❌ Este usuario ya existe.")
      return None
    contrasena = self.validar.validar_entrada("Ingrese contraseña: ", "contraseña")
    self.usuarios[nombre] = Usuario(nombre, contrasena)
    print("✅ Usuario registrado correctamente.")
    return self.usuarios[nombre]

  def iniciar_sesion(self):
    nombre = self.validar.validar_entrada("Ingrese nombre de usuario: ", "usuario")
    contrasena = self.validar.validar_entrada("Ingrese contraseña: ", "contraseña")
    if nombre in self.usuarios and self.usuarios[nombre].contrasena == contrasena:
      print(f"✅ Bienvenido, {nombre}.")
      return self.usuarios[nombre]
    else:
      print("❌ Credenciales incorrectas.")
      return None

  def cambiar_contrasena(self, usuario):
    nueva_contra = self.validar.validar_entrada("Ingrese nueva contraseña: ", "contraseña")
    usuario.contrasena = nueva_contra
    print("✅ Contraseña actualizada con éxito.")

  def registrar_usuario_interfaz(self, nombre, contrasena):
        if nombre in self.usuarios:
            return False
        self.usuarios[nombre] = Usuario(nombre, contrasena)
        return True

  def iniciar_sesion_interfaz(self, nombre, contrasena):
      if nombre in self.usuarios and self.usuarios[nombre].contrasena == contrasena:
          return self.usuarios[nombre]
      return None