import re

# Clase Validar
class Validar:
  @staticmethod
  def validar_entrada(mensaje, tipo):
    while True:
      valor = input(mensaje).strip()
      if not valor:
        print("❌ El campo no puede estar vacío.")
        continue

      if tipo == "usuario":
        if re.match(r"^[a-zA-Z0-9_]{3,12}$", valor):
          return valor
        print("❌ El nombre de usuario debe tener entre 3 y 12 caracteres alfanuméricos o guion bajo (_).")

      elif tipo == "contraseña":
        if re.match(r"^[a-zA-Z0-9]{4,6}$", valor):
          return valor
        print("❌ La contraseña debe tener entre 4 y 6 caracteres alfanuméricos.")

      elif tipo == "titulo":
        if 3 <= len(valor) <= 50:
          return valor
        print("❌ El título debe tener entre 3 y 50 caracteres.")

      elif tipo == "contenido":  # Contenido de la nota ahora es un número entre 0.0 y 5.0
        try:
          numero = float(valor)
          if 0.0 <= numero <= 5.0:
            return numero
          print("❌ El contenido debe ser un número entre 0.0 y 5.0.")
        except ValueError:
          print("❌ Debe ingresar un número válido entre 0.0 y 5.0.")