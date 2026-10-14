// Módulo 4 (continuación): monitoreo de pilas - temperatura, humedad, pH y volteos.

const usuario = UI.iniciar({ pagina: 'monitoreo', titulo: 'Monitoreo de pilas' });
const esAdmin = Sesion.esAdmin();
const COLUMNAS = 9;
const COLOR_REFERENCIA = '#898781';

const tabla = document.getElementById('tabla');
const filtros = document.getElementById('formFiltros');
const formulario = document.getElementById('formMonitoreo');
const modal = new bootstrap.Modal('#modalMonitoreo');
let mediciones = [];
let pilas = [];
let idEditando = null;
let graficos = [];

formulario.fecha_monitoreo.max = UI.hoy();

if (usuario) iniciar();

async function iniciar() {
  try {
    pilas = await Api.get('/pilas');
    UI.opciones(filtros.id_pila, pilas, 'id_pila', (p) => `${p.codigo} · ${UI.etiqueta(p.fase)}`, 'Todas las pilas');
    const pilaUrl = UI.parametroUrl('pila');
    if (pilaUrl) filtros.id_pila.value = pilaUrl;
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
    mediciones = await Api.get('/monitoreos', UI.datosFormulario(filtros));
    pintar();
    pintarGraficos();
  } catch (error) {
    UI.sinDatos(tabla, COLUMNAS, 'No fue posible cargar la información');
    UI.error(error);
  }
}

function pintar() {
  document.getElementById('resumen').textContent = `${mediciones.length} medición(es)`;
  if (!mediciones.length) return UI.sinDatos(tabla, COLUMNAS);
  tabla.innerHTML = mediciones
    .map(
      (m) => `
      <tr>
        <td class="text-nowrap">${UI.fecha(m.fecha_monitoreo)}</td>
        <td><span class="fw-semibold">${UI.escapar(m.pila)}</span><div>${UI.badge(m.fase)}</div></td>
        <td class="numero">${UI.numero(m.temperatura, 1)}</td>
        <td class="numero">${UI.numero(m.humedad, 1)}</td>
        <td class="numero">${m.ph !== null ? UI.numero(m.ph, 1) : '—'}</td>
        <td>${m.volteo === 'S' ? '<i class="bi bi-arrow-repeat text-success"></i> Sí' : '<span class="texto-suave">No</span>'}</td>
        <td>${m.alerta
          ? `<span class="text-danger small"><i class="bi bi-exclamation-triangle-fill me-1"></i>${UI.escapar(m.alerta)}</span>`
          : '<span class="text-success small"><i class="bi bi-check-circle me-1"></i>En rango</span>'}</td>
        <td class="small">${UI.escapar(m.usuario)}</td>
        <td class="acciones">${esAdmin ? UI.botonesAccion(m.id_monitoreo) : ''}</td>
      </tr>`
    )
    .join('');
}

// ---------- Curvas de temperatura y humedad (solo con una pila seleccionada) ----------
function lineaReferencia(etiqueta, valor, cantidad) {
  return {
    label: etiqueta,
    data: Array(cantidad).fill(valor),
    borderColor: COLOR_REFERENCIA,
    borderDash: [6, 4],
    borderWidth: 1.5,
    pointRadius: 0,
    pointHoverRadius: 0,
  };
}

function grafico(canvas, etiqueta, valores, fechas, referencias, maximo) {
  return new Chart(canvas, {
    type: 'line',
    data: {
      labels: fechas,
      datasets: [
        {
          label: etiqueta,
          data: valores,
          borderColor: COLORES_SERIE[0],
          backgroundColor: COLORES_SERIE[0],
          borderWidth: 2,
          pointRadius: 4,
          tension: 0.3,
        },
        ...referencias,
      ],
    },
    options: {
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { position: 'top', align: 'end' } },
      scales: { x: { grid: { display: false } }, y: { beginAtZero: true, suggestedMax: maximo } },
    },
  });
}

