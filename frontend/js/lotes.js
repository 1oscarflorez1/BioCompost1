// Lotes de abono producidos y trazabilidad hasta los proveedores de origen.

const usuario = UI.iniciar({ pagina: 'lotes', titulo: 'Lotes de abono' });
const esAdmin = Sesion.esAdmin();
const COLUMNAS = 8;

const tabla = document.getElementById('tabla');
const filtros = document.getElementById('formFiltros');
const formulario = document.getElementById('formLote');
const modal = new bootstrap.Modal('#modalLote');
const modalTraza = new bootstrap.Modal('#modalTrazabilidad');
let lotes = [];
let pilas = [];
let idEditando = null;

UI.opcionesCatalogo(filtros.calidad, CATALOGOS.calidad, 'Todas');
UI.opcionesCatalogo(filtros.estado, CATALOGOS.estadoLote, 'Todos');
UI.opcionesCatalogo(formulario.calidad, CATALOGOS.calidad);
UI.opcionesCatalogo(formulario.estado, CATALOGOS.estadoLote);
formulario.fecha_produccion.max = UI.hoy();

if (usuario) iniciar();

async function iniciar() {
  try {
    pilas = await Api.get('/pilas');
    UI.opciones(filtros.id_pila, pilas, 'id_pila', (p) => p.codigo, 'Todas');
    cargar();
  } catch (error) {
    UI.error(error);
  }
}

filtros.addEventListener('input', UI.esperar(cargar));
filtros.addEventListener('submit', (evento) => evento.preventDefault());
document.getElementById('btnNuevo')?.addEventListener('click', () => abrirFormulario());

async function cargar() {
  UI.cargando(tabla, COLUMNAS);
  try {
    lotes = await Api.get('/lotes', UI.datosFormulario(filtros));
    pintar();
  } catch (error) {
    UI.sinDatos(tabla, COLUMNAS, 'No fue posible cargar la información');
    UI.error(error);
  }
}

function pintar() {
  const total = lotes.reduce((suma, l) => suma + l.kilos_producidos, 0);
  const disponible = lotes.filter((l) => l.estado === 'DISPONIBLE').reduce((suma, l) => suma + l.kilos_producidos, 0);
  document.getElementById('resumen').textContent =
    `${lotes.length} lote(s) · ${UI.numero(total)} kg producidos · ${UI.numero(disponible)} kg disponibles`;
  if (!lotes.length) return UI.sinDatos(tabla, COLUMNAS);
  tabla.innerHTML = lotes
    .map((l) => {
      const botonTraza = `<button class="btn btn-sm btn-outline-secondary" data-accion="traza" data-id="${l.id_lote}" title="Ver trazabilidad"><i class="bi bi-diagram-3"></i></button>`;
      return `
      <tr>
        <td class="fw-semibold">${UI.escapar(l.codigo_lote)}</td>
        <td>${UI.escapar(l.pila)}</td>
        <td class="text-nowrap">${UI.fecha(l.fecha_produccion)}</td>
        <td class="numero">${UI.numero(l.kilos_producidos)}</td>
        <td>${UI.badge(l.calidad)}</td>
        <td>${UI.badge(l.estado)}</td>
        <td class="small texto-suave">${UI.escapar(l.observaciones || '')}</td>
        <td class="acciones">${UI.botonesAccion(l.id_lote, { editar: esAdmin, eliminar: esAdmin, extra: botonTraza })}</td>
      </tr>`;
    })
    .join('');
}

tabla.addEventListener('click', (evento) => {
  const boton = evento.target.closest('button[data-accion]');
  if (!boton) return;
  const lote = lotes.find((l) => l.id_lote === Number(boton.dataset.id));
  if (boton.dataset.accion === 'traza') verTrazabilidad(lote);
  if (boton.dataset.accion === 'editar') abrirFormulario(lote);
  if (boton.dataset.accion === 'eliminar') eliminar(lote);
});

