import datetime

# Clase Nota
class Nota:
  def __init__(self, titulo, contenido):
    self.titulo = titulo
    self.contenido = contenido  # Ahora es un número entre 0.0 y 5.0
    self.fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")