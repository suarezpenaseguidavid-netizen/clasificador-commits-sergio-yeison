# Clasificador de commits

## Descripción

Clasificador de mensajes de commits desarrollado con FastAPI, PostgreSQL y Docker. La aplicación recibe mensajes de commit mediante una API REST, los clasifica según su tipo (`feat`, `fix`, `docs`, `test`, `chore` o `refactor`) y registra cada inferencia en PostgreSQL. El sistema cuenta con un motor ECO basado en reglas y puede integrarse con un motor Ollama para realizar clasificaciones mediante un modelo local.

## Integrantes

- Sergio Suarez
- Yeison

### Perfil de hardware utilizado

El proyecto fue desarrollado y probado utilizando equipos con:

- Sistema operativo: Ubuntu Linux
- Arquitectura: x86_64
- Procesador: Intel core 3
- Memoria RAM: 3
- Almacenamiento: 500gb

## Requisitos mínimos

### Hardware

- CPU de 2 núcleos o superior.
- 4 GB de RAM mínimo.
- 10 GB de espacio libre en disco.
- Conexión a Internet para descargar dependencias e imágenes Docker.

### Software

- Ubuntu Linux o distribución Linux compatible.
- Docker.
- Docker Compose.
- Git.
- Python 3.12.
- `curl`.
- Navegador web.

## Instalación
### 1. Clonar el repositorio

```bash
git clone https://github.com/suarezpenaseguidavid-netizen/clasificador-commits-sergio-yeison.git
cd clasificador-commits-sergio-yeison
```

### 2. Verificar Docker

Comprobar que Docker y Docker Compose estén instalados:

```bash
docker --version
docker compose version
```

### 3. Configurar las variables de entorno

Crear el archivo `.env` a partir de la plantilla:

```bash
cp .env.example .env
```

Verificar el archivo:

```bash
cat .env
```

Las credenciales y secretos deben mantenerse en el archivo `.env` y no deben subirse al repositorio.

### 4. Levantar los servicios

Ejecutar:

```bash
docker compose up -d
```

### 5. Verificar los contenedores

Ejecutar:

```bash
docker compose ps
```

Los servicios `api-ia` y `db-ia` deben aparecer activos y la base de datos debe mostrar el estado `healthy`.

### 6. Verificar la API

Ejecutar:

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{
  "estado": "ok",
  "base_datos": "ok"
}
```
## Prueba de los endpoints

### 1. GET /health

Comprueba que la API y la base de datos estén disponibles.

```bash
curl http://localhost:8000/health
```

### 2. POST /clasificar

Clasifica un mensaje de commit utilizando el motor ECO.

```bash
curl -X POST http://localhost:8000/clasificar \
  -H "Content-Type: application/json" \
  -d '{"texto":"fix: corregir error de conexión","motor":"eco"}'
```

Respuesta esperada:

```json
{
  "motor": "eco",
  "modelo": "reglas-v1",
  "entrada": "fix: corregir error de conexión",
  "tipo": "fix",
  "latencia_ms": 0
}
```

### 3. GET /inferencias

Consulta las inferencias almacenadas en PostgreSQL.

```bash
curl "http://localhost:8000/inferencias?limite=5"
```

## Pruebas automatizadas

Con los servicios levantados, ejecutar:

```bash
PYTHONPATH=. pytest -v
```

Resultado esperado:

```text
5 passed
```

## Prueba de carga

La prueba de carga se encuentra en:

```text
tests/carga/prueba_carga.js
```

Para ejecutarla:

```bash
docker run --rm -i --network host grafana/k6 run - < tests/carga/prueba_carga.js
```

Durante la prueba se pueden observar los recursos utilizados mediante:

```bash
docker stats
```

En la prueba realizada se obtuvieron los siguientes resultados:

- p95: 50.01 ms.
- Tasa de errores: 0.00%.
- Peticiones: 641.
- Checks exitosos: 100%.
## Solución de problemas

### 1. Error de permisos al ejecutar Docker

Se presentó un error de permisos al intentar conectarse al servicio de Docker.

Solución:

```bash
sudo usermod -aG docker $USER
```

Después se verificó que Docker estuviera disponible:

```bash
docker --version
```

### 2. PostgreSQL no estaba disponible

Al ejecutar las pruebas se presentó un error de conexión con PostgreSQL porque los contenedores no estaban levantados.

Solución:

```bash
docker compose up -d
```

Después se verificó el estado de los servicios:

```bash
docker compose ps
```

### 3. Las pruebas de pytest no encontraban el módulo `app`

Al ejecutar las pruebas se presentó un error relacionado con la ubicación del módulo `app`.

Solución:

```bash
PYTHONPATH=. pytest -v
```

Con esta configuración las pruebas se ejecutaron correctamente y se obtuvieron 5 pruebas exitosas.

### 4. Ruff detectó una excepción demasiado general

Ruff reportó el error:

```text
BLE001 Do not catch blind exception
```

Se revisó el manejo de excepciones en el código y se realizó la corrección correspondiente.

Para comprobar nuevamente el código:

```bash
ruff check app/
```

Resultado esperado:

```text
All checks passed!
```

### 5. Git rechazó un `push`

Durante el trabajo con Git se presentó un rechazo del `push` porque el repositorio remoto tenía cambios que no estaban en la copia local.

Solución:

```bash
git pull --rebase origin main
```

Si aparecen conflictos, resolverlos y ejecutar:

```bash
git add <archivo>
git rebase --continue
```

Finalmente:

```bash
git push origin main
```

## Detener los servicios

Para detener los contenedores:

```bash
docker compose down
```

Para volver a iniciar la aplicación:

```bash
docker compose up -d
```
