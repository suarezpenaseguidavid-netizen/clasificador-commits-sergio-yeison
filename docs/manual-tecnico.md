# Manual Técnico

## Arquitectura

El sistema está compuesto por cuatro componentes principales:

```text
                    Cliente (Navegador / Swagger)
                              |
                     HTTP - Puerto 8000
                              |
                     +------------------+
                     |   FastAPI API    |
                     |  app/main.py     |
                     +------------------+
                      |              |
          Motor eco   |              | Motor Ollama
      (reglas-v1)     |              | (gemma3:270m)
                      |              |
                      +-------+------+
                              |
                    PostgreSQL - Puerto 5432
                              |
                     Base de datos db-ia
```

### Componentes

- Cliente: realiza las peticiones HTTP a la API.
- API FastAPI: recibe las solicitudes, clasifica los commits y registra los resultados.
- Motor eco: clasifica mediante reglas predefinidas.
- Motor Ollama: utiliza el modelo `gemma3:270m` para realizar la clasificación.
- PostgreSQL: almacena las inferencias realizadas.

---

## Seguridad

### Puertos expuestos

- **8000:** utilizado por FastAPI para recibir solicitudes HTTP.
- **5432:** utilizado por PostgreSQL para permitir la conexión de la API con la base de datos.

### Roles de la base de datos

- **Administrador:** puede crear tablas, modificar la estructura y administrar la base de datos.
- **Aplicación:** puede insertar nuevas inferencias y consultar los registros almacenados.

### Manejo de secretos

Las credenciales de conexión se almacenan en variables de entorno y no deben incluirse en el repositorio. El archivo `.env.example` sirve como plantilla para configurar el entorno.

### ¿Qué hacer si se filtra una contraseña?

Si una contraseña se filtra se deben realizar las siguientes acciones:

1. Cambiar inmediatamente la contraseña comprometida.
2. Actualizar las variables de entorno de la aplicación.
3. Reiniciar los servicios afectados.
4. Revisar los registros para detectar accesos no autorizados.
5. Revocar las credenciales antiguas y generar nuevas.
