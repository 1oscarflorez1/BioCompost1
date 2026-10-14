// Módulo 2: Gestión de proveedores de residuos (CRUD + búsqueda y filtros).

const usuario = UI.iniciar({ pagina: 'proveedores', titulo: 'Proveedores' });
const esAdmin = Sesion.esAdmin();
const COLUMNAS = 8;

const tabla = document.getElementById('tabla');
const filtros = document.getElementById('formFiltros');
const formulario = document.getElementById('formProveedor');
const modal = new bootstrap.Modal('#modalProveedor');
let proveedores = [];
let idEditando = null;

UI.opcionesCatalogo(filtros.tipo_proveedor, CATALOGOS.tipoProveedor, 'Todos');
UI.opcionesCatalogo(filtros.tipo_residuo, CATALOGOS.tipoResiduo, 'Todos');
UI.opcionesCatalogo(formulario.tipo_proveedor, CATALOGOS.tipoProveedor, 'Seleccione...');
UI.opcionesCatalogo(formulario.tipo_residuo, CATALOGOS.tipoResiduo, 'Seleccione...');

if (usuario) cargar();

filtros.addEventListener('input', UI.esperar(cargar));
filtros.addEventListener('submit', (evento) => evento.preventDefault());
document.getElementById('btnNuevo')?.addEventListener('click', () => abrirFormulario());

async function cargar() {
  UI.cargando(tabla, COLUMNAS);
  try {
    proveedores = await Api.get('/proveedores', UI.datosFormulario(filtros));
    pintar();
  } catch (error) {
    UI.sinDatos(tabla, COLUMNAS, 'No fue posible cargar la información');
    UI.error(error);
  }
}

function pintar() {
  document.getElementById('resumen').textContent = `${proveedores.length} registro(s)`;
  if (!proveedores.length) return UI.sinDatos(tabla, COLUMNAS);
  tabla.innerHTML = proveedores
    .map(
      (p) => `
      <tr>
        <td><div class="fw-semibold">${UI.escapar(p.nombre)}</div><div class="small texto-suave">NIT ${UI.escapar(p.documento)}</div></td>
        <td>${UI.etiqueta(p.tipo_proveedor)}</td>
        <td>${UI.escapar(p.municipio)}<div class="small texto-suave">${UI.escapar(p.direccion)}</div></td>
        <td>${UI.etiqueta(p.tipo_residuo)}</td>
        <td>${UI.escapar(p.contacto || '—')}<div class="small texto-suave">${UI.escapar(p.telefono || '')}</div></td>
        <td class="numero">${UI.numero(p.kg_aportados)}<div class="small texto-suave">${p.num_recolecciones} entregas</div></td>
        <td>${UI.badge(p.activo)}</td>
        <td class="acciones">${esAdmin ? UI.botonesAccion(p.id_proveedor) : ''}</td>
      </tr>`
    )
    .join('');
}

tabla.addEventListener('click', (evento) => {
  const boton = evento.target.closest('button[data-accion]');
  if (!boton) return;
  const proveedor = proveedores.find((p) => p.id_proveedor === Number(boton.dataset.id));
  if (boton.dataset.accion === 'editar') abrirFormulario(proveedor);
  if (boton.dataset.accion === 'eliminar') eliminar(proveedor);
});

function abrirFormulario(proveedor = null) {
  idEditando = proveedor ? proveedor.id_proveedor : null;
  formulario.reset();
  UI.limpiarValidacion(formulario);
  document.getElementById('tituloModal').textContent = proveedor ? 'Editar proveedor' : 'Nuevo proveedor';
  if (proveedor) UI.llenarFormulario(formulario, proveedor);
  modal.show();
}

formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  UI.limpiarValidacion(formulario);
  if (!UI.validar(formulario)) return;

  const datos = UI.datosFormulario(formulario);
  await UI.conCarga(document.getElementById('btnGuardar'), async () => {
    try {
      if (idEditando) await Api.put(`/proveedores/${idEditando}`, datos);
      else await Api.post('/proveedores', datos);
      modal.hide();
      UI.toast(idEditando ? 'Proveedor actualizado correctamente' : 'Proveedor registrado correctamente');
      cargar();
    } catch (error) {
      UI.errorFormulario(formulario, error);
    }
  });
});

async function eliminar(proveedor) {
  const confirmado = await UI.confirmar(
    `¿Eliminar el proveedor "${proveedor.nombre}"? Si tiene recolecciones registradas no se podrá eliminar; en ese caso, desactívelo.`
  );
  if (!confirmado) return;
  try {
    await Api.eliminar(`/proveedores/${proveedor.id_proveedor}`);
    UI.toast('Proveedor eliminado correctamente');
    cargar();
  } catch (error) {
    UI.error(error);
  }
}
