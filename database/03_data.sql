-- =====================================================================
-- BioCompost - 03_data.sql
-- Datos iniciales para pruebas. Ejecutar después de 02_constraints.sql
--
-- Usuarios de prueba (contraseñas cifradas con bcrypt):
--   admin@biocompost.com            / Admin2026*       (ADMINISTRADOR)
--   carlos.rodriguez@biocompost.com / Recolector2026*  (RECOLECTOR)
--   diana.torres@biocompost.com     / Recolector2026*  (RECOLECTOR)
--   pedro.salazar@biocompost.com    / Recolector2026*  (RECOLECTOR inactivo)
-- =====================================================================

-- ---------- Roles ----------
INSERT INTO roles (codigo, nombre, descripcion) VALUES ('ADMINISTRADOR', 'Administrador de planta', 'Gestiona todo el sistema: usuarios, proveedores, pilas, mediciones y lotes');
INSERT INTO roles (codigo, nombre, descripcion) VALUES ('RECOLECTOR', 'Recolector / Proveedor', 'Registra las recolecciones en campo y consulta la información');

-- ---------- Usuarios ----------
INSERT INTO usuarios (nombre, correo, contrasena_hash, telefono, id_rol, activo)
VALUES ('Andrea Martínez', 'admin@biocompost.com', '$2b$10$xByJWWtqWlSoRGT3scWH0.DAeadxaRyC..QytwsZHsBnZg11nZhBm', '3101234567',
        (SELECT id_rol FROM roles WHERE codigo = 'ADMINISTRADOR'), 'S');
INSERT INTO usuarios (nombre, correo, contrasena_hash, telefono, id_rol, activo)
VALUES ('Carlos Rodríguez', 'carlos.rodriguez@biocompost.com', '$2b$10$B53stqqNwy.2fNbUjXVmOuya4yRRhGTXdONNJtjh2uhsOS9334aL2', '3159876543',
        (SELECT id_rol FROM roles WHERE codigo = 'RECOLECTOR'), 'S');
INSERT INTO usuarios (nombre, correo, contrasena_hash, telefono, id_rol, activo)
VALUES ('Diana Torres', 'diana.torres@biocompost.com', '$2b$10$B53stqqNwy.2fNbUjXVmOuya4yRRhGTXdONNJtjh2uhsOS9334aL2', '3204567890',
        (SELECT id_rol FROM roles WHERE codigo = 'RECOLECTOR'), 'S');
INSERT INTO usuarios (nombre, correo, contrasena_hash, telefono, id_rol, activo)
VALUES ('Pedro Salazar', 'pedro.salazar@biocompost.com', '$2b$10$B53stqqNwy.2fNbUjXVmOuya4yRRhGTXdONNJtjh2uhsOS9334aL2', '3007654321',
        (SELECT id_rol FROM roles WHERE codigo = 'RECOLECTOR'), 'N');

