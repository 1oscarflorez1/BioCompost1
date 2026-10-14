-- =====================================================================
-- BioCompost - 02_constraints.sql
-- Llaves foráneas, restricciones de unicidad, de dominio (CHECK) e índices.
-- Ejecutar después de 01_tables.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- Restricciones de unicidad (UNIQUE)
-- ---------------------------------------------------------------------
ALTER TABLE roles         ADD CONSTRAINT uq_roles_codigo        UNIQUE (codigo);
ALTER TABLE roles         ADD CONSTRAINT uq_roles_nombre        UNIQUE (nombre);
ALTER TABLE usuarios      ADD CONSTRAINT uq_usuarios_correo     UNIQUE (correo);
ALTER TABLE proveedores   ADD CONSTRAINT uq_proveedores_doc     UNIQUE (documento);
ALTER TABLE pilas_compost ADD CONSTRAINT uq_pilas_codigo        UNIQUE (codigo);
ALTER TABLE lotes_abono   ADD CONSTRAINT uq_lotes_codigo        UNIQUE (codigo_lote);

-- ---------------------------------------------------------------------
-- Llaves foráneas (FOREIGN KEY)
-- ---------------------------------------------------------------------
ALTER TABLE usuarios ADD CONSTRAINT fk_usuarios_rol
  FOREIGN KEY (id_rol) REFERENCES roles (id_rol);

ALTER TABLE recolecciones ADD CONSTRAINT fk_recolecciones_proveedor
  FOREIGN KEY (id_proveedor) REFERENCES proveedores (id_proveedor);

ALTER TABLE recolecciones ADD CONSTRAINT fk_recolecciones_usuario
  FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario);

-- Si se elimina una pila, sus recolecciones quedan "sin asignar"
ALTER TABLE recolecciones ADD CONSTRAINT fk_recolecciones_pila
  FOREIGN KEY (id_pila) REFERENCES pilas_compost (id_pila) ON DELETE SET NULL;

-- El monitoreo pertenece a la pila: se elimina junto con ella
ALTER TABLE monitoreo_pilas ADD CONSTRAINT fk_monitoreo_pila
  FOREIGN KEY (id_pila) REFERENCES pilas_compost (id_pila) ON DELETE CASCADE;

ALTER TABLE monitoreo_pilas ADD CONSTRAINT fk_monitoreo_usuario
  FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario);

-- No se puede eliminar una pila que ya produjo lotes de abono
ALTER TABLE lotes_abono ADD CONSTRAINT fk_lotes_pila
  FOREIGN KEY (id_pila) REFERENCES pilas_compost (id_pila);

-- ---------------------------------------------------------------------
-- Restricciones de dominio (CHECK)
-- ---------------------------------------------------------------------
-- Los permisos del backend están programados para estos dos códigos de rol
ALTER TABLE roles ADD CONSTRAINT ck_roles_codigo CHECK (codigo IN ('ADMINISTRADOR', 'RECOLECTOR'));

ALTER TABLE usuarios ADD CONSTRAINT ck_usuarios_activo  CHECK (activo IN ('S', 'N'));
ALTER TABLE usuarios ADD CONSTRAINT ck_usuarios_correo  CHECK (correo LIKE '%_@_%._%');

ALTER TABLE proveedores ADD CONSTRAINT ck_proveedores_tipo
  CHECK (tipo_proveedor IN ('PLAZA_MERCADO', 'FINCA', 'AGROINDUSTRIA'));
ALTER TABLE proveedores ADD CONSTRAINT ck_proveedores_residuo
  CHECK (tipo_residuo IN ('FRUTAS', 'HORTALIZAS', 'ESTIERCOL', 'BAGAZO', 'MIXTO'));
ALTER TABLE proveedores ADD CONSTRAINT ck_proveedores_activo CHECK (activo IN ('S', 'N'));

ALTER TABLE pilas_compost ADD CONSTRAINT ck_pilas_fase
  CHECK (fase IN ('MESOFILICA', 'TERMOFILICA', 'ENFRIAMIENTO', 'MADURACION', 'FINALIZADA'));
ALTER TABLE pilas_compost ADD CONSTRAINT ck_pilas_capacidad CHECK (capacidad_kg > 0);
ALTER TABLE pilas_compost ADD CONSTRAINT ck_pilas_fechas
  CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio);

