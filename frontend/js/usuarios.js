// Módulo 1: Autenticación y perfiles - gestión de usuarios y roles (solo ADMINISTRADOR).

const usuario = UI.iniciar({ pagina: 'usuarios', titulo: 'Usuarios y roles', soloAdmin: true });
const COLUMNAS = 7;

// Los permisos dependen del código interno del rol, que no cambia aunque se edite el nombre
const PERMISOS = {
  ADMINISTRADOR: ['Gestiona usuarios y roles', 'CRUD completo de proveedores, pilas, monitoreo y lotes',
    'Elimina recolecciones', 'Consulta dashboard y reportes'],
  RECOLECTOR: ['Registra recolecciones y edita solo las suyas', 'Consulta proveedores, pilas, monitoreo y lotes',
    'Consulta dashboard y reportes', 'Sin acceso a usuarios'],
};

const tabla = document.getElementById('tabla');
const filtros = document.getElementById('formFiltros');
const formulario = document.getElementById('formUsuario');
const formularioRol = document.getElementById('formRol');
let usuarios = [];
let roles = [];
let idEditando = null;
let idRolEditando = null;
let modal = null;
let modalRol = null;

if (usuario) {
  modal = new bootstrap.Modal('#modalUsuario');
  modalRol = new bootstrap.Modal('#modalRol');
  iniciar();
  filtros.addEventListener('input', UI.esperar(cargar));
  filtros.addEventListener('submit', (evento) => evento.preventDefault());
  document.getElementById('btnNuevo').addEventListener('click', () => abrirFormulario());
  document.getElementById('tarjetasRoles').addEventListener('click', (evento) => {
    const boton = evento.target.closest('button[data-rol]');
    if (boton) abrirFormularioRol(roles.find((r) => r.id_rol === Number(boton.dataset.rol)));
  });
}

async function iniciar() {
  try {
    await refrescarRoles();
    cargar();
  } catch (error) {
    UI.error(error);
  }
}

// Vuelve a pedir los roles y actualiza las tarjetas y las listas desplegables
async function refrescarRoles() {
  roles = await Api.get('/roles');
  const rolFiltrado = filtros.id_rol.value;
  UI.opciones(filtros.id_rol, roles, 'id_rol', (r) => r.nombre, 'Todos');
  UI.opciones(formulario.id_rol, roles, 'id_rol', (r) => r.nombre, 'Seleccione...');
  filtros.id_rol.value = rolFiltrado;
  pintarRoles();
}

function pintarRoles() {
  document.getElementById('tarjetasRoles').innerHTML = roles
    .map(
      (r) => `
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
              <div>
                <h2 class="h6 mb-0"><i class="bi bi-shield-check me-1"></i>${UI.escapar(r.nombre)}</h2>
                <span class="small texto-suave">Código interno: ${UI.escapar(r.codigo)} · ${r.total_usuarios} usuario(s)</span>
              </div>
              <button class="btn btn-sm btn-outline-primary" data-rol="${r.id_rol}" title="Editar nombre y descripción">
                <i class="bi bi-pencil me-1"></i>Editar
              </button>
            </div>
            <p class="small texto-suave mb-2">${UI.escapar(r.descripcion || '')}</p>
            <ul class="small mb-0 ps-3">${(PERMISOS[r.codigo] || []).map((p) => `<li>${p}</li>`).join('')}</ul>
          </div>
        </div>
      </div>`
    )
    .join('');
}

async function cargar() {
  UI.cargando(tabla, COLUMNAS);
  try {
    usuarios = await Api.get('/usuarios', UI.datosFormulario(filtros));
    pintar();
  } catch (error) {
    UI.sinDatos(tabla, COLUMNAS, 'No fue posible cargar la información');
    UI.error(error);
  }
}

function pintar() {
  document.getElementById('resumen').textContent = `${usuarios.length} usuario(s)`;
  if (!usuarios.length) return UI.sinDatos(tabla, COLUMNAS);
  tabla.innerHTML = usuarios
    .map((u) => {
      const esYo = u.id_usuario === usuario.id_usuario;
      return `
      <tr>
        <td class="fw-semibold">${UI.escapar(u.nombre)} ${esYo ? '<span class="badge text-bg-light border">Usted</span>' : ''}</td>
        <td>${UI.escapar(u.correo)}</td>
        <td>${UI.escapar(u.telefono || '—')}</td>
        <td>${UI.badge(u.rol, u.rol_nombre)}</td>
        <td>${UI.badge(u.activo)}</td>
        <td class="text-nowrap">${UI.fecha(u.fecha_creacion)}</td>
        <td class="acciones">${UI.botonesAccion(u.id_usuario, { eliminar: !esYo })}</td>
      </tr>`;
    })
    .join('');
}

// Si el rol no tiene acceso, UI.iniciar reemplazó el contenido y la tabla no existe
tabla?.addEventListener('click', (evento) => {
  const boton = evento.target.closest('button[data-accion]');
  if (!boton) return;
  const seleccionado = usuarios.find((u) => u.id_usuario === Number(boton.dataset.id));
  if (boton.dataset.accion === 'editar') abrirFormulario(seleccionado);
  if (boton.dataset.accion === 'eliminar') eliminar(seleccionado);
});

// ---------- Formulario de usuario ----------
function abrirFormulario(seleccionado = null) {
  idEditando = seleccionado ? seleccionado.id_usuario : null;
  formulario.reset();
  UI.limpiarValidacion(formulario);
  document.getElementById('tituloModal').textContent = seleccionado ? 'Editar usuario' : 'Nuevo usuario';
  // Al crear la contraseña es obligatoria; al editar, vacía = conservar la actual
  formulario.contrasena.required = !seleccionado;
  document.getElementById('contrasenaObligatoria').classList.toggle('d-none', !!seleccionado);
  document.getElementById('ayudaContrasena').textContent = seleccionado
    ? 'Déjela vacía para conservar la contraseña actual.'
    : 'Mínimo 8 caracteres, con letras y números.';
  if (seleccionado) UI.llenarFormulario(formulario, seleccionado);
  modal.show();
}

formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  UI.limpiarValidacion(formulario);
  if (!UI.validar(formulario)) return;

  const datos = UI.datosFormulario(formulario);
  await UI.conCarga(document.getElementById('btnGuardar'), async () => {
    try {
      if (idEditando) await Api.put(`/usuarios/${idEditando}`, datos);
      else await Api.post('/usuarios', datos);
      modal.hide();
      UI.toast(idEditando ? 'Usuario actualizado correctamente' : 'Usuario creado correctamente');
      await refrescarRoles();
      cargar();
    } catch (error) {
      UI.errorFormulario(formulario, error);
    }
  });
});

async function eliminar(seleccionado) {
  const confirmado = await UI.confirmar(
    `¿Eliminar el usuario ${seleccionado.nombre}? Si tiene registros asociados no se podrá eliminar; en ese caso, desactívelo.`
  );
  if (!confirmado) return;
  try {
    await Api.eliminar(`/usuarios/${seleccionado.id_usuario}`);
    UI.toast('Usuario eliminado correctamente');
    await refrescarRoles();
    cargar();
  } catch (error) {
    UI.error(error);
  }
}

// ---------- Formulario de rol (nombre visible y descripción) ----------
function abrirFormularioRol(rol) {
  idRolEditando = rol.id_rol;
  formularioRol.reset();
  UI.limpiarValidacion(formularioRol);
  document.getElementById('codigoRol').textContent = rol.codigo;
  UI.llenarFormulario(formularioRol, rol);
  modalRol.show();
}

formularioRol?.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  UI.limpiarValidacion(formularioRol);
  if (!UI.validar(formularioRol)) return;

  await UI.conCarga(document.getElementById('btnGuardarRol'), async () => {
    try {
      const rol = await Api.put(`/roles/${idRolEditando}`, UI.datosFormulario(formularioRol));
      modalRol.hide();
      UI.toast(`Rol "${rol.nombre}" actualizado correctamente`);
      // Si es el rol del usuario conectado, se actualiza el nombre en el menú y la barra superior
      if (rol.codigo === usuario.rol) {
        const sesion = { ...Sesion.usuario(), rol_nombre: rol.nombre };
        Sesion.guardar(Sesion.token(), sesion);
        UI.dibujarMenu('usuarios', sesion);
        UI.dibujarBarraSuperior('Usuarios y roles', sesion);
      }
      await refrescarRoles();
      cargar();
    } catch (error) {
      UI.errorFormulario(formularioRol, error);
    }
  });
});
