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

## Endpoints

La API expone los siguientes endpoints principales:

| Método | Ruta | Parámetros de entrada | Respuesta | Códigos |
|---|---|---|---|---|
| GET | `/health` | Ninguno | Estado del servicio y de la base de datos | 200, 503 |
| POST | `/clasificar` | JSON: `texto`, `motor` | Motor utilizado, modelo, entrada, tipo y latencia | 200, 422 |
| GET | `/inferencias` | Query opcional: `limite` | Lista de inferencias registradas | 200, 422 |

### GET /health

Comprueba la disponibilidad de la API y la conexión con PostgreSQL.

**Ejemplo de respuesta:**

```json
{
  "estado": "ok",
  "base_datos": "ok"
}
### POST /clasificar

Recibe un mensaje de commit y lo clasifica utilizando el motor seleccionado.

**Entrada:**

```json
{
  "texto": "fix: corregir error de conexión",
  "motor": "eco"
}
**Respuesta:**

```json
{
  "motor": "eco",
  "modelo": "reglas-v1",
  "entrada": "fix: corregir error de conexión",
  "tipo": "fix",
  "latencia_ms": 0
}
### GET /inferencias

Devuelve las últimas inferencias registradas en la base de datos.

**Parámetro de entrada:**

- `limite`: parámetro opcional que indica la cantidad máxima de registros a devolver. Su valor predeterminado es 20.

**Ejemplo:**

```bash
curl "http://localhost:8000/inferencias?limite=5"
`


**Respuesta:**

```json
[
  {
    "id": 1,
    "fecha": "2026-08-12T14:02:50.631752",
    "motor": "eco",
    "modelo": "reglas-v1",
    "entrada": "fix: corregir error de conexión",
    "salida": "fix",
    "latencia_ms": 0
  }
]
## Modelo de datos

La aplicación utiliza PostgreSQL para almacenar las inferencias realizadas por el sistema.

### Tabla `inferencias`

| Campo | Descripción |
|---|---|
| `id` | Identificador único de la inferencia. |
| `fecha` | Fecha y hora en que se registró la inferencia. |
| `motor` | Motor utilizado para realizar la clasificación. |
| `modelo` | Modelo o versión utilizada por el motor. |
| `entrada` | Texto del mensaje de commit recibido. |
| `salida` | Tipo de commit obtenido como resultado de la clasificación. |
| `latencia_ms` | Tiempo empleado por el motor para realizar la clasificación, expresado en milisegundos. |

La tabla permite conservar un historial de las clasificaciones realizadas por la API.

El rol `app_ia` utiliza la tabla con privilegios mínimos. Puede realizar las operaciones necesarias para el funcionamiento de la aplicación, pero no puede eliminar registros ni modificar o eliminar la estructura de la tabla.
## Respaldo y restauración

El respaldo de PostgreSQL permite conservar la información de la base de datos ante fallos o pérdida del contenedor.

### Respaldo

El respaldo se realiza utilizando `pg_dump` sobre la base de datos `iadb`.

```bash
docker compose exec db pg_dump -U postgres -d iadb > respaldo.sql
### Restauración

Para restaurar un respaldo se utiliza:

```bash
cat respaldo.sql | docker compose exec -T db psql -U postgres -d iadb
Después de la restauración se debe comprobar que la tabla `inferencias` y sus registros estén disponibles.

### Persistencia

La persistencia fue comprobada deteniendo y levantando nuevamente los servicios:

```bash
docker compose down
docker compose up -d
curl "http://localhost:8000/inferencias?limite=5"
Después de volver a levantar los servicios, los registros previamente creados continuaron disponibles.
## Decisiones de diseño y limitaciones

### Dockerfile multi-etapa

Se utiliza un Dockerfile multi-etapa para separar la etapa de construcción de la etapa de ejecución. Esto permite mantener la imagen final más limpia y reducir elementos innecesarios en el entorno de ejecución.

### Usuario sin privilegios

La aplicación se ejecuta utilizando un usuario sin privilegios administrativos dentro del contenedor. Esto reduce el impacto que tendría una posible vulnerabilidad de la aplicación.

### Motor ECO

El motor ECO utiliza reglas predefinidas para clasificar los mensajes de commit. Se utiliza como motor por defecto porque no requiere un modelo externo y proporciona respuestas rápidas y predecibles.

### Privilegios mínimos en PostgreSQL

La aplicación utiliza el rol `app_ia` con privilegios mínimos sobre la base de datos, aplicando el principio de mínimo privilegio.

El rol puede realizar las operaciones necesarias para el funcionamiento de la API, pero no puede eliminar registros de la tabla `inferencias` ni eliminar su estructura.

Esta configuración fue comprobada mediante pruebas de acceso. Las operaciones `DELETE` y `DROP TABLE` fueron rechazadas por PostgreSQL.

### Limitaciones conocidas

- El motor ECO depende de las reglas predefinidas para realizar la clasificación.
- El motor Ollama requiere recursos adicionales de procesamiento y memoria.
- La API no implementa autenticación de usuarios en los endpoints.
- PostgreSQL es necesario para almacenar y consultar las inferencias.
- La solución está orientada al entorno de desarrollo y demostración del proyecto.
- La prueba de carga con k6 mostró un p95 de aproximadamente `50.01 ms` y una tasa de errores de `0.00 %` en el entorno de prueba utilizado.


---

## Respaldo y restauración de la base de datos

### Crear un respaldo

```bash
mkdir -p backups
docker exec db-ia pg_dump -U postgres clasificador > backups/backup_clasificador.sql
```

Verificar que el archivo fue creado:

```bash
ls -lh backups
```

### Simular un desastre

Consultar la cantidad de registros:

```bash
docker compose exec -T db psql -U postgres -d clasificador -c "SELECT COUNT(*) FROM inferencias;"
```

Eliminar temporalmente los datos:

```bash
docker compose exec -T db psql -U postgres -d clasificador -c "TRUNCATE inferencias;"
```

Verificar que la tabla quedó vacía:

```bash
docker compose exec -T db psql -U postgres -d clasificador -c "SELECT COUNT(*) FROM inferencias;"
```

### Restaurar el respaldo

```bash
cat backups/backup_clasificador.sql | docker compose exec -T db psql -U postgres -d clasificador
```

Verificar que los datos fueron recuperados:

```bash
docker compose exec -T db psql -U postgres -d clasificador -c "SELECT COUNT(*) FROM inferencias;"
```

Resultado esperado:

- Antes del desastre: **12 registros**.
- Después de `TRUNCATE`: **0 registros**.
- Después de la restauración: **12 registros**.

