import pytest
from unittest.mock import patch
from io import StringIO
import re
import datetime
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


from ..Model.Validar import Validar
from ..Model.Nota import Nota
from ..Model.ListaNotas import ListaNotas
from ..Model.Usuario import Usuario
from ..Model.Start import Start
from ..Model.GestorUsuarios import GestorUsuarios
from ..UI.Menu import Menu

# ==================== PRUEBAS UNITARIAS ====================

# Pruebas para Validar
class TestValidar:
    @patch('builtins.input', return_value="user123")
    def test_validar_usuario_valido(self, mock_input):
        assert Validar.validar_entrada("", "usuario") == "user123"

    @patch('builtins.input', return_value="pass")
    def test_validar_contrasena_valida(self, mock_input):
        assert Validar.validar_entrada("", "contraseña") == "pass"

    @patch('builtins.input', return_value="3.5")
    def test_validar_contenido_valido(self, mock_input):
        assert Validar.validar_entrada("", "contenido") == 3.5

    @patch('builtins.input', side_effect=["user@123", "user_123"])
    def test_usuario_invalido(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Validar.validar_entrada("", "usuario")
            assert "caracteres alfanuméricos" in fake_out.getvalue()

    @patch('builtins.input', side_effect=["1234567", "123456"])
    def test_contrasena_larga(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Validar.validar_entrada("", "contraseña")
            assert "4 y 6 caracteres" in fake_out.getvalue()

    @patch('builtins.input', side_effect=["texto", "3.5"])
    def test_contenido_no_numerico(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Validar.validar_entrada("", "contenido")
            assert "número válido" in fake_out.getvalue()


# Pruebas para Nota
class TestNota:
    def test_creacion_nota(self):
        nota = Nota("Título", 4.5)
        assert nota.titulo == "Título"
        assert nota.contenido == 4.5

    def test_fecha_creacion(self):
        nota = Nota("Test", 3.0)
        assert isinstance(nota.fecha_creacion, str)

    def test_nota_contenido_float(self):
        nota = Nota("Float", 2.5)
        assert isinstance(nota.contenido, float)


# Pruebas para ListaNotas
class TestListaNotas:
    def test_agregar_nota(self):
        lista = ListaNotas()
        lista.agregar_nota(Nota("Nota 1", 3.0))
        assert lista.head is not None

    def test_lista_vacia(self):
        lista = ListaNotas()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            lista.mostrar_notas()
            assert "No hay notas" in fake_out.getvalue()

    def test_mostrar_notas(self):
        lista = ListaNotas()
        lista.agregar_nota(Nota("Mostrar", 4.0))
        with patch('sys.stdout', new=StringIO()) as fake_out:
            lista.mostrar_notas()
            assert "Mostrar" in fake_out.getvalue()

    def test_eliminar_nota_lista_vacia(self):
        lista = ListaNotas()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            lista.eliminar_nota("inexistente")
            assert "No hay notas" in fake_out.getvalue()


# Pruebas para Usuario
class TestUsuario:
    def test_creacion_usuario(self):
        usuario = Usuario("test", "1234")
        assert usuario.nombre_usuario == "test"

    def test_notas_vacias(self):
        usuario = Usuario("user", "pass")
        assert usuario.notas.head is None

    def test_agregar_nota_usuario(self):
        usuario = Usuario("user", "pass")
        usuario.notas.agregar_nota(Nota("Nota", 3.5))
        assert usuario.notas.head is not None


# Pruebas para GestorUsuarios
class TestGestorUsuarios:
    def test_registro_usuario(self):
        gestor = GestorUsuarios()
        with patch('builtins.input', side_effect=["newuser", "1234"]):
            usuario = gestor.registrar_usuario()
            assert usuario is not None

    def test_login_exitoso(self):
        gestor = GestorUsuarios()
        gestor.usuarios["user"] = Usuario("user", "pass")
        with patch('builtins.input', side_effect=["user", "pass"]):
            usuario = gestor.iniciar_sesion()
            assert usuario is not None

    def test_login_fallido(self):
        gestor = GestorUsuarios()
        with patch('builtins.input', side_effect=["user", "wrong"]):
            usuario = gestor.iniciar_sesion()
            assert usuario is None


# Pruebas para Menu
class TestMenu:
    @patch('builtins.input', return_value="1")
    def test_menu_opcion_valida(self, mock_input):
        assert Menu.menu() == "1"

    @patch('builtins.input', return_value="")
    def test_menu_sin_input(self, mock_input):
        assert Menu.menu() == ""

    def test_menu_display(self, capsys):
        with patch('builtins.input', return_value=""):
            Menu.menu()
            captured = capsys.readouterr()
            assert "Menú" in captured.out


# Pruebas para Start
class TestStart:
    @patch('builtins.input', side_effect=["3"])
    def test_salir_directo(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Start.start()
            assert "Saliendo" in fake_out.getvalue()

    @patch('builtins.input', side_effect=["1", "user", "pass", "6", "3"])
    def test_login_exitoso(self, mock_input):
        gestor = GestorUsuarios()
        gestor.usuarios["user"] = Usuario("user", "pass")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Start.start()
            assert "Bienvenido" in fake_out.getvalue()

    @patch('builtins.input', side_effect=["2", "newuser", "1234", "6", "3"])
    def test_registro_exitoso(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Start.start()
            assert "registrado" in fake_out.getvalue()

    @patch('builtins.input', side_effect=["1", "  ", "user", "pass", "6", "3"])
    def test_login_usuario_vacio(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Start.start()
            assert "El campo no puede estar vacío" in fake_out.getvalue()

    @patch('builtins.input', side_effect=["2", "inválido!", "valid", "1234", "6", "3"])
    def test_registro_usuario_invalido(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Start.start()
            assert "caracteres alfanuméricos" in fake_out.getvalue()


if __name__ == "__main__":
    pytest.main(["-v"])