// Módulo 4: Control de pilas de compostaje (CRUD + filtro por fase de maduración).

const usuario = UI.iniciar({ pagina: 'pilas', titulo: 'Pilas de compostaje' });
const esAdmin = Sesion.esAdmin();
const COLUMNAS = 8;

const tabla = document.getElementById('tabla');
const formulario = document.getElementById('formPila');
const modal = new bootstrap.Modal('#modalPila');
let pilas = [];
let faseSeleccionada = UI.parametroUrl('fase') || '';
let idEditando = null;

UI.opcionesCatalogo(formulario.fase, CATALOGOS.fase);
formulario.fecha_inicio.max = UI.hoy();
formulario.fecha_fin.max = UI.hoy();

if (usuario) {
  contarFases();
  cargar();
}

document.getElementById('fTexto').addEventListener('input', UI.esperar(cargar));
document.getElementById('btnNuevo')?.addEventListener('click', () => abrirFormulario());

// Botones de fase con la cantidad de pilas en cada una
async function contarFases() {
  try {
    const todas = await Api.get('/pilas');
    const conteo = (fase) => todas.filter((p) => !fase || p.fase === fase).length;
    const fases = ['', ...CATALOGOS.fase];
    document.getElementById('botonesFase').innerHTML = fases
      .map((fase) => {
        const activo = fase === faseSeleccionada ? 'btn-primary' : 'btn-outline-primary';
        return `<button type="button" class="btn btn-sm ${activo}" data-fase="${fase}">
                  ${fase ? UI.etiqueta(fase) : 'Todas'} <span class="badge text-bg-light ms-1">${conteo(fase)}</span>
                </button>`;
      })
      .join('');
  } catch (error) {
    UI.error(error);
  }
}

document.getElementById('botonesFase').addEventListener('click', (evento) => {
  const boton = evento.target.closest('button[data-fase]');
  if (!boton) return;
  faseSeleccionada = boton.dataset.fase;
  document.querySelectorAll('#botonesFase button').forEach((b) => {
    b.classList.toggle('btn-primary', b === boton);
    b.classList.toggle('btn-outline-primary', b !== boton);
  });
  cargar();
});

async function cargar() {
  UI.cargando(tabla, COLUMNAS);
  try {
    // El filtro por fase lo resuelve el backend: GET /api/pilas?fase=...
    pilas = await Api.get('/pilas', { fase: faseSeleccionada, texto: document.getElementById('fTexto').value.trim() });
    pintar();
  } catch (error) {
    UI.sinDatos(tabla, COLUMNAS, 'No fue posible cargar la información');
    UI.error(error);
  }
}

function barraCapacidad(pila) {
  if (!pila.capacidad_kg) return `${UI.numero(pila.kg_recibidos)} kg`;
  const porcentaje = Math.min(100, Math.round((pila.kg_recibidos / pila.capacidad_kg) * 100));
  return `
    <div class="small">${UI.numero(pila.kg_recibidos)} / ${UI.numero(pila.capacidad_kg)} kg</div>
    <div class="progress barra-capacidad" role="progressbar" aria-label="Capacidad usada" aria-valuenow="${porcentaje}" aria-valuemin="0" aria-valuemax="100">
      <div class="progress-bar bg-success" style="width:${porcentaje}%"></div>
    </div>`;
}

function ultimaMedicion(pila) {
  if (!pila.ultimo_monitoreo) return '<span class="small texto-suave">Sin mediciones</span>';
  const alerta = pila.alerta
    ? `<div class="small text-danger"><i class="bi bi-exclamation-triangle-fill me-1"></i>${UI.escapar(pila.alerta)}</div>`
    : '';
  return `<div class="small"><i class="bi bi-thermometer-half"></i> ${UI.numero(pila.ultima_temperatura, 1)} °C ·
          <i class="bi bi-droplet"></i> ${UI.numero(pila.ultima_humedad, 1)} %</div>
          <div class="small texto-suave">${UI.fecha(pila.ultimo_monitoreo)}</div>${alerta}`;
}