// ---------- Trazabilidad: lote -> pila -> recolecciones -> proveedores ----------
async function verTrazabilidad(lote) {
  const contenido = document.getElementById('contenidoTraza');
  document.getElementById('tituloTraza').textContent = `Trazabilidad del lote ${lote.codigo_lote}`;
  contenido.innerHTML = '<div class="text-center py-4"><span class="spinner-border"></span></div>';
  modalTraza.show();
  try {
    const t = await Api.get(`/lotes/${lote.id_lote}/trazabilidad`);
    const filas = t.recolecciones
      .map(
        (r) => `
        <tr>
          <td class="text-nowrap">${UI.fecha(r.fecha_recoleccion)}</td>
          <td>${UI.escapar(r.proveedor)}<div class="small texto-suave">${UI.etiqueta(r.tipo_proveedor)} · ${UI.escapar(r.municipio)}</div></td>
          <td>${UI.etiqueta(r.tipo_residuo)}</td>
          <td class="numero">${UI.numero(r.peso_kg)}</td>
          <td>${UI.badge(r.clasificacion)}</td>
        </tr>`
      )
      .join('');
    contenido.innerHTML = `
      <div class="d-flex flex-wrap align-items-center gap-2 mb-3 small">
        <span class="badge text-bg-light border p-2"><i class="bi bi-shop me-1"></i>${t.num_proveedores} proveedores</span>
        <i class="bi bi-arrow-right"></i>
        <span class="badge text-bg-light border p-2"><i class="bi bi-truck me-1"></i>${t.recolecciones.length} recolecciones · ${UI.numero(t.kg_residuo_pila)} kg</span>
        <i class="bi bi-arrow-right"></i>
        <span class="badge text-bg-light border p-2"><i class="bi bi-layers me-1"></i>Pila ${UI.escapar(t.lote.pila)}</span>
        <i class="bi bi-arrow-right"></i>
        <span class="badge text-bg-success p-2"><i class="bi bi-box-seam me-1"></i>${UI.escapar(t.lote.codigo_lote)} · ${UI.numero(t.lote.kilos_producidos)} kg</span>
      </div>
      <p class="small texto-suave">La pila ${UI.escapar(t.lote.pila)} produjo ${UI.numero(t.kg_abono_pila)} kg de abono en total,
         un rendimiento de <strong>${UI.numero(t.rendimiento_pct, 1)} %</strong> sobre el residuo recibido.</p>
      <div class="table-responsive">
        <table class="table table-sm align-middle">
          <thead><tr><th>Fecha</th><th>Proveedor de origen</th><th>Residuo</th><th class="numero">Kg</th><th>Clasificación</th></tr></thead>
          <tbody>${filas || '<tr><td colspan="5" class="texto-suave">La pila no tiene recolecciones asociadas</td></tr>'}</tbody>
        </table>
      </div>`;
  } catch (error) {
    contenido.innerHTML = `<div class="alert alert-danger">${UI.escapar(error.message)}</div>`;
  }
}

// ---------- Formulario ----------
function abrirFormulario(lote = null) {
  idEditando = lote ? lote.id_lote : null;
  formulario.reset();
  UI.limpiarValidacion(formulario);
  const aptas = pilas.filter((p) => ['MADURACION', 'FINALIZADA'].includes(p.fase) || p.id_pila === lote?.id_pila);
  UI.opciones(formulario.id_pila, aptas, 'id_pila',
    (p) => `${p.codigo} · ${UI.etiqueta(p.fase)} · ${UI.numero(p.kg_recibidos)} kg recibidos`, 'Seleccione...');
  document.getElementById('tituloModal').textContent = lote ? `Editar lote ${lote.codigo_lote}` : 'Registrar lote';
  if (lote) UI.llenarFormulario(formulario, lote);
  else formulario.fecha_produccion.value = UI.hoy();
  modal.show();
}

formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  UI.limpiarValidacion(formulario);
  if (!UI.validar(formulario)) return;

  const datos = UI.datosFormulario(formulario);
  await UI.conCarga(document.getElementById('btnGuardar'), async () => {
    try {
      if (idEditando) await Api.put(`/lotes/${idEditando}`, datos);
      else await Api.post('/lotes', datos);
      modal.hide();
      UI.toast(idEditando ? 'Lote actualizado correctamente' : 'Lote registrado correctamente');
      cargar();
    } catch (error) {
      UI.errorFormulario(formulario, error);
    }
  });
});

async function eliminar(lote) {
  if (!(await UI.confirmar(`¿Eliminar el lote ${lote.codigo_lote} (${UI.numero(lote.kilos_producidos)} kg)?`))) return;
  try {
    await Api.eliminar(`/lotes/${lote.id_lote}`);
    UI.toast('Lote eliminado correctamente');
    cargar();
  } catch (error) {
    UI.error(error);
  }
}