function pintarGraficos() {
  const seccion = document.getElementById('seccionGraficos');
  graficos.forEach((g) => g.destroy());
  graficos = [];
  const idPila = Number(filtros.id_pila.value);
  if (!idPila || filtros.solo_alertas.checked || mediciones.length < 2) {
    seccion.classList.add('d-none');
    return;
  }
  seccion.classList.remove('d-none');
  const pila = pilas.find((p) => p.id_pila === idPila);
  document.querySelectorAll('.nombrePila').forEach((el) => (el.textContent = pila.codigo));

  const ordenadas = [...mediciones].reverse(); // de la más antigua a la más reciente
  const fechas = ordenadas.map((m) => UI.fecha(m.fecha_monitoreo).slice(0, 5));
  const n = ordenadas.length;
  graficos.push(
    grafico(document.getElementById('graficoTemperatura'), 'Temperatura', ordenadas.map((m) => m.temperatura), fechas,
      [lineaReferencia('Máximo recomendado (70 °C)', 70, n)], 80),
    grafico(document.getElementById('graficoHumedad'), 'Humedad', ordenadas.map((m) => m.humedad), fechas,
      [lineaReferencia('Mínimo (40 %)', 40, n), lineaReferencia('Máximo (65 %)', 65, n)], 80)
  );
}

tabla.addEventListener('click', (evento) => {
  const boton = evento.target.closest('button[data-accion]');
  if (!boton) return;
  const medicion = mediciones.find((m) => m.id_monitoreo === Number(boton.dataset.id));
  if (boton.dataset.accion === 'editar') abrirFormulario(medicion);
  if (boton.dataset.accion === 'eliminar') eliminar(medicion);
});

// ---------- Formulario ----------
function abrirFormulario(medicion = null) {
  idEditando = medicion ? medicion.id_monitoreo : null;
  formulario.reset();
  UI.limpiarValidacion(formulario);
  const abiertas = pilas.filter((p) => p.fase !== 'FINALIZADA' || p.id_pila === medicion?.id_pila);
  UI.opciones(formulario.id_pila, abiertas, 'id_pila', (p) => `${p.codigo} · ${UI.etiqueta(p.fase)}`, 'Seleccione...');
  document.getElementById('tituloModal').textContent = medicion ? 'Editar medición' : 'Registrar medición';
  if (medicion) {
    UI.llenarFormulario(formulario, medicion);
  } else {
    formulario.fecha_monitoreo.value = UI.hoy();
    if (filtros.id_pila.value && abiertas.some((p) => p.id_pila === Number(filtros.id_pila.value))) {
      formulario.id_pila.value = filtros.id_pila.value;
    }
  }
  modal.show();
}

formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  UI.limpiarValidacion(formulario);
  if (!UI.validar(formulario)) return;

  const datos = UI.datosFormulario(formulario);
  await UI.conCarga(document.getElementById('btnGuardar'), async () => {
    try {
      const guardada = idEditando
        ? await Api.put(`/monitoreos/${idEditando}`, datos)
        : await Api.post('/monitoreos', datos);
      modal.hide();
      UI.toast(idEditando ? 'Medición actualizada' : 'Medición registrada');
      if (guardada.alerta) UI.toast(`Alerta en ${guardada.pila}: ${guardada.alerta}`, 'warning');
      cargar();
    } catch (error) {
      UI.errorFormulario(formulario, error);
    }
  });
});

async function eliminar(medicion) {
  const confirmado = await UI.confirmar(`¿Eliminar la medición de la pila ${medicion.pila} del ${UI.fecha(medicion.fecha_monitoreo)}?`);
  if (!confirmado) return;
  try {
    await Api.eliminar(`/monitoreos/${medicion.id_monitoreo}`);
    UI.toast('Medición eliminada correctamente');
    cargar();
  } catch (error) {
    UI.error(error);
  }
}
