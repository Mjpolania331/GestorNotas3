import pytest
from datetime import datetime
from unittest.mock import patch
from io import StringIO
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


from ..Model.Validar import Validar
from ..Model.Nota import Nota
from ..Model.Usuario import Usuario
from ..Model.Start import Start
from ..Model.ListaNotas import ListaNotas
from ..UI.Menu import Menu
from ..Model.GestorUsuarios import GestorUsuarios

# Pruebas para la clase Validar
class TestValidar:
    def test_validar_usuario_correcto(self):
        with patch('builtins.input', return_value="user_123"):
            assert Validar.validar_entrada("", "usuario") == "user_123"

    def test_validar_usuario_extremos(self):
        # Test mínimo (3 caracteres)
        with patch('builtins.input', return_value="usr"):
            assert Validar.validar_entrada("", "usuario") == "usr"

        # Test máximo (12 caracteres)
        with patch('builtins.input', side_effect=["user123456789", "usr"]):
            assert Validar.validar_entrada("", "usuario") == "usr"

    def test_validar_contenido_extremos(self):
        # Test mínimo (0.0)
        with patch('builtins.input', return_value="0.0"):
            assert Validar.validar_entrada("", "contenido") == 0.0

        # Test máximo (5.0)
        with patch('builtins.input', return_value="5.0"):
            assert Validar.validar_entrada("", "contenido") == 5.0

        # Test inválido (fuera de rango)
        with patch('builtins.input', side_effect=["5.1", "4.9"]):
            assert Validar.validar_entrada("", "contenido") == 4.9


# Pruebas para la clase Nota
class TestNota:
    def test_creacion_nota(self):
        nota = Nota("Título", 3.5)
        assert nota.titulo == "Título"
        assert nota.contenido == 3.5
        assert isinstance(nota.fecha_creacion, str)

    def test_fecha_creacion_formato(self):
        nota = Nota("Test", 2.0)
        try:
            datetime.strptime(nota.fecha_creacion, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pytest.fail("Formato de fecha incorrecto")

    def test_nota_contenido_limites(self):
        # Nota con contenido mínimo
        nota_min = Nota("Mínimo", 0.0)
        assert nota_min.contenido == 0.0

        # Nota con contenido máximo
        nota_max = Nota("Máximo", 5.0)
        assert nota_max.contenido == 5.0


# Pruebas para la clase ListaNotas
class TestListaNotas:
    def test_lista_vacia(self):
        lista = ListaNotas()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            lista.mostrar_notas()
            assert "No hay notas registradas" in fake_out.getvalue()

    def test_agregar_eliminar_nota(self):
        lista = ListaNotas()
        nota = Nota("Test", 3.0)

        # Agregar nota
        lista.agregar_nota(nota)
        assert lista.head.nota.titulo == "Test"

        # Eliminar nota
        with patch('sys.stdout', new=StringIO()) as fake_out:
            lista.eliminar_nota("Test")
            assert "eliminada" in fake_out.getvalue()
            assert lista.head is None

    def test_editar_nota_inexistente(self):
        lista = ListaNotas()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            lista.editar_nota("No existe")
            assert "No se encontró" in fake_out.getvalue()


# Pruebas para la clase Usuario
class TestUsuario:
    def test_creacion_usuario(self):
        usuario = Usuario("test", "1234")
        assert usuario.nombre_usuario == "test"
        assert usuario.contrasena == "1234"
        assert isinstance(usuario.notas, ListaNotas)

    def test_notas_vacias(self):
        usuario = Usuario("user", "pass")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            usuario.notas.mostrar_notas()
            assert "No hay notas" in fake_out.getvalue()
        assert usuario.notas.head.nota.titulo == "Nota 1"


# Pruebas para la clase GestorUsuarios
class TestGestorUsuarios:
    def test_registro_usuario(self):
        gestor = GestorUsuarios()
        with patch('builtins.input', side_effect=["new_user", "1234"]):
            usuario = gestor.registrar_usuario()
            assert usuario.nombre_usuario == "new_user"
            assert "new_user" in gestor.usuarios

    def test_login_exitoso(self):
        gestor = GestorUsuarios()
        gestor.usuarios["exist"] = Usuario("exist", "pass")
        with patch('builtins.input', side_effect=["exist", "pass"]):
            usuario = gestor.iniciar_sesion()
            assert usuario is not None

    def test_login_fallido(self):
        gestor = GestorUsuarios()
        gestor.usuarios["exist"] = Usuario("exist", "pass")
        with patch('builtins.input', side_effect=["exist", "wrong"]), \
                patch('sys.stdout', new=StringIO()) as fake_out:
            usuario = gestor.iniciar_sesion()
            assert usuario is None
            assert "incorrectas" in fake_out.getvalue()


# Pruebas para la clase Menu
class TestMenu:
    def test_menu_opciones(self):
        with patch('builtins.input', return_value="1"):
            assert Menu.menu() == "1"

    def test_menu_display(self, capsys):
        with patch('builtins.input', return_value=""):
            Menu.menu()
            captured = capsys.readouterr()
            assert "Menú" in captured.out
            assert "1️⃣" in captured.out

    def test_menu_multiple_inputs(self):
        with patch('builtins.input', side_effect=["7", "2"]):
            # Primera llamada devuelve "7" (inválido)
            assert Menu.menu() == "7"
            # Segunda llamada devuelve "2"
            assert Menu.menu() == "2"


# Pruebas para la clase Start
class TestStart:
    @patch('builtins.input', side_effect=["3"])
    def test_salir_directo(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Start.start()
            assert "Saliendo" in fake_out.getvalue()

    @patch('builtins.input', side_effect=["1", "test", "wrong", "3"])
    def test_login_fallido_salir(self, mock_input):
        gestor = GestorUsuarios()
        gestor.usuarios["test"] = Usuario("test", "pass")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Start.start()
            assert "incorrectas" in fake_out.getvalue()
            assert "Saliendo" in fake_out.getvalue()

    @patch('builtins.input', side_effect=["2", "newuser", "1234", "6", "3"])
    def test_registro_y_logout(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Start.start()
            output = fake_out.getvalue()
            assert "registrado" in output
            assert "Cerrando sesión" in output