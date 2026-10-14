// Módulo 5: Reportes consolidados (datos calculados en Oracle por el backend).

const usuario = UI.iniciar({ pagina: 'reportes', titulo: 'Reportes' });
const selectAnio = document.getElementById('anio');
const formProveedores = document.getElementById('formProveedores');
let reporteMensual = null;
let reporteProveedores = [];
let graficoMensual = null;

if (usuario) iniciar();

async function iniciar() {
  try {
    const anios = await Api.get('/reportes/anios');
    selectAnio.innerHTML = anios.map((a) => `<option value="${a}">${a}</option>`).join('');
    formProveedores.fecha_desde.value = `${anios[0]}-01-01`;
    formProveedores.fecha_hasta.value = UI.hoy();
    cargarMensual();
    cargarProveedores();
  } catch (error) {
    UI.error(error);
  }
}

// ---------- Reporte mensual ----------
selectAnio.addEventListener('change', cargarMensual);

async function cargarMensual() {
  const tbody = document.getElementById('tablaMensual');
  UI.cargando(tbody, 6);
  try {
    reporteMensual = await Api.get('/reportes/mensual', { anio: selectAnio.value });
    document.getElementById('tituloAnio').textContent = reporteMensual.anio;
    const meses = reporteMensual.meses;
    if (!meses.length) {
      UI.sinDatos(tbody, 6, 'No hay movimientos registrados en este año');
      document.getElementById('totalMensual').innerHTML = '';
    } else {
      tbody.innerHTML = meses
        .map(
          (m) => `
          <tr>
            <td class="text-nowrap">${UI.mes(m.mes)}</td>
            <td class="numero">${m.num_recolecciones}</td>
            <td class="numero">${UI.numero(m.toneladas_desviadas, 2)}</td>
            <td class="numero">${UI.numero(m.toneladas_rechazadas, 2)}</td>
            <td class="numero">${m.num_lotes}</td>
            <td class="numero">${UI.numero(m.kg_abono_producido)}</td>
          </tr>`
        )
        .join('');
      const t = reporteMensual.totales;
      document.getElementById('totalMensual').innerHTML = `
        <tr>
          <td>Total ${reporteMensual.anio}</td>
          <td class="numero">${t.num_recolecciones}</td>
          <td class="numero">${UI.numero(t.toneladas_desviadas, 2)}</td>
          <td class="numero">${UI.numero(t.toneladas_rechazadas, 2)}</td>
          <td class="numero">${t.num_lotes}</td>
          <td class="numero">${UI.numero(t.kg_abono_producido)}</td>
        </tr>`;
    }
    pintarGrafico(meses);
  } catch (error) {
    UI.sinDatos(tbody, 6, 'No fue posible generar el reporte');
    UI.error(error);
  }
}

function pintarGrafico(meses) {
  if (graficoMensual) graficoMensual.destroy();
  graficoMensual = new Chart(document.getElementById('graficoMensual'), {
    type: 'bar',
    data: {
      labels: meses.map((m) => UI.mes(m.mes)),
      datasets: [
        { label: 'Residuo desviado (t)', data: meses.map((m) => m.toneladas_desviadas), backgroundColor: COLORES_SERIE[0] },
        { label: 'Abono producido (t)', data: meses.map((m) => m.kg_abono_producido / 1000), backgroundColor: COLORES_SERIE[1] },
      ],
    },
    options: {
      datasets: { bar: { borderRadius: 4, maxBarThickness: 28, categoryPercentage: 0.7, barPercentage: 0.9 } },
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'top', align: 'end' },
        tooltip: { callbacks: { label: (c) => `${c.dataset.label.replace(' (t)', '')}: ${UI.numero(c.parsed.y, 2)} t` } },
      },
      scales: { x: { grid: { display: false } }, y: { beginAtZero: true, title: { display: true, text: 'toneladas' } } },
    },
  });
}

document.getElementById('btnCsvMensual').addEventListener('click', () => {
  if (!reporteMensual?.meses.length) return UI.toast('No hay datos para exportar', 'warning');
  UI.exportarCSV(`reporte_mensual_${reporteMensual.anio}.csv`, [
    { titulo: 'Mes', campo: 'mes' },
    { titulo: 'Recolecciones', campo: 'num_recolecciones' },
    { titulo: 'Residuo desviado (t)', campo: 'toneladas_desviadas' },
    { titulo: 'Residuo rechazado (t)', campo: 'toneladas_rechazadas' },
    { titulo: 'Lotes producidos', campo: 'num_lotes' },
    { titulo: 'Abono producido (kg)', campo: 'kg_abono_producido' },
  ], reporteMensual.meses);
});

// ---------- Reporte por proveedor ----------
formProveedores.addEventListener('submit', (evento) => {
  evento.preventDefault();
  cargarProveedores();
});

async function cargarProveedores() {
  const tbody = document.getElementById('tablaProveedores');
  if (!UI.validar(formProveedores)) return;
  if (formProveedores.fecha_hasta.value < formProveedores.fecha_desde.value) {
    return UI.toast('La fecha final no puede ser anterior a la inicial', 'warning');
  }
  UI.cargando(tbody, 7);
  try {
    reporteProveedores = await Api.get('/reportes/proveedores', UI.datosFormulario(formProveedores));
    const total = reporteProveedores.reduce((suma, p) => suma + p.kg_aprovechados, 0);
    reporteProveedores.forEach((p) => (p.porcentaje = total ? (p.kg_aprovechados / total) * 100 : 0));
    tbody.innerHTML = reporteProveedores
      .map(
        (p) => `
        <tr>
          <td class="fw-semibold">${UI.escapar(p.proveedor)}</td>
          <td>${UI.etiqueta(p.tipo_proveedor)}</td>
          <td>${UI.escapar(p.municipio)}</td>
          <td class="numero">${p.num_recolecciones}</td>
          <td class="numero">${UI.numero(p.kg_aprovechados)}</td>
          <td class="numero">${UI.numero(p.kg_rechazados)}</td>
          <td class="numero">${UI.numero(p.porcentaje, 1)} %</td>
        </tr>`
      )
      .join('');
  } catch (error) {
    UI.sinDatos(tbody, 7, 'No fue posible generar el reporte');
    UI.error(error);
  }
}

document.getElementById('btnCsvProveedores').addEventListener('click', () => {
  if (!reporteProveedores.length) return UI.toast('No hay datos para exportar', 'warning');
  UI.exportarCSV('reporte_proveedores.csv', [
    { titulo: 'Proveedor', campo: 'proveedor' },
    { titulo: 'Tipo', valor: (p) => UI.etiqueta(p.tipo_proveedor) },
    { titulo: 'Municipio', campo: 'municipio' },
    { titulo: 'Recolecciones', campo: 'num_recolecciones' },
    { titulo: 'Aprovechado (kg)', campo: 'kg_aprovechados' },
    { titulo: 'Rechazado (kg)', campo: 'kg_rechazados' },
    { titulo: '% del total', valor: (p) => p.porcentaje.toFixed(1) },
  ], reporteProveedores);
});
