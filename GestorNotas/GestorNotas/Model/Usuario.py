from Model.ListaNotas import ListaNotas

# Clase Usuario
class Usuario:
  def __init__(self, nombre_usuario, contrasena):
    self.nombre_usuario = nombre_usuario
    self.contrasena = contrasena
    self.notas = ListaNotas()