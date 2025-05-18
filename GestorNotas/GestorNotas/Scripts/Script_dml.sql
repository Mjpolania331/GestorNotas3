-- Script DML: Insertar datos de ejemplo en Gestor de Notas

-- Insertar usuarios
INSERT INTO Usuarios (nombre_usuario, contrasena) VALUES ('juan', '1234');
INSERT INTO Usuarios (nombre_usuario, contrasena) VALUES ('maria', 'abcd');

-- Insertar notas para juan (asumiendo id_usuario = 1)
INSERT INTO Notas (titulo, contenido, id_usuario) VALUES ('Matemáticas', 4.5, 1);
INSERT INTO Notas (titulo, contenido, id_usuario) VALUES ('Historia', 3.7, 1);

-- Insertar notas para maria (asumiendo id_usuario = 2)
INSERT INTO Notas (titulo, contenido, id_usuario) VALUES ('Biología', 5.0, 2);
INSERT INTO Notas (titulo, contenido, id_usuario) VALUES ('Química', 4.2, 2);

-- Ejemplo UPDATE (editar nota)
UPDATE Notas SET contenido = 4.8 WHERE titulo = 'Matemáticas' AND id_usuario = 1;

-- Ejemplo DELETE (eliminar nota)
DELETE FROM Notas WHERE titulo = 'Historia' AND id_usuario = 1;
