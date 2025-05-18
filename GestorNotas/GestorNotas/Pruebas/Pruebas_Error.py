import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from pathlib import Path

# Configurar ruta del proyecto
RUTA_PROYECTO = Path(__file__).parent.parent
sys.path.append(str(RUTA_PROYECTO))

# Importar módulos
from ..Model.Validar import Validar
from ..Model.Nota import Nota
from ..Model.Usuario import Usuario
from ..Model.Start import Start
from ..Model.ListaNotas import ListaNotas
from ..UI.Menu import Menu
from ..Model.GestorUsuarios import GestorUsuarios


# ==================== PRUEBAS DE ERRORES ====================

class TestErroresValidar:
    """Pruebas para casos de error en la clase Validar"""

    def test_usuario_invalido_caracteres_especiales(self):
        with patch('builtins.input', side_effect=["user@123", "user_123"]), \
                patch('sys.stdout', new=StringIO()) as salida:
            resultado = Validar.validar_entrada("", "usuario")
            assert "❌ El nombre de usuario debe tener" in salida.getvalue()
            assert resultado == "user_123"

    def test_contrasena_demasiado_larga(self):
        with patch('builtins.input', side_effect=["1234567", "123456"]), \
                patch('sys.stdout', new=StringIO()) as salida:
            resultado = Validar.validar_entrada("", "contraseña")
            assert "❌ La contraseña debe tener" in salida.getvalue()
            assert resultado == "123456"

    def test_contenido_no_numerico(self):
        with patch('builtins.input', side_effect=["no es número", "3.5"]), \
                patch('sys.stdout', new=StringIO()) as salida:
            resultado = Validar.validar_entrada("", "contenido")
            assert "❌ Debe ingresar un número válido" in salida.getvalue()
            assert resultado == 3.5


class TestErroresNota:
    """Pruebas para casos de error en la clase Nota"""

    def test_crear_nota_con_contenido_invalido(self):
        with pytest.raises(ValueError):
            Nota("Título válido", 10.0)  # Contenido fuera de rango

    def test_crear_nota_con_titulo_vacio(self):
        with pytest.raises(ValueError):
            Nota("", 3.5)  # Título vacío


class TestErroresListaNotas:
    """Pruebas para casos de error en la clase ListaNotas"""

    def test_eliminar_nota_inexistente(self):
        lista = ListaNotas()
        lista.agregar_nota(Nota("Existente", 2.5))
        with patch('sys.stdout', new=StringIO()) as salida:
            lista.eliminar_nota("no_existe")
            assert "No se encontró" in salida.getvalue()

    def test_editar_lista_vacia(self):
        lista = ListaNotas()
        with patch('sys.stdout', new=StringIO()) as salida:
            lista.editar_nota("cualquiera")
            assert "No hay notas registradas" in salida.getvalue()


class TestErroresUsuario:
    """Pruebas para casos de error en la clase Usuario"""

    def test_crear_usuario_con_contrasena_vacia(self):
        with pytest.raises(ValueError):
            Usuario("test", "")

    def test_agregar_nota_invalida(self):
        usuario = Usuario("test", "1234")
        with pytest.raises(TypeError):
            usuario.notas.agregar_nota("No es un objeto Nota")


class TestErroresGestorUsuarios:
    """Pruebas para casos de error en la clase GestorUsuarios"""

    def test_registrar_usuario_existente(self):
        gestor = GestorUsuarios()
        gestor.usuarios["existente"] = Usuario("existente", "1234")
        with patch('builtins.input', side_effect=["existente", "nuevapass"]), \
                patch('sys.stdout', new=StringIO()) as salida:
            resultado = gestor.registrar_usuario()
            assert resultado is None
            assert "Este usuario ya existe" in salida.getvalue()

    def test_iniciar_sesion_usuario_inexistente(self):
        gestor = GestorUsuarios()
        with patch('builtins.input', side_effect=["no_existe", "pass"]), \
                patch('sys.stdout', new=StringIO()) as salida:
            resultado = gestor.iniciar_sesion()
            assert resultado is None
            assert "Credenciales incorrectas" in salida.getvalue()


class TestErroresMenu:
    """Pruebas para casos de error en la clase Menu"""

    def test_opcion_menu_invalida(self):
        with patch('builtins.input', return_value="999"), \
                patch('sys.stdout', new=StringIO()) as salida:
            resultado = Menu.menu()
            assert resultado == "999"
            assert "Menú" in salida.getvalue()


class TestErroresStart:
    """Pruebas para casos de error en la clase Start"""

    @patch('builtins.input', side_effect=["99", "3"])
    def test_opcion_principal_invalida(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as salida:
            Start.start()
            output = salida.getvalue()
            assert "Opción no válida" in output
            assert "Saliendo" in output

    @patch('builtins.input', side_effect=["1", "", "valido", "pass", "6", "3"])
    def test_login_usuario_vacio(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as salida:
            Start.start()
            output = salida.getvalue()
            assert "El campo no puede estar vacío" in output
            assert "Bienvenido" in output


if __name__ == "__main__":
    pytest.main(["-v", "--cov=../Model", "--cov-report=html"])