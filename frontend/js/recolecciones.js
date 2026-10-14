// Módulo 3: Registro de recolecciones y entradas (pesaje, fecha, origen y clasificación).
// - Cualquier usuario puede registrar.
// - El RECOLECTOR solo edita sus propios registros; solo el ADMINISTRADOR elimina.

const usuario = UI.iniciar({ pagina: 'recolecciones', titulo: 'Recolecciones' });
const esAdmin = Sesion.esAdmin();
const COLUMNAS = 8;

const tabla = document.getElementById('tabla');
const filtros = document.getElementById('formFiltros');
const formulario = document.getElementById('formRecoleccion');
const modal = new bootstrap.Modal('#modalRecoleccion');
let recolecciones = [];
let proveedores = [];
let pilas = [];
let idEditando = null;

UI.opcionesCatalogo(filtros.tipo_residuo, CATALOGOS.tipoResiduo, 'Todos');
UI.opcionesCatalogo(filtros.clasificacion, CATALOGOS.clasificacion, 'Todas');
UI.opcionesCatalogo(formulario.tipo_residuo, CATALOGOS.tipoResiduo, 'Seleccione...');
UI.opcionesCatalogo(formulario.clasificacion, CATALOGOS.clasificacion);
formulario.fecha_recoleccion.max = UI.hoy();

if (usuario) iniciar();

async function iniciar() {
  try {
    [proveedores, pilas] = await Promise.all([Api.get('/proveedores'), Api.get('/pilas')]);
    UI.opciones(filtros.id_proveedor, proveedores, 'id_proveedor', (p) => p.nombre, 'Todos');
    UI.opciones(filtros.id_pila, pilas, 'id_pila', (p) => p.codigo, 'Todas');
    await cargar();
    if (UI.parametroUrl('nuevo')) abrirFormulario();
  } catch (error) {
    UI.error(error);
  }
}

filtros.addEventListener('input', UI.esperar(cargar));
filtros.addEventListener('reset', () => setTimeout(cargar));
filtros.addEventListener('submit', (evento) => evento.preventDefault());
document.getElementById('btnNuevo').addEventListener('click', () => abrirFormulario());

async function cargar() {
  UI.cargando(tabla, COLUMNAS);
  try {
    recolecciones = await Api.get('/recolecciones', UI.datosFormulario(filtros));
    pintar();
  } catch (error) {
    UI.sinDatos(tabla, COLUMNAS, 'No fue posible cargar la información');
    UI.error(error);
  }
}

function puedeEditar(r) {
  return esAdmin || r.id_usuario === usuario.id_usuario;
}

function pintar() {
  const totalKg = recolecciones.reduce((suma, r) => suma + (r.clasificacion !== 'RECHAZADO' ? r.peso_kg : 0), 0);
  document.getElementById('resumen').textContent =
    `${recolecciones.length} registro(s) · ${UI.numero(totalKg)} kg aprovechables`;
  if (!recolecciones.length) return UI.sinDatos(tabla, COLUMNAS);

  tabla.innerHTML = recolecciones
    .map(
      (r) => `
      <tr>
        <td class="text-nowrap">${UI.fecha(r.fecha_recoleccion)}</td>
        <td><div class="fw-semibold">${UI.escapar(r.proveedor)}</div><div class="small texto-suave">${UI.escapar(r.municipio)}</div></td>
        <td>${UI.etiqueta(r.tipo_residuo)}</td>
        <td class="numero">${UI.numero(r.peso_kg, 1)}</td>
        <td>${UI.badge(r.clasificacion)}${r.observaciones ? `<div class="small texto-suave text-truncate" style="max-width:180px" title="${UI.escapar(r.observaciones)}">${UI.escapar(r.observaciones)}</div>` : ''}</td>
        <td>${r.pila ? UI.escapar(r.pila) : '<span class="texto-suave small">Sin asignar</span>'}</td>
        <td class="small">${UI.escapar(r.recolector)}</td>
        <td class="acciones">${UI.botonesAccion(r.id_recoleccion, { editar: puedeEditar(r), eliminar: esAdmin })}</td>
      </tr>`
    )
    .join('');
}