-- ---------- Proveedores (puntos de recolección) ----------
INSERT INTO proveedores (nombre, tipo_proveedor, documento, contacto, telefono, direccion, municipio, tipo_residuo, activo, fecha_registro)
VALUES ('Plaza de Mercado El Porvenir', 'PLAZA_MERCADO', '900111222-1', 'Martha Lucía Ríos', '3124455667', 'Calle 34 # 12-40, bodega de residuos', 'Cali', 'FRUTAS', 'S', DATE '2026-04-20');
INSERT INTO proveedores (nombre, tipo_proveedor, documento, contacto, telefono, direccion, municipio, tipo_residuo, activo, fecha_registro)
VALUES ('Plaza de Mercado La Floresta', 'PLAZA_MERCADO', '900222333-2', 'Hernán Castillo', '3135566778', 'Carrera 28 # 30-15', 'Palmira', 'HORTALIZAS', 'S', DATE '2026-04-22');
INSERT INTO proveedores (nombre, tipo_proveedor, documento, contacto, telefono, direccion, municipio, tipo_residuo, activo, fecha_registro)
VALUES ('Finca La Esperanza', 'FINCA', '900333444-3', 'José Arango', '3146677889', 'Vereda El Lauro, km 4', 'Candelaria', 'ESTIERCOL', 'S', DATE '2026-04-25');
INSERT INTO proveedores (nombre, tipo_proveedor, documento, contacto, telefono, direccion, municipio, tipo_residuo, activo, fecha_registro)
VALUES ('Granja Porcícola San José', 'FINCA', '900444555-4', 'Rosa Elena Muñoz', '3167788990', 'Vereda Potrerito, finca San José', 'Jamundí', 'ESTIERCOL', 'S', DATE '2026-04-28');
INSERT INTO proveedores (nombre, tipo_proveedor, documento, contacto, telefono, direccion, municipio, tipo_residuo, activo, fecha_registro)
VALUES ('Trapiche El Cañaveral', 'AGROINDUSTRIA', '900555666-5', 'Fabio Quintero', '3178899001', 'Vía Pradera - Potrerillo km 2', 'Pradera', 'BAGAZO', 'S', DATE '2026-05-02');
INSERT INTO proveedores (nombre, tipo_proveedor, documento, contacto, telefono, direccion, municipio, tipo_residuo, activo, fecha_registro)
VALUES ('Frutos del Valle S.A.S.', 'AGROINDUSTRIA', '900666777-6', 'Liliana Ospina', '3189900112', 'Zona industrial Acopi, bodega 12', 'Yumbo', 'FRUTAS', 'S', DATE '2026-05-02');
INSERT INTO proveedores (nombre, tipo_proveedor, documento, contacto, telefono, direccion, municipio, tipo_residuo, activo, fecha_registro)
VALUES ('Finca Villa Verde', 'FINCA', '900777888-7', 'Álvaro Cifuentes', '3190011223', 'Corregimiento Santa Elena, vereda Alta', 'El Cerrito', 'HORTALIZAS', 'S', DATE '2026-05-10');
INSERT INTO proveedores (nombre, tipo_proveedor, documento, contacto, telefono, direccion, municipio, tipo_residuo, activo, fecha_registro)
VALUES ('Centro de Acopio Agrícola Florida', 'PLAZA_MERCADO', '900888999-8', 'Gloria Patiño', '3201122334', 'Calle 8 # 15-22', 'Florida', 'MIXTO', 'N', DATE '2026-06-15');

-- ---------- Pilas de compostaje ----------
INSERT INTO pilas_compost (codigo, ubicacion, fecha_inicio, fecha_fin, fase, capacidad_kg, observaciones)
VALUES ('P-2026-01', 'Patio A - Era 1', DATE '2026-05-04', DATE '2026-08-12', 'FINALIZADA', 10000, 'Pila cerrada; produjo los lotes L-2026-001 y L-2026-002');
INSERT INTO pilas_compost (codigo, ubicacion, fecha_inicio, fecha_fin, fase, capacidad_kg, observaciones)
VALUES ('P-2026-02', 'Patio A - Era 2', DATE '2026-06-08', DATE '2026-09-16', 'FINALIZADA', 10000, 'Pila cerrada; produjo los lotes L-2026-003 y L-2026-004');
INSERT INTO pilas_compost (codigo, ubicacion, fecha_inicio, fecha_fin, fase, capacidad_kg, observaciones)
VALUES ('P-2026-03', 'Patio B - Era 1', DATE '2026-07-13', NULL, 'MADURACION', 10000, 'En maduración, cosecha estimada a finales de octubre');
INSERT INTO pilas_compost (codigo, ubicacion, fecha_inicio, fecha_fin, fase, capacidad_kg, observaciones)
VALUES ('P-2026-04', 'Patio B - Era 2', DATE '2026-08-20', NULL, 'ENFRIAMIENTO', 8000, NULL);
INSERT INTO pilas_compost (codigo, ubicacion, fecha_inicio, fecha_fin, fase, capacidad_kg, observaciones)
VALUES ('P-2026-05', 'Patio C - Era 1', DATE '2026-09-07', NULL, 'TERMOFILICA', 8000, 'Volteo cada 4 a 5 días');
INSERT INTO pilas_compost (codigo, ubicacion, fecha_inicio, fecha_fin, fase, capacidad_kg, observaciones)
VALUES ('P-2026-06', 'Patio C - Era 2', DATE '2026-10-06', NULL, 'MESOFILICA', 8000, 'Pila en conformación');

