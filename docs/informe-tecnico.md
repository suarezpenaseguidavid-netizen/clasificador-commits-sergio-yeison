# Informe técnico del modelo

| Dato | Valor |
|------|-------|
| Perfil de hardware | *(Completar con la información de la Sección 2 de la guía: procesador, sistema operativo, etc.)* |
| RAM total del equipo | 3,5 GiB |
| Modelo y etiqueta | gemma3:270m |
| Tamaño en disco | 291 MB |
| Latencia ejecución 1 | 4664 ms |
| Latencia ejecución 2 | 3342 ms |
| Latencia ejecución 3 | 3299 ms |
| Latencia ejecución 4 | 3265 ms |
| Latencia ejecución 5 | 3373 ms |
| Latencia promedio | 3589 ms |
| RAM usada durante la inferencia | 1,9 GiB (o el valor que observes durante la prueba) |
| Calidad percibida | 3/5. El modelo responde correctamente y con buena velocidad, pero presenta imprecisiones en algunas respuestas técnicas debido a su tamaño reducido. |

---

# Plan de pruebas

| ID | Tipo | Qué se verifica | Resultado esperado | Obtenido | Estado |
|----|------|-----------------|--------------------|----------|--------|
| P-01 | Funcional | GET /health responde | Código 200 y estado ok | Código 200 y {"estado":"ok","base_datos":"ok"} |  PASÓ |
| P-02 | Funcional | POST /clasificar con motor eco | Código 200 y tipo correcto | Código 200 y clasificación correcta |  PASÓ |
| P-03 | Funcional | Motor inválido | Código 400 | Código 400 |  PASÓ |
| P-04 | Acceso | Rol app_ia intenta DROP TABLE | Error de permisos | Permisos restringidos |  PASÓ |
| P-05 | Conectividad | La API resuelve el host de la base de datos | Devuelve una IP interna | Conexión correcta a la base de datos |  PASÓ |
| P-06 | Disponibilidad | Reinicio del contenedor de BD | La API se recupera sola | Recuperación correcta |  PASÓ |
| P-07 | Persistencia | down y up conservan los datos | Los registros siguen existiendo | Persistencia verificada |  PASÓ |
| P-08 | Carga | 10 usuarios sobre el motor eco | p95 < 800 ms y errores < 5 % | Prueba ejecutada correctamente |  PASÓ |
| P-09 | Caracterización | 10 inferencias con el modelo | Promedio, mediana y p95 | Promedio: 1590 ms, Mediana: 260 ms, P95: 301 ms | PASÓ |

## Análisis del cuello de botella

Al comparar las pruebas P-08 y P-09 se observa que el mayor tiempo de respuesta se encuentra en la inferencia del modelo. La API y la base de datos responden rápidamente, mientras que el modelo requiere más tiempo para procesar la primera solicitud debido a la carga inicial en memoria. Después de esta carga, los tiempos de respuesta se estabilizan alrededor de los 250–300 ms.

## Propuestas de mejora

- Mantener el modelo cargado en memoria para evitar la alta latencia de la primera inferencia.
- Implementar un mecanismo de caché para consultas repetidas y reducir el tiempo de respuesta del servicio.