ALTER TABLE recolecciones ADD CONSTRAINT ck_recolecciones_peso
  CHECK (peso_kg > 0 AND peso_kg <= 50000);
ALTER TABLE recolecciones ADD CONSTRAINT ck_recolecciones_residuo
  CHECK (tipo_residuo IN ('FRUTAS', 'HORTALIZAS', 'ESTIERCOL', 'BAGAZO', 'MIXTO'));
ALTER TABLE recolecciones ADD CONSTRAINT ck_recolecciones_clasif
  CHECK (clasificacion IN ('APTO', 'CONDICIONADO', 'RECHAZADO'));

ALTER TABLE monitoreo_pilas ADD CONSTRAINT ck_monitoreo_temp   CHECK (temperatura BETWEEN 0 AND 90);
ALTER TABLE monitoreo_pilas ADD CONSTRAINT ck_monitoreo_hum    CHECK (humedad BETWEEN 0 AND 100);
ALTER TABLE monitoreo_pilas ADD CONSTRAINT ck_monitoreo_ph     CHECK (ph BETWEEN 0 AND 14);
ALTER TABLE monitoreo_pilas ADD CONSTRAINT ck_monitoreo_volteo CHECK (volteo IN ('S', 'N'));

ALTER TABLE lotes_abono ADD CONSTRAINT ck_lotes_kilos   CHECK (kilos_producidos > 0);
ALTER TABLE lotes_abono ADD CONSTRAINT ck_lotes_calidad CHECK (calidad IN ('PREMIUM', 'ESTANDAR', 'REPROCESO'));
ALTER TABLE lotes_abono ADD CONSTRAINT ck_lotes_estado  CHECK (estado IN ('DISPONIBLE', 'DESPACHADO'));

-- ---------------------------------------------------------------------
-- Índices para las búsquedas y llaves foráneas más consultadas
-- ---------------------------------------------------------------------
CREATE INDEX idx_usuarios_rol          ON usuarios (id_rol);
CREATE INDEX idx_recolecciones_prov    ON recolecciones (id_proveedor);
CREATE INDEX idx_recolecciones_usuario ON recolecciones (id_usuario);
CREATE INDEX idx_recolecciones_pila    ON recolecciones (id_pila);
CREATE INDEX idx_recolecciones_fecha   ON recolecciones (fecha_recoleccion);
CREATE INDEX idx_monitoreo_pila        ON monitoreo_pilas (id_pila, fecha_monitoreo);
CREATE INDEX idx_monitoreo_usuario     ON monitoreo_pilas (id_usuario);
CREATE INDEX idx_lotes_pila            ON lotes_abono (id_pila);
CREATE INDEX idx_pilas_fase            ON pilas_compost (fase);

-- ---------------------------------------------------------------------
-- Diccionario de datos (comentarios visibles en SQL Developer)
-- ---------------------------------------------------------------------
COMMENT ON TABLE roles           IS 'Perfiles de acceso: ADMINISTRADOR (planta) y RECOLECTOR';
COMMENT ON TABLE usuarios        IS 'Usuarios del sistema; la contraseña se guarda cifrada con bcrypt';
COMMENT ON TABLE proveedores     IS 'Puntos de recolección: plazas de mercado, fincas y agroindustrias';
COMMENT ON TABLE pilas_compost   IS 'Pilas de compostaje y su fase de maduración';
COMMENT ON TABLE recolecciones   IS 'Entradas de residuo orgánico: pesaje, fecha, origen y clasificación';
COMMENT ON TABLE monitoreo_pilas IS 'Mediciones periódicas de temperatura, humedad, pH y volteos';
COMMENT ON TABLE lotes_abono     IS 'Lotes de abono orgánico producidos a partir de una pila';

COMMENT ON COLUMN roles.codigo                IS 'Código interno fijo que usan los permisos; no se edita';
COMMENT ON COLUMN roles.nombre                IS 'Nombre visible del rol; el administrador puede cambiarlo';
COMMENT ON COLUMN recolecciones.clasificacion IS 'APTO, CONDICIONADO (con impurezas menores) o RECHAZADO (no se composta)';
COMMENT ON COLUMN pilas_compost.fase          IS 'MESOFILICA, TERMOFILICA, ENFRIAMIENTO, MADURACION o FINALIZADA';
COMMENT ON COLUMN monitoreo_pilas.volteo      IS 'S = se realizó volteo de la pila en esta visita';