-- ---------- Recolecciones (entradas de residuo) ----------
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900111222-1'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-05-04', 870, 'FRUTAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900111222-1'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-05-07', 835, 'FRUTAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-05-11', 940, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900777888-7'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-05-14', 585, 'HORTALIZAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900111222-1'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-05-18', 365, 'FRUTAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-05-21', 1215, 'MIXTO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900333444-3'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-05-25', 825, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900333444-3'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-05-28', 1500, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900111222-1'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-06-01', 355, 'FRUTAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900333444-3'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), DATE '2026-06-04', 1390, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900555666-5'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-06-08', 1815, 'BAGAZO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-06-11', 820, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-06-15', 840, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900777888-7'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-06-18', 445, 'HORTALIZAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900333444-3'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-06-22', 1110, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900555666-5'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-06-25', 830, 'BAGAZO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900222333-2'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-06-29', 780, 'HORTALIZAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900666777-6'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-07-02', 900, 'MIXTO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-07-06', 1180, 'ESTIERCOL', 'CONDICIONADO', 'Presencia menor de plásticos, se retiraron manualmente');
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900666777-6'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), DATE '2026-07-09', 775, 'FRUTAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900555666-5'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-07-13', 1280, 'BAGAZO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900555666-5'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-07-16', 1400, 'BAGAZO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-07-20', 735, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900111222-1'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-07-23', 830, 'MIXTO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900777888-7'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-07-27', 445, 'HORTALIZAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900333444-3'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-07-30', 1020, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-08-03', 945, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900777888-7'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-08-06', 430, 'HORTALIZAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-08-10', 1130, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-08-13', 645, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900666777-6'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), DATE '2026-08-17', 450, 'FRUTAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), DATE '2026-08-20', 655, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900222333-2'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), NULL, DATE '2026-08-24', 260, 'HORTALIZAS', 'RECHAZADO', 'Residuo contaminado con material inorgánico');
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900555666-5'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), DATE '2026-08-27', 1805, 'BAGAZO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900222333-2'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), DATE '2026-08-31', 590, 'HORTALIZAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900333444-3'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), DATE '2026-09-03', 1170, 'ESTIERCOL', 'CONDICIONADO', 'Presencia menor de plásticos, se retiraron manualmente');
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900333444-3'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), DATE '2026-09-07', 1115, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900777888-7'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), DATE '2026-09-10', 560, 'HORTALIZAS', 'CONDICIONADO', 'Presencia menor de plásticos, se retiraron manualmente');
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900222333-2'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), DATE '2026-09-14', 320, 'HORTALIZAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900666777-6'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), DATE '2026-09-17', 470, 'FRUTAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900222333-2'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), DATE '2026-09-21', 755, 'HORTALIZAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), DATE '2026-09-24', 620, 'ESTIERCOL', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), DATE '2026-09-28', 585, 'MIXTO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900111222-1'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), DATE '2026-10-01', 690, 'FRUTAS', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900111222-1'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), DATE '2026-10-05', 585, 'MIXTO', 'APTO', NULL);
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900444555-4'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), (SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-06'), DATE '2026-10-08', 595, 'ESTIERCOL', 'APTO', NULL);

-- Entradas recientes aún pendientes de asignar a una pila
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900555666-5'), (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rodriguez@biocompost.com'), NULL, DATE '2026-10-10', 1450, 'BAGAZO', 'APTO', 'Pendiente de asignar a pila');
INSERT INTO recolecciones (id_proveedor, id_usuario, id_pila, fecha_recoleccion, peso_kg, tipo_residuo, clasificacion, observaciones)
VALUES ((SELECT id_proveedor FROM proveedores WHERE documento = '900666777-6'), (SELECT id_usuario FROM usuarios WHERE correo = 'diana.torres@biocompost.com'), NULL, DATE '2026-10-11', 720, 'FRUTAS', 'CONDICIONADO', 'Algunas bolsas plásticas mezcladas, se retiraron manualmente');

-- ---------- Monitoreo de pilas ----------
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-05-05', 29.3, 47.6, 7.3, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-05-12', 63.1, 57.1, 7.3, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-05-17', 55.6, 52.7, 7.8, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-05-21', 56.7, 53.8, 8.2, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-05-26', 60.1, 46.3, 6.8, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-01', 61.0, 49.9, 6.6, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-08', 56.6, 58.9, 8.0, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-12', 66.4, 58.3, 8.0, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-16', 47.3, 54.6, 7.4, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-20', 45.6, 57.8, 7.7, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-26', 41.6, 58.3, 6.4, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-30', 38.8, 57.3, 6.6, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-06', 29.0, 49.9, 6.9, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-12', 28.4, 37.3, 8.1, 'N', 'Humedad baja: se aplicó riego');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-18', 28.2, 33.5, 6.2, 'N', 'Humedad baja: se aplicó riego');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-22', 26.9, 61.8, 8.0, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-28', 28.3, 56.1, 7.5, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-04', 26.2, 52.9, 8.3, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-08', 27.0, 56.6, 8.1, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-09', 28.2, 46.0, 7.7, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-13', 44.1, 57.4, 7.8, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-17', 58.9, 45.3, 8.2, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-21', 64.4, 47.0, 6.5, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-06-27', 55.4, 51.5, 6.7, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-02', 65.1, 36.6, 7.3, 'S', 'Humedad baja: se aplicó riego');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-08', 65.2, 35.7, 7.1, 'N', 'Humedad baja: se aplicó riego');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-13', 67.3, 54.4, 7.6, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-19', 48.7, 57.6, 6.3, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-24', 45.7, 56.5, 8.0, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-31', 41.7, 58.4, 7.4, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-05', 36.9, 52.8, 7.9, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-11', 28.7, 47.6, 8.1, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-17', 29.9, 56.9, 7.9, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-22', 27.3, 57.4, 6.5, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-26', 29.6, 34.1, 8.0, 'N', 'Humedad baja: se aplicó riego');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-01', 27.7, 51.5, 8.2, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-06', 28.4, 47.4, 7.0, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-12', 25.8, 56.3, 6.6, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-14', 28.2, 47.3, 7.0, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-18', 46.4, 61.0, 6.9, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-23', 70.4, 47.5, 6.3, 'S', 'Temperatura alta: se programó volteo adicional');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-27', 71.9, 54.0, 7.5, 'S', 'Temperatura alta: se programó volteo adicional');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-07-31', 67.8, 57.4, 7.0, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-04', 59.5, 53.8, 7.9, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-11', 66.9, 37.9, 7.9, 'N', 'Humedad baja: se aplicó riego');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-17', 64.8, 53.6, 6.9, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-24', 48.2, 58.7, 6.7, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-30', 45.4, 59.1, 7.4, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-06', 40.5, 47.2, 6.8, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-12', 29.2, 49.5, 7.3, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-18', 28.5, 54.5, 6.5, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-24', 28.9, 51.8, 7.4, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-30', 28.6, 56.5, 8.1, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-10-05', 27.4, 46.0, 7.0, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-03'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-10-10', 25.6, 49.3, 6.9, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-21', 30.3, 59.5, 7.2, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-25', 43.1, 47.1, 8.0, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-08-31', 59.2, 53.8, 7.5, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-05', 68.0, 34.6, 6.7, 'S', 'Humedad baja: se aplicó riego');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-10', 64.2, 53.9, 7.4, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-14', 58.5, 57.5, 8.3, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-21', 63.6, 55.3, 6.7, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-27', 55.5, 37.0, 6.7, 'N', 'Humedad baja: se aplicó riego');
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-10-02', 47.4, 57.4, 6.8, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-04'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-10-09', 44.5, 56.0, 7.3, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-08', 30.9, 59.5, 8.2, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-14', 61.4, 46.3, 7.4, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-20', 67.5, 59.8, 7.5, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-09-25', 55.4, 59.5, 6.5, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-10-01', 65.1, 56.5, 8.0, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-10-08', 61.9, 55.3, 7.7, 'S', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-06'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-10-07', 27.5, 56.2, 6.3, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-06'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-10-11', 44.1, 58.9, 6.5, 'N', NULL);
INSERT INTO monitoreo_pilas (id_pila, id_usuario, fecha_monitoreo, temperatura, humedad, ph, volteo, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-05'), (SELECT id_usuario FROM usuarios WHERE correo = 'admin@biocompost.com'), DATE '2026-10-11', 71.8, 38.5, 7.4, 'N', 'Temperatura alta y humedad baja: programar volteo y riego');

-- ---------- Lotes de abono producidos ----------
INSERT INTO lotes_abono (id_pila, codigo_lote, fecha_produccion, kilos_producidos, calidad, estado, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), 'L-2026-001', DATE '2026-08-14', 1700, 'PREMIUM', 'DESPACHADO', 'Despachado a Finca La Esperanza');
INSERT INTO lotes_abono (id_pila, codigo_lote, fecha_produccion, kilos_producidos, calidad, estado, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-01'), 'L-2026-002', DATE '2026-08-14', 1400, 'ESTANDAR', 'DESPACHADO', 'Uso en huertas comunitarias');
INSERT INTO lotes_abono (id_pila, codigo_lote, fecha_produccion, kilos_producidos, calidad, estado, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), 'L-2026-003', DATE '2026-09-18', 1850, 'PREMIUM', 'DISPONIBLE', NULL);
INSERT INTO lotes_abono (id_pila, codigo_lote, fecha_produccion, kilos_producidos, calidad, estado, observaciones)
VALUES ((SELECT id_pila FROM pilas_compost WHERE codigo = 'P-2026-02'), 'L-2026-004', DATE '2026-09-18', 1450, 'ESTANDAR', 'DISPONIBLE', 'Empacado en bultos de 40 kg');

COMMIT;