function pintar() {
  document.getElementById('resumen').textContent = `${pilas.length} pila(s)`;
  if (!pilas.length) return UI.sinDatos(tabla, COLUMNAS, 'No hay pilas en esta fase');
  tabla.innerHTML = pilas
    .map((p) => {
      const verMonitoreo = `<a class="btn btn-sm btn-outline-secondary" href="monitoreo.html?pila=${p.id_pila}" title="Ver monitoreo"><i class="bi bi-graph-up"></i></a>`;
      return `
      <tr>
        <td><div class="fw-semibold text-nowrap">${UI.escapar(p.codigo)}</div><div class="small texto-suave">${UI.escapar(p.ubicacion || '')}</div></td>
        <td>${UI.badge(p.fase)}</td>
        <td class="text-nowrap">${UI.fecha(p.fecha_inicio)}${p.fecha_fin ? `<div class="small texto-suave">Fin: ${UI.fecha(p.fecha_fin)}</div>` : ''}</td>
        <td class="numero">${p.dias_proceso}</td>
        <td>${barraCapacidad(p)}<div class="small texto-suave">${p.num_recolecciones} entradas</div></td>
        <td>${ultimaMedicion(p)}</td>
        <td class="numero">${p.kg_abono ? UI.numero(p.kg_abono) : '—'}</td>
        <td class="acciones">${UI.botonesAccion(p.id_pila, { editar: esAdmin, eliminar: esAdmin, extra: verMonitoreo })}</td>
      </tr>`;
    })
    .join('');
}

tabla.addEventListener('click', (evento) => {
  const boton = evento.target.closest('button[data-accion]');
  if (!boton) return;
  const pila = pilas.find((p) => p.id_pila === Number(boton.dataset.id));
  if (boton.dataset.accion === 'editar') abrirFormulario(pila);
  if (boton.dataset.accion === 'eliminar') eliminar(pila);
});

// ---------- Formulario ----------
function ajustarFechaFin() {
  const finalizada = formulario.fase.value === 'FINALIZADA';
  document.getElementById('grupoFechaFin').classList.toggle('d-none', !finalizada);
  formulario.fecha_fin.required = finalizada;
  formulario.fecha_fin.disabled = !finalizada;
  formulario.fecha_fin.min = formulario.fecha_inicio.value; // no puede terminar antes de empezar
  if (finalizada && !formulario.fecha_fin.value) formulario.fecha_fin.value = UI.hoy();
}
formulario.fase.addEventListener('change', ajustarFechaFin);
formulario.fecha_inicio.addEventListener('change', () => (formulario.fecha_fin.min = formulario.fecha_inicio.value));

function abrirFormulario(pila = null) {
  idEditando = pila ? pila.id_pila : null;
  formulario.reset();
  UI.limpiarValidacion(formulario);
  document.getElementById('tituloModal').textContent = pila ? `Editar pila ${pila.codigo}` : 'Nueva pila';
  if (pila) UI.llenarFormulario(formulario, pila);
  else formulario.fecha_inicio.value = UI.hoy();
  ajustarFechaFin();
  modal.show();
}

formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  UI.limpiarValidacion(formulario);
  if (!UI.validar(formulario)) return;

  const datos = UI.datosFormulario(formulario);
  await UI.conCarga(document.getElementById('btnGuardar'), async () => {
    try {
      if (idEditando) await Api.put(`/pilas/${idEditando}`, datos);
      else await Api.post('/pilas', datos);
      modal.hide();
      UI.toast(idEditando ? 'Pila actualizada correctamente' : 'Pila creada correctamente');
      contarFases();
      cargar();
    } catch (error) {
      UI.errorFormulario(formulario, error);
    }
  });
});

async function eliminar(pila) {
  const confirmado = await UI.confirmar(
    `¿Eliminar la pila ${pila.codigo}? Se eliminarán sus mediciones y sus recolecciones quedarán sin pila asignada.`
  );
  if (!confirmado) return;
  try {
    await Api.eliminar(`/pilas/${pila.id_pila}`);
    UI.toast('Pila eliminada correctamente');
    contarFases();
    cargar();
  } catch (error) {
    UI.error(error);
  }
}
