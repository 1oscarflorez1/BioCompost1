// Cliente de la API REST: todas las peticiones del frontend pasan por aquí (fetch).
// El frontend NUNCA se conecta a Oracle: solo habla con FastAPI.

class ErrorApi extends Error {
  constructor(mensaje, estado, errores = []) {
    super(mensaje);
    this.estado = estado; // código HTTP (0 = sin conexión)
    this.errores = errores; // errores de validación por campo [{campo, mensaje}]
  }
}

const MENSAJES_HTTP = {
  400: 'La solicitud no es válida',
  401: 'Debe iniciar sesión',
  403: 'No tiene permisos para realizar esta acción',
  404: 'El registro no existe',
  409: 'El registro entra en conflicto con información existente',
  422: 'Hay datos no válidos en el formulario',
  500: 'Error interno del servidor',
  503: 'El servicio no está disponible en este momento',
};

const Api = {
  async solicitud(metodo, ruta, datos) {
    const cabeceras = { Accept: 'application/json' };
    if (datos !== undefined) cabeceras['Content-Type'] = 'application/json';
    const token = Sesion.token();
    if (token) cabeceras.Authorization = `Bearer ${token}`;

    let respuesta;
    try {
      respuesta = await fetch(API_URL + ruta, {
        method: metodo,
        headers: cabeceras,
        body: datos !== undefined ? JSON.stringify(datos) : undefined,
      });
    } catch {
      throw new ErrorApi('No hay conexión con el servidor. Verifique que la API esté en ejecución.', 0);
    }

    const cuerpo = await respuesta.json().catch(() => null);
    if (!respuesta.ok) {
      // Token vencido o inválido: se cierra la sesión y se vuelve al login
      if (respuesta.status === 401 && ruta !== '/auth/login') {
        Sesion.cerrar(cuerpo?.detail || 'Su sesión terminó. Inicie sesión nuevamente.');
      }
      const mensaje = cuerpo?.detail || MENSAJES_HTTP[respuesta.status] || 'Ocurrió un error inesperado';
      throw new ErrorApi(mensaje, respuesta.status, cuerpo?.errores || []);
    }
    return cuerpo;
  },

  // Convierte {texto: 'x', fase: ''} en "?texto=x" (omite los filtros vacíos)
  consulta(filtros) {
    if (!filtros) return '';
    const parametros = new URLSearchParams();
    for (const [clave, valor] of Object.entries(filtros)) {
      if (valor !== null && valor !== undefined && valor !== '' && valor !== false) parametros.append(clave, valor);
    }
    const texto = parametros.toString();
    return texto ? `?${texto}` : '';
  },

  get(ruta, filtros) {
    return this.solicitud('GET', ruta + this.consulta(filtros));
  },
  post(ruta, datos) {
    return this.solicitud('POST', ruta, datos);
  },
  put(ruta, datos) {
    return this.solicitud('PUT', ruta, datos);
  },
  eliminar(ruta) {
    return this.solicitud('DELETE', ruta);
  },
};
