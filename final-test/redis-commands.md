# 📂 Redis Cheat Sheet: Tipos y Comandos

## 1. El Hash (`HGET`, `HSET`)

Es un mapa de campos y valores. Pensalo como un **objeto JSON plano** o una fila de una tabla SQL.

* **Uso ideal:** Perfiles de usuario, configuraciones, estados de sesión.
* **Comandos válidos:**
* `HSET key field value`: Crea o actualiza un campo.
* `HGET key field`: Trae un campo específico.
* `HMGET key field1 field2`: Trae varios campos a la vez.
* `HGETALL key`: Trae TODO el objeto (ojo con el rendimiento si es muy grande).
* `HDEL key field`: Borra un campo del objeto.

---

## 2. El Stream (`XADD`, `XREAD`)

Es un **log de eventos** (append-only). Cada entrada tiene un ID (timestamp) y adentro contiene pares de campo-valor.

* **Uso ideal:** Historial de transacciones, logs de sistema, colas de mensajería robustas.
* **Comandos válidos:**
* `XADD key ID field value`: Agrega un mensaje (usa `*` para ID automático).
* `XREAD STREAMS key ID`: Lee mensajes nuevos desde un punto.
* `XRANGE key start end`: Consulta mensajes en un rango de tiempo.
* `XGROUP CREATE / XREADGROUP`: Para repartir carga entre varios workers.
* `XACK key group ID`: Confirma que procesaste un mensaje.
* `XDEL key ID`: Marca un mensaje como borrado (pero no libera espacio de inmediato como `HDEL`).

---

## 3. Otros Tipos Importantes

| Tipo | Comandos Principales | Uso Común |
| --- | --- | --- |
| **String** | `SET`, `GET`, `INCR` | Cache simple, contadores. |
| **List** | `LPUSH`, `RPOP`, `LMOVE` | Colas simples (FIFO/LIFO). |
| **Set** | `SADD`, `SISMEMBER`, `SINTER` | Colecciones únicas (ej. etiquetas, seguidores). |
| **Sorted Set** | `ZADD`, `ZRANGE`, `ZREM` | Leaderboards, rankings, índices de tiempo. |

---

### 💡 ¿Cómo se relacionan en tu proyecto?

Si estás haciendo el sistema que mencionamos antes (donde el Stream tiene mucha carga), podrías usar ambos **en conjunto** pero con comandos distintos:

1. Usás `HSET user:123 ...` para guardar la info del usuario.
2. Usás `XADD logs:usuarios * id_usuario 123 accion "login"` para registrar el evento.
3. Tu proceso de Python lee el Stream con `XREAD` y, si necesita más detalle del usuario, tira un `HGET user:123`
