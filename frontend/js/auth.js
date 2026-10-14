// Manejo de la sesión en el navegador: token JWT y datos básicos del usuario.

// Ruta base: las páginas dentro de /pages necesitan subir un nivel.
const BASE = location.pathname.includes('/pages/') ? '../' : './';

const Sesion = {
  guardar(token, usuario) {
    localStorage.setItem('bc_token', token);
    localStorage.setItem('bc_usuario', JSON.stringify(usuario));
  },

  token() {
    return localStorage.getItem('bc_token');
  },

  usuario() {
    try {
      return JSON.parse(localStorage.getItem('bc_usuario'));
    } catch {
      return null;
    }
  },

  esAdmin() {
    return this.usuario()?.rol === 'ADMINISTRADOR';
  },

  // Lee la fecha de expiración que viene dentro del token (no valida la firma: eso lo hace el backend)
  expirada() {
    const token = this.token();
    if (!token) return true;
    try {
      const datos = JSON.parse(atob(token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
      return datos.exp * 1000 < Date.now();
    } catch {
      return true;
    }
  },

  cerrar(aviso) {
    localStorage.removeItem('bc_token');
    localStorage.removeItem('bc_usuario');
    if (aviso) sessionStorage.setItem('bc_aviso', aviso);
    location.replace(BASE + 'login.html');
  },
};
