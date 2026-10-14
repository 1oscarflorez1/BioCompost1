// Dashboard: indicadores calculados por el backend (GET /api/dashboard).

const usuarioDashboard = UI.iniciar({ pagina: 'dashboard', titulo: 'Dashboard' });
if (usuarioDashboard) {
  document.getElementById('saludo').textContent = `Hola, ${usuarioDashboard.nombre.split(' ')[0]}`;
  cargarDashboard();
}

async function cargarDashboard() {
  try {
    const datos = await Api.get('/dashboard');
    pintarIndicadores(datos.indicadores);
    graficoMensual(datos.por_mes);
    graficoTipos(datos.por_tipo);
    pintarFases(datos.pilas_por_fase);
    pintarAlertas(datos.alertas);
    pintarUltimas(datos.ultimas_recolecciones);
  } catch (error) {
    UI.error(error);
  }
}

function pintarIndicadores(ind) {
  document.getElementById('kpiToneladas').textContent = UI.numero(ind.toneladas_desviadas, 1);
  document.getElementById('kpiAbono').textContent = UI.numero(ind.kg_abono_producido);
  document.getElementById('kpiDisponible').textContent = UI.numero(ind.kg_abono_disponible);
  document.getElementById('kpiConversion').textContent = UI.numero(ind.tasa_conversion_pct, 1);
  document.getElementById('kpiRecoleccionesMes').textContent = UI.numero(ind.recolecciones_mes);
  document.getElementById('kpiKgMes').textContent = UI.numero(ind.kg_mes);
  document.getElementById('kpiPilas').textContent = ind.pilas_activas;
  document.getElementById('kpiProveedores').textContent = ind.proveedores_activos;
}

function graficoMensual(meses) {
  new Chart(document.getElementById('graficoMensual'), {
    type: 'bar',
    data: {
      labels: meses.map((m) => UI.mes(m.mes)),
      datasets: [
        {
          label: 'Residuo desviado (t)',
          data: meses.map((m) => m.toneladas_desviadas),
          backgroundColor: COLORES_SERIE[0],
        },
        {
          label: 'Abono producido (t)',
          data: meses.map((m) => m.kg_abono_producido / 1000),
          backgroundColor: COLORES_SERIE[1],
        },
      ],
    },
    options: {
      datasets: { bar: { borderRadius: 4, maxBarThickness: 28, categoryPercentage: 0.7, barPercentage: 0.9 } },
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'top', align: 'end' },
        tooltip: { callbacks: { label: (c) => `${c.dataset.label.replace(' (t)', '')}: ${UI.numero(c.parsed.y, 2)} t` } },
      },
      scales: {
        x: { grid: { display: false } },
        y: { beginAtZero: true, title: { display: true, text: 'toneladas' }, ticks: { callback: (v) => UI.numero(v, 0) } },
      },
    },
  });
}

function graficoTipos(tipos) {
  new Chart(document.getElementById('graficoTipos'), {
    type: 'bar',
    data: {
      labels: tipos.map((t) => UI.etiqueta(t.tipo_residuo)),
      datasets: [{ label: 'Toneladas', data: tipos.map((t) => t.toneladas), backgroundColor: COLORES_SERIE[0] }],
    },
    options: {
      indexAxis: 'y',
      datasets: { bar: { borderRadius: 4, maxBarThickness: 22 } },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (c) => `${UI.numero(c.parsed.x, 2)} t` } },
      },
      scales: { x: { beginAtZero: true }, y: { grid: { display: false } } },
    },
  });
}

function pintarFases(fases) {
  document.getElementById('listaFases').innerHTML = fases
    .map(
      (f) => `
      <a href="pages/pilas.html?fase=${f.fase}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
        ${UI.badge(f.fase)}
        <span class="fw-semibold">${f.cantidad} ${f.cantidad === 1 ? 'pila' : 'pilas'}</span>
      </a>`
    )
    .join('');
}

function pintarAlertas(alertas) {
  const lista = document.getElementById('listaAlertas');
  if (!alertas.length) {
    lista.innerHTML = `<li class="list-group-item small text-success"><i class="bi bi-check-circle me-1"></i>Todas las pilas activas están en rango</li>`;
    return;
  }
  lista.innerHTML = alertas
    .map(
      (a) => `
      <a href="pages/monitoreo.html?pila=${a.id_pila}" class="list-group-item list-group-item-action small">
        <i class="bi bi-exclamation-triangle-fill text-warning me-1"></i>
        <strong>${UI.escapar(a.codigo)}</strong> · ${UI.escapar(a.alerta)}
        <div class="texto-suave">Última medición: ${UI.fecha(a.fecha)}</div>
      </a>`
    )
    .join('');
}

function pintarUltimas(recolecciones) {
  const tbody = document.getElementById('tablaUltimas');
  if (!recolecciones.length) return UI.sinDatos(tbody, 5, 'Aún no hay recolecciones registradas');
  tbody.innerHTML = recolecciones
    .map(
      (r) => `
      <tr>
        <td>${UI.fecha(r.fecha_recoleccion)}</td>
        <td>${UI.escapar(r.proveedor)}<div class="small texto-suave">${UI.escapar(r.municipio)}</div></td>
        <td>${UI.etiqueta(r.tipo_residuo)}</td>
        <td class="numero">${UI.numero(r.peso_kg)}</td>
        <td>${UI.badge(r.clasificacion)}</td>
      </tr>`
    )
    .join('');
}