tabla.addEventListener('click', (evento) => {
  const boton = evento.target.closest('button[data-accion]');
  if (!boton) return;
  const recoleccion = recolecciones.find((r) => r.id_recoleccion === Number(boton.dataset.id));
  if (boton.dataset.accion === 'editar') abrirFormulario(recoleccion);
  if (boton.dataset.accion === 'eliminar') eliminar(recoleccion);
});

// ---------- Formulario ----------
function llenarListas(recoleccion) {
  // Proveedores activos (+ el actual si fue desactivado después)
  const disponibles = proveedores.filter((p) => p.activo === 'S' || p.id_proveedor === recoleccion?.id_proveedor);
  UI.opciones(formulario.id_proveedor, disponibles, 'id_proveedor', (p) => `${p.nombre} (${p.municipio})`, 'Seleccione...');
  // Pilas que no han finalizado (+ la actual)
  const abiertas = pilas.filter((p) => p.fase !== 'FINALIZADA' || p.id_pila === recoleccion?.id_pila);
  UI.opciones(formulario.id_pila, abiertas, 'id_pila', (p) => `${p.codigo} · ${UI.etiqueta(p.fase)}`, 'Sin asignar');
}

function ajustarSegunClasificacion() {
  const clasificacion = formulario.clasificacion.value;
  const rechazado = clasificacion === 'RECHAZADO';
  formulario.id_pila.disabled = rechazado;
  if (rechazado) formulario.id_pila.value = '';
  document.getElementById('ayudaPila').textContent = rechazado
    ? 'Un residuo rechazado no ingresa a ninguna pila.'
    : 'Opcional. Solo pilas que aún no han finalizado.';
  formulario.observaciones.required = clasificacion !== 'APTO';
  document.getElementById('obsObligatoria').classList.toggle('d-none', clasificacion === 'APTO');
}

formulario.clasificacion.addEventListener('change', ajustarSegunClasificacion);

// Al elegir el proveedor se sugiere su tipo de residuo principal
formulario.id_proveedor.addEventListener('change', () => {
  const proveedor = proveedores.find((p) => p.id_proveedor === Number(formulario.id_proveedor.value));
  if (proveedor && !idEditando) formulario.tipo_residuo.value = proveedor.tipo_residuo;
});

function abrirFormulario(recoleccion = null) {
  idEditando = recoleccion ? recoleccion.id_recoleccion : null;
  formulario.reset();
  UI.limpiarValidacion(formulario);
  llenarListas(recoleccion);
  document.getElementById('tituloModal').textContent = recoleccion ? 'Editar recolección' : 'Registrar recolección';
  if (recoleccion) UI.llenarFormulario(formulario, recoleccion);
  else formulario.fecha_recoleccion.value = UI.hoy();
  ajustarSegunClasificacion();
  modal.show();
}

formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  UI.limpiarValidacion(formulario);
  if (!UI.validar(formulario)) return;

  const datos = UI.datosFormulario(formulario);
  await UI.conCarga(document.getElementById('btnGuardar'), async () => {
    try {
      if (idEditando) await Api.put(`/recolecciones/${idEditando}`, datos);
      else await Api.post('/recolecciones', datos);
      modal.hide();
      UI.toast(idEditando ? 'Recolección actualizada correctamente' : 'Recolección registrada correctamente');
      cargar();
    } catch (error) {
      UI.errorFormulario(formulario, error);
    }
  });
});

async function eliminar(recoleccion) {
  const confirmado = await UI.confirmar(
    `¿Eliminar la recolección de ${UI.numero(recoleccion.peso_kg)} kg de "${recoleccion.proveedor}" del ${UI.fecha(recoleccion.fecha_recoleccion)}?`
  );
  if (!confirmado) return;
  try {
    await Api.eliminar(`/recolecciones/${recoleccion.id_recoleccion}`);
    UI.toast('Recolección eliminada correctamente');
    cargar();
  } catch (error) {
    UI.error(error);
  }
}
