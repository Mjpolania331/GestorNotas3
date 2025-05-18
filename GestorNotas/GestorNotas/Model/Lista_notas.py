from Model.NodoNota import NodoNota
from Model.Validar import Validar
import datetime

# Lista doblemente enlazada circular para las notas
class ListaNotas:
  def __init__(self):
    self.head = None

  def agregar_nota(self, nota):
    nuevo_nodo = NodoNota(nota)
    if self.head is None:
      self.head = nuevo_nodo
      nuevo_nodo.prev = nuevo_nodo
      nuevo_nodo.next = nuevo_nodo
    else:
      last = self.head.prev
      nuevo_nodo.prev = last
      nuevo_nodo.next = self.head
      self.head.prev = nuevo_nodo
      last.next = nuevo_nodo
      self.head = nuevo_nodo

  def eliminar_nota(self, titulo):
    if self.head is None:
      print("⚠ No hay notas registradas.")
      return

    current = self.head
    while True:
      if current.nota.titulo == titulo:
        if current.next == current:
          self.head = None
        else:
          if current == self.head:
            self.head = current.next
          current.prev.next = current.next
          current.next.prev = current.prev
        print(f"✅ Nota '{titulo}' eliminada.")
        return
      current = current.next
      if current == self.head:
        break

    print(f"❌ No se encontró una nota con el título '{titulo}'.")

  def editar_nota(self, titulo, nuevo_valor):
    actual = self.head
    if actual:
        while True:
            if actual.nota.titulo == titulo:
                actual.nota.contenido = nuevo_valor
                return True
            actual = actual.next
            if actual == self.head:
                break
    return False

    current = self.head
    while True:
      if current.nota.titulo == titulo:
        print(f"✏ Editando nota: {titulo}")
        nuevo_contenido = validar.validar_entrada("Nuevo contenido (0.0 - 5.0): ", "contenido")
        current.nota.contenido = nuevo_contenido
        current.nota.fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("✅ Nota actualizada correctamente.")
        return
      current = current.next
      if current == self.head:
        break

    print(f"❌ No se encontró una nota con el título '{titulo}'.")

  def mostrar_notas(self):
    if self.head is None:
      print("⚠ No hay notas registradas.")
      return

    current = self.head
    print("\n📋 --- Tus Notas ---")
    while True:
      nota = current.nota
      print(f"📌 Título: {nota.titulo}\n📊 Contenido (calificación): {nota.contenido}\n📅 Fecha: {nota.fecha_creacion}\n")
      current = current.next
      if current == self.head:
        break