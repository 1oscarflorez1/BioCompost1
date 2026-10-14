// Inicio de sesión: envía las credenciales a POST /api/auth/login y guarda el token.

const formulario = document.getElementById('formLogin');
const aviso = document.getElementById('aviso');

function mostrarAviso(mensaje, tipo) {
  aviso.className = `alert alert-${tipo} small`;
  aviso.textContent = mensaje;
}

// Si ya hay una sesión vigente, se va directo al dashboard
if (Sesion.token() && !Sesion.expirada()) location.replace('index.html');

// Mensaje que deja otra página (sesión cerrada o expirada)
const avisoPendiente = sessionStorage.getItem('bc_aviso');
if (avisoPendiente) {
  mostrarAviso(avisoPendiente, 'info');
  sessionStorage.removeItem('bc_aviso');
}

document.getElementById('verContrasena').addEventListener('click', (evento) => {
  const campo = document.getElementById('contrasena');
  const visible = campo.type === 'text';
  campo.type = visible ? 'password' : 'text';
  evento.currentTarget.innerHTML = `<i class="bi bi-eye${visible ? '' : '-slash'}"></i>`;
});

formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  if (!UI.validar(formulario)) return;

  const boton = document.getElementById('btnIngresar');
  boton.disabled = true;
  boton.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Validando...';
  try {
    const respuesta = await Api.post('/auth/login', {
      correo: formulario.correo.value.trim(),
      contrasena: formulario.contrasena.value,
    });
    Sesion.guardar(respuesta.access_token, respuesta.usuario);
    location.replace('index.html');
  } catch (error) {
    mostrarAviso(error.message, error.estado === 0 ? 'warning' : 'danger');
    boton.disabled = false;
    boton.innerHTML = '<i class="bi bi-box-arrow-in-right me-1"></i>Ingresar';
  }
});
