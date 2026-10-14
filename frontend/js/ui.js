// Utilidades de interfaz compartidas por todas las páginas:
// menú lateral, mensajes (toasts), confirmaciones, formatos y formularios.

const MENU = [
  { seccion: 'General' },
  { id: 'dashboard', texto: 'Dashboard', icono: 'speedometer2', url: 'index.html' },
  { seccion: 'Operación' },
  { id: 'proveedores', texto: 'Proveedores', icono: 'shop', url: 'pages/proveedores.html' },
  { id: 'recolecciones', texto: 'Recolecciones', icono: 'truck', url: 'pages/recolecciones.html' },
  { seccion: 'Compostaje' },
  { id: 'pilas', texto: 'Pilas de compostaje', icono: 'layers', url: 'pages/pilas.html' },
  { id: 'monitoreo', texto: 'Monitoreo de pilas', icono: 'thermometer-half', url: 'pages/monitoreo.html' },
  { id: 'lotes', texto: 'Lotes de abono', icono: 'box-seam', url: 'pages/lotes.html' },
  { seccion: 'Análisis' },
  { id: 'reportes', texto: 'Reportes', icono: 'file-earmark-bar-graph', url: 'pages/reportes.html' },
  { seccion: 'Administración', soloAdmin: true },
  { id: 'usuarios', texto: 'Usuarios y roles', icono: 'people', url: 'pages/usuarios.html', soloAdmin: true },
];

// Textos legibles para los códigos que guarda la base de datos
const ETIQUETAS = {
  PLAZA_MERCADO: 'Plaza de mercado', FINCA: 'Finca', AGROINDUSTRIA: 'Agroindustria',
  FRUTAS: 'Frutas', HORTALIZAS: 'Hortalizas', ESTIERCOL: 'Estiércol', BAGAZO: 'Bagazo', MIXTO: 'Mixto',
  APTO: 'Apto', CONDICIONADO: 'Condicionado', RECHAZADO: 'Rechazado',
  MESOFILICA: 'Mesofílica', TERMOFILICA: 'Termofílica', ENFRIAMIENTO: 'Enfriamiento',
  MADURACION: 'Maduración', FINALIZADA: 'Finalizada',
  PREMIUM: 'Premium', ESTANDAR: 'Estándar', REPROCESO: 'Reproceso',
  DISPONIBLE: 'Disponible', DESPACHADO: 'Despachado',
  ADMINISTRADOR: 'Administrador', RECOLECTOR: 'Recolector',
  S: 'Activo', N: 'Inactivo',
};

const COLORES = {
  APTO: 'success', CONDICIONADO: 'warning', RECHAZADO: 'danger',
  MESOFILICA: 'warning', TERMOFILICA: 'danger', ENFRIAMIENTO: 'info', MADURACION: 'primary', FINALIZADA: 'secondary',
  PREMIUM: 'success', ESTANDAR: 'info', REPROCESO: 'warning',
  DISPONIBLE: 'success', DESPACHADO: 'secondary',
  ADMINISTRADOR: 'primary', RECOLECTOR: 'info', S: 'success', N: 'secondary',
};

const CATALOGOS = {
  tipoProveedor: ['PLAZA_MERCADO', 'FINCA', 'AGROINDUSTRIA'],
  tipoResiduo: ['FRUTAS', 'HORTALIZAS', 'ESTIERCOL', 'BAGAZO', 'MIXTO'],
  clasificacion: ['APTO', 'CONDICIONADO', 'RECHAZADO'],
  fase: ['MESOFILICA', 'TERMOFILICA', 'ENFRIAMIENTO', 'MADURACION', 'FINALIZADA'],
  calidad: ['PREMIUM', 'ESTANDAR', 'REPROCESO'],
  estadoLote: ['DISPONIBLE', 'DESPACHADO'],
};

const UI = {
  // ---------------------------------------------------------------
  // Inicio de página: valida la sesión y dibuja el menú
  // ---------------------------------------------------------------
  iniciar({ pagina, titulo, soloAdmin = false }) {
    if (!Sesion.token() || Sesion.expirada()) {
      Sesion.cerrar(Sesion.token() ? 'Su sesión expiró. Inicie sesión nuevamente.' : null);
      return null;
    }
    const usuario = Sesion.usuario();
    this.dibujarMenu(pagina, usuario);
    this.dibujarBarraSuperior(titulo, usuario);
    document.title = `${titulo} | BioCompost`;

    // Oculta los elementos que solo puede usar el administrador
    if (!Sesion.esAdmin()) document.querySelectorAll('[data-solo-admin]').forEach((el) => el.remove());

    if (soloAdmin && !Sesion.esAdmin()) {
      document.querySelector('main').innerHTML = `
        <div class="alert alert-warning d-flex gap-2 align-items-start">
          <i class="bi bi-shield-lock fs-4"></i>
          <div><strong>Acceso restringido.</strong><br>Este módulo solo está disponible para el Administrador de planta.</div>
        </div>`;
      return null;
    }
    return usuario;
  },

  dibujarMenu(pagina, usuario) {
    const sidebar = document.getElementById('sidebar');
    const enlaces = MENU.filter((item) => !item.soloAdmin || usuario.rol === 'ADMINISTRADOR')
      .map((item) => {
        if (item.seccion) return `<div class="seccion">${item.seccion}</div>`;
        const activo = item.id === pagina ? 'active' : '';
        return `<a class="nav-link ${activo}" href="${BASE}${item.url}"><i class="bi bi-${item.icono}"></i>${item.texto}</a>`;
      })
      .join('');
    const marca = `<a class="marca" href="${BASE}index.html"><img src="${BASE}assets/logo.svg" alt="">BioCompost</a>`;

    sidebar.innerHTML = `
      <div class="offcanvas-header p-0 pe-3">
        ${marca}
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" data-bs-target="#sidebar" aria-label="Cerrar"></button>
      </div>
      <div class="offcanvas-body d-flex flex-column p-0 h-100">
        <div class="d-none d-lg-block">${marca}</div>
        <nav class="nav flex-column pb-3">${enlaces}</nav>
        <div class="usuario mt-auto">
          <div class="fw-semibold text-truncate">${this.escapar(usuario.nombre)}</div>
          <div class="small text-white-50 mb-2">${this.escapar(usuario.rol_nombre || this.etiqueta(usuario.rol))}</div>
          <button class="btn btn-sm btn-outline-light w-100" id="btnSalir"><i class="bi bi-box-arrow-right me-1"></i>Cerrar sesión</button>
        </div>
      </div>`;
    document.getElementById('btnSalir').addEventListener('click', () => Sesion.cerrar('Sesión cerrada correctamente.'));
  },

  dibujarBarraSuperior(titulo, usuario) {
    document.getElementById('topbar').innerHTML = `
      <button class="btn btn-outline-secondary btn-sm d-lg-none" data-bs-toggle="offcanvas" data-bs-target="#sidebar" aria-label="Abrir menú">
        <i class="bi bi-list fs-5"></i>
      </button>
      <h1>${titulo}</h1>
      <div class="ms-auto d-flex align-items-center gap-2 small">
        <span class="d-none d-sm-inline texto-suave">${this.escapar(usuario.nombre)}</span>
        ${this.badge(usuario.rol, usuario.rol_nombre)}
      </div>`;
  },

  // ---------------------------------------------------------------
  // Mensajes al usuario
  // ---------------------------------------------------------------
  toast(mensaje, tipo = 'success') {
    const iconos = { success: 'check-circle-fill', danger: 'x-circle-fill', warning: 'exclamation-triangle-fill', info: 'info-circle-fill' };
    let contenedor = document.getElementById('toasts');
    if (!contenedor) {
      contenedor = document.createElement('div');
      contenedor.id = 'toasts';
      contenedor.className = 'toast-container position-fixed top-0 end-0 p-3';
      document.body.appendChild(contenedor);
    }
    const cierreBlanco = tipo === 'warning' ? '' : 'btn-close-white';
    const elemento = document.createElement('div');
    elemento.className = `toast align-items-center text-bg-${tipo} border-0`;
    elemento.setAttribute('role', 'alert');
    elemento.innerHTML = `
      <div class="d-flex">
        <div class="toast-body"><i class="bi bi-${iconos[tipo]} me-2"></i>${this.escapar(mensaje)}</div>
        <button type="button" class="btn-close ${cierreBlanco} me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button>
      </div>`;
    contenedor.appendChild(elemento);
    const toast = new bootstrap.Toast(elemento, { delay: tipo === 'danger' ? 6000 : 3500 });
    elemento.addEventListener('hidden.bs.toast', () => elemento.remove());
    toast.show();
  },

  error(error) {
    this.toast(error.message || 'Ocurrió un error inesperado', error.estado === 403 ? 'warning' : 'danger');
  },

  confirmar(mensaje, { titulo = 'Confirmar acción', boton = 'Eliminar', tipo = 'danger' } = {}) {
    return new Promise((resolver) => {
      const div = document.createElement('div');
      div.className = 'modal fade';
      div.tabIndex = -1;
      div.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header"><h5 class="modal-title">${titulo}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button></div>
            <div class="modal-body">${this.escapar(mensaje)}</div>
            <div class="modal-footer">
              <button type="button" class="btn btn-light" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" class="btn btn-${tipo}" data-aceptar>${boton}</button>
            </div>
          </div>
        </div>`;
      document.body.appendChild(div);
      const modal = new bootstrap.Modal(div);
      let aceptado = false;
      div.querySelector('[data-aceptar]').addEventListener('click', () => {
        aceptado = true;
        modal.hide();
      });
      div.addEventListener('hidden.bs.modal', () => {
        div.remove();
        resolver(aceptado);
      });
      modal.show();
    });
  },

  // ---------------------------------------------------------------
  // Formatos
  // ---------------------------------------------------------------
  escapar(texto) {
    const mapa = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
    return String(texto ?? '').replace(/[&<>"']/g, (c) => mapa[c]);
  },

  fecha(valor) {
    if (!valor) return '—';
    const [anio, mes, dia] = String(valor).slice(0, 10).split('-');
    return `${dia}/${mes}/${anio}`;
  },

  numero(valor, decimales = 0) {
    if (valor === null || valor === undefined || valor === '') return '—';
    return Number(valor).toLocaleString('es-CO', { minimumFractionDigits: decimales, maximumFractionDigits: decimales });
  },

  // "2026-05" -> "May 2026"
  mes(texto) {
    const nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    const [anio, mes] = texto.split('-').map(Number);
    return `${nombres[mes - 1]} ${anio}`;
  },

  etiqueta(codigo) {
    return ETIQUETAS[codigo] || codigo || '—';
  },

  // El color sale del código; el texto puede venir aparte (ej. el nombre editable de un rol)
  badge(codigo, texto) {
    const color = COLORES[codigo] || 'secondary';
    return `<span class="badge rounded-pill bg-${color}-subtle text-${color}-emphasis border border-${color}-subtle">${this.escapar(texto || this.etiqueta(codigo))}</span>`;
  },

  hoy() {
    const ahora = new Date();
    return new Date(ahora.getTime() - ahora.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  },

  // ---------------------------------------------------------------
  // Tablas y listas desplegables
  // ---------------------------------------------------------------
  filaMensaje(tbody, columnas, html) {
    tbody.innerHTML = `<tr><td colspan="${columnas}" class="text-center py-4 texto-suave">${html}</td></tr>`;
  },

  cargando(tbody, columnas) {
    this.filaMensaje(tbody, columnas, '<span class="spinner-border spinner-border-sm me-2"></span>Cargando...');
  },

  sinDatos(tbody, columnas, mensaje = 'No se encontraron registros con los filtros aplicados') {
    this.filaMensaje(tbody, columnas, `<i class="bi bi-inbox me-1"></i>${mensaje}`);
  },

  // Botones de editar / eliminar de cada fila (se leen con data-accion y data-id)
  botonesAccion(id, { editar = true, eliminar = true, extra = '' } = {}) {
    const botonEditar = editar
      ? `<button class="btn btn-sm btn-outline-primary" data-accion="editar" data-id="${id}" title="Editar"><i class="bi bi-pencil"></i></button>`
      : '';
    const botonEliminar = eliminar
      ? `<button class="btn btn-sm btn-outline-danger" data-accion="eliminar" data-id="${id}" title="Eliminar"><i class="bi bi-trash"></i></button>`
      : '';
    return `${extra} ${botonEditar} ${botonEliminar}`;
  },

  // Lee los parámetros de la URL, ej. pilas.html?fase=TERMOFILICA
  parametroUrl(nombre) {
    return new URLSearchParams(location.search).get(nombre);
  },

  opcionesCatalogo(select, codigos, textoVacio) {
    const vacia = textoVacio !== undefined ? `<option value="">${textoVacio}</option>` : '';
    select.innerHTML = vacia + codigos.map((c) => `<option value="${c}">${this.etiqueta(c)}</option>`).join('');
  },

  opciones(select, elementos, campoValor, textoOpcion, textoVacio) {
    const vacia = textoVacio !== undefined ? `<option value="">${textoVacio}</option>` : '';
    select.innerHTML = vacia + elementos
      .map((e) => `<option value="${this.escapar(e[campoValor])}">${this.escapar(textoOpcion(e))}</option>`)
      .join('');
  },

  // ---------------------------------------------------------------
  // Formularios
  // ---------------------------------------------------------------
  // Lee el formulario como objeto. Los campos vacíos se envían como null.
  datosFormulario(formulario) {
    const datos = {};
    for (const campo of formulario.elements) {
      if (!campo.name || campo.disabled) continue;
      if (campo.type === 'checkbox') {
        datos[campo.name] = campo.checked ? campo.value : campo.dataset.apagado ?? null;
        continue;
      }
      let valor = campo.value.trim();
      if (valor === '') valor = null;
      else if (campo.type === 'number' || campo.dataset.tipo === 'numero') valor = Number(valor);
      datos[campo.name] = valor;
    }
    return datos;
  },

  llenarFormulario(formulario, datos) {
    for (const campo of formulario.elements) {
      if (!campo.name || !(campo.name in datos)) continue;
      const valor = datos[campo.name];
      if (campo.type === 'checkbox') campo.checked = valor === campo.value;
      else if (campo.type === 'date') campo.value = valor ? String(valor).slice(0, 10) : '';
      else campo.value = valor ?? '';
    }
  },

  // Validación del navegador (HTML5 + estilos de Bootstrap)
  validar(formulario) {
    formulario.classList.add('was-validated');
    return formulario.checkValidity();
  },

  limpiarValidacion(formulario) {
    formulario.classList.remove('was-validated');
    formulario.querySelectorAll('.is-invalid').forEach((campo) => campo.classList.remove('is-invalid'));
    formulario.querySelectorAll('.invalid-feedback[data-original]').forEach((fb) => {
      fb.textContent = fb.dataset.original;
    });
    const alerta = formulario.querySelector('[data-alerta]');
    if (alerta) alerta.classList.add('d-none');
  },

  // Muestra en el formulario el error que devolvió el backend
  errorFormulario(formulario, error) {
    formulario.classList.remove('was-validated');
    const alerta = formulario.querySelector('[data-alerta]');
    if (alerta) {
      alerta.textContent = error.message;
      alerta.classList.remove('d-none');
    } else {
      this.error(error);
    }
    for (const { campo, mensaje } of error.errores || []) {
      const entrada = formulario.elements[campo];
      if (!entrada || !entrada.classList) continue;
      entrada.classList.add('is-invalid');
      const retro = entrada.parentElement.querySelector('.invalid-feedback');
      if (retro) {
        if (!retro.dataset.original) retro.dataset.original = retro.textContent;
        retro.textContent = mensaje;
      }
    }
  },

  // Bloquea el botón mientras se guarda
  async conCarga(boton, accion) {
    const textoOriginal = boton.innerHTML;
    boton.disabled = true;
    boton.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Guardando...';
    try {
      return await accion();
    } finally {
      boton.disabled = false;
      boton.innerHTML = textoOriginal;
    }
  },

  esperar(funcion, milisegundos = 350) {
    let temporizador;
    return (...argumentos) => {
      clearTimeout(temporizador);
      temporizador = setTimeout(() => funcion(...argumentos), milisegundos);
    };
  },

  // ---------------------------------------------------------------
  // Exportar a CSV (se abre en Excel)
  // ---------------------------------------------------------------
  exportarCSV(nombreArchivo, columnas, filas) {
    const celda = (valor) => `"${String(valor ?? '').replace(/"/g, '""')}"`;
    const lineas = [
      columnas.map((c) => celda(c.titulo)).join(';'),
      ...filas.map((fila) => columnas.map((c) => celda(c.valor ? c.valor(fila) : fila[c.campo])).join(';')),
    ];
    const archivo = new Blob(['﻿' + lineas.join('\r\n')], { type: 'text/csv;charset=utf-8' });
    const enlace = document.createElement('a');
    enlace.href = URL.createObjectURL(archivo);
    enlace.download = nombreArchivo;
    enlace.click();
    URL.revokeObjectURL(enlace.href);
  },
};

// ---------------------------------------------------------------
// Configuración común de los gráficos (Chart.js)
// ---------------------------------------------------------------
const COLORES_SERIE = ['#2a78d6', '#eb6834', '#1baf7a'];

function configurarGraficos() {
  if (typeof Chart === 'undefined') return;
  Chart.defaults.font.family = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif';
  Chart.defaults.color = '#52514e';
  Chart.defaults.borderColor = '#e1e0d9';
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.tooltip.backgroundColor = '#1f2a24';
  Chart.defaults.plugins.tooltip.padding = 10;
  Chart.defaults.maintainAspectRatio = false;
}
configurarGraficos();
