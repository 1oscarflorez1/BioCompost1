# Prompt para generar la presentación en NotebookLM

## Paso 1. Cargar las fuentes

Cree un cuaderno nuevo en [NotebookLM](https://notebooklm.google.com) y agregue como fuentes estos archivos del
repositorio (si no acepta `.md`, cambie la extensión a `.txt` o use *Texto copiado* y pegue el contenido):

1. `docs/presentacion/resumen_proyecto.md` ← **la más importante**
2. `README.md`
3. `docs/modelo_datos.md`
4. `docs/arquitectura.md`
5. `docs/api.md`
6. `docs/pruebas.md`
7. `Enunciado_Proyecto_Integrador_Desarrollo_Web.docx` (para que respete los criterios de evaluación)

Opcional: capturas de pantalla del dashboard, Swagger y la ejecución de las pruebas.

## Paso 2. Generar la presentación

En el panel **Studio** elija **Presentación** (*Slide deck*), pulse el ícono de lápiz para personalizar y pegue
el siguiente prompt. Antes de pegarlo, reemplace `[Integrante 1]`, `[Integrante 2]` e `[Integrante 3]` por los
nombres reales.

---

```text
Crea una presentación académica en español para sustentar el proyecto integrador "BioCompost: Sistema de
Trazabilidad de Recolección de Residuos Orgánicos y Compostaje Agrícola" ante el docente y el salón del curso
Desarrollo Web y Sistemas Móviles de la Universidad Cooperativa de Colombia, sede Cali.

Usa ÚNICAMENTE la información de las fuentes; no inventes cifras, tecnologías ni funcionalidades. Las cifras
oficiales son: 7 tablas en Oracle, 5 módulos, 42 endpoints, 2 roles, 48 recolecciones, 40,37 toneladas
desviadas de vertederos, 6.400 kg de abono producido, rendimiento de 34,8 %, 24 pruebas pytest aprobadas y
41 verificaciones de Postman aprobadas.

Duración de la exposición: 20 minutos, entre tres expositores. Indica en cada diapositiva quién la presenta
con una etiqueta pequeña: [Integrante 1], [Integrante 2] o [Integrante 3].

Estructura (una idea principal por diapositiva, máximo 5 viñetas cortas, frases breves, sin párrafos):

[Integrante 1]
1. Portada: nombre del proyecto, subtítulo, curso, universidad, periodo 2026-2 y los tres integrantes.
2. El problema: residuos orgánicos de plazas de mercado, fincas y agroindustrias que terminan en vertederos,
   y la falta de trazabilidad de una planta de compostaje.
3. Objetivo y alcance: objetivo general y los 5 módulos funcionales en una sola vista.
4. Arquitectura de tres capas: diagrama Usuario → Frontend → API REST FastAPI → Oracle → API → Frontend,
   con las tecnologías de cada capa.
5. Decisión técnica: "antes y después" de la conexión a la base de datos (ORDS + curl con errores →
   oracledb + Oracle en Docker) y por qué se tomó esa decisión.
6. Modelo de datos: las 7 tablas y sus relaciones, destacando la cadena de trazabilidad
   Proveedor → Recolección → Pila → Lote de abono.
7. Integridad y seguridad: restricciones de Oracle (PK, FK, UNIQUE, CHECK), contraseñas con bcrypt, token JWT,
   roles Administrador de planta y Recolector / Proveedor con sus permisos (401 y 403), y la decisión de dar a
   cada rol un código interno fijo para los permisos y un nombre visible que el administrador puede editar.

[Integrante 2]
8. Backend con FastAPI: organización en capas (routers, schemas, services, models, database, core),
   42 endpoints documentados en Swagger y los códigos HTTP usados (200, 201, 400, 401, 403, 404, 409, 422, 503).
9. Validación en tres niveles: navegador, backend y base de datos, con un ejemplo de error mostrado al usuario.
10. Módulo de proveedores: CRUD, búsqueda y filtros por tipo, residuo, municipio y estado.
11. Módulo de recolecciones: pesaje, clasificación apto/condicionado/rechazado, reglas de negocio
    (rechazado no entra a pila, proveedor inactivo, pila finalizada) y permisos del recolector.

[Integrante 3]
12. Control de pilas de compostaje: las fases mesofílica, termofílica, enfriamiento, maduración y finalizada,
    el filtro por fase y el monitoreo de temperatura, humedad, pH y volteos con alertas (>70 °C, humedad fuera
    de 40 %–65 %).
13. Lotes de abono y trazabilidad: de un lote se llega a su pila, sus recolecciones y sus proveedores;
    rendimiento de 34,8 %.
14. Dashboard y reportes: indicadores (40,37 t desviadas, 6.400 kg de abono), reporte consolidado de toneladas
    transformadas por mes, reporte por proveedor y exportación a CSV.
15. Frontend responsive: HTML5, Bootstrap, JavaScript con fetch(), vista en computador y en celular.
16. Pruebas: 24 pruebas automatizadas y colección de Postman, con la tabla de casos (login, CRUD, validación,
    control de acceso por rol, filtros, reportes).
17. Demostración en vivo: diapositiva de transición con los pasos que se mostrarán.
18. Conclusiones, aprendizajes del equipo y trabajo futuro (nube con HTTPS, app móvil, sensores, código QR en
    los bultos de abono).
19. Preguntas y agradecimiento.

Estilo visual: limpio y profesional, paleta verde bosque, verde claro y tonos tierra, íconos sencillos de
hojas, reciclaje, camión, termómetro y base de datos. Usa diagramas para la arquitectura, el modelo de datos y la
cadena de trazabilidad, y gráficos o tarjetas grandes para las cifras. Evita el exceso de texto.

Incluye notas del orador en cada diapositiva con lo que debe decir el expositor en 3 a 5 frases.
```

---

## Paso 3 (opcional). Otros formatos útiles de NotebookLM

**Resumen en video o audio** (para repasar antes de la sustentación) — en *Personalizar* pegue:

```text
Explica en español, en 6 minutos y con tono cercano para estudiantes, cómo funciona BioCompost de punta a punta:
el problema de los residuos orgánicos, la arquitectura Frontend → FastAPI → Oracle, la trazabilidad
proveedor → recolección → pila → lote, la seguridad por roles y las pruebas realizadas. Usa solo las fuentes.
```

**Simulacro de preguntas del docente** — en el chat del cuaderno escriba:

```text
Actúa como el docente evaluador del proyecto integrador. Con base en el enunciado y en las fuentes, hazme
10 preguntas difíciles sobre BioCompost (arquitectura, base de datos, seguridad, API REST, frontend, pruebas
y decisiones de diseño), una por una. Después de cada respuesta mía, califícala de 1 a 5 según los criterios de
evaluación del enunciado y dime qué faltó.
```

**Guía de estudio** — en *Informes* elija *Guía de estudio* para obtener un cuestionario con respuestas que
cada integrante puede usar para prepararse.
