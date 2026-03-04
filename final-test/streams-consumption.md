# 🏗️ Arquitectura de Consumo y Gestión de Grandes Volúmenes

Guía técnica sobre la eficiencia en el procesamiento de Redis Streams.

---

## 1. Single Consumers (Consumidores Individuales)

Se usan cuando leés un Stream con el comando `XREAD`.

* **Qué son:** Un único cliente que lee mensajes del Stream.
* **Cuándo usarlos:** Cuando necesitás un modelo de "Fan-out" (donde cada consumidor debe recibir una copia de cada mensaje) o para herramientas de monitoreo simple.
* **Limitación:** No permiten repartir la carga. Si el volumen de mensajes sube, el consumidor individual puede saturarse.

## 2. Consumer Groups (Grupos de Consumidores)

Se usan con el comando `XREADGROUP`.

* **Qué son:** Un conjunto de consumidores que colaboran para procesar un único Stream.
* **Para qué se usan:** Para **escalar horizontalmente**. Redis reparte los mensajes de forma que un mensaje solo sea procesado por un integrante del grupo.
* **Conceptos clave:**
  * **Load Balancing:** Ideal para microservicios que procesan tareas pesadas.
  * **Pointers:** Cada grupo mantiene su propio puntero de lectura independiente del Stream original.
  * **Ownership:** Redis sabe exactamente qué consumidor tiene qué mensaje pendiente (PEL).

---

## 3. Large Streams & Payload Considerations

Manejar "payloads" (carga de datos) grandes requiere estrategias específicas para no agotar la RAM de Redis.

### Estrategias de Payload

* **Datos Pequeños (In-Stream):** Si el mensaje es corto (ej. coordenadas GPS, temperatura), se guarda directamente en el Stream.

* **Datos Grandes (Off-Stream):** Si necesitás procesar imágenes o JSONs gigantes, **no los guardes en el Stream**.
  * *Buena práctica:* Guardá el objeto grande en una base de datos (S3, MongoDB) y poné solo el **ID** o la **URL** en el mensaje del Redis Stream.

### Rendimiento con Radix Trees

Como aprendimos, Redis usa **Radix Trees** para los IDs. Esto significa que:

* Las búsquedas por ID son extremadamente rápidas ($O(\log N)$).
* El consumo de memoria es eficiente siempre que los IDs sean secuenciales (usando `*`).

---

## 4. Gestión del Crecimiento (Capping)

Un Stream no debe crecer infinitamente. Se usan dos estrategias:

1. **MAXLEN:** `XADD mystream MAXLEN 1000 * field value`. Limita el Stream a los últimos 1000 mensajes.
2. **MINID:** Elimina mensajes más viejos que un ID específico. Es más eficiente para borrar datos por antigüedad.

---

## 💡 Resumen para el Examen

* **¿Cuándo usar Consumer Groups?** Siempre que necesites procesar mensajes en paralelo y asegurar que ninguno se pierda (Reliability).
* **¿Qué pasa con la RAM?** Los payloads grandes en miles de mensajes pueden llenar la memoria rápido. Usar punteros a datos externos es la estrategia Senior.
* **¿Cómo se borran mensajes?** Los mensajes de un Stream **no se borran al leerlos** (a diferencia de una Queue común). Se deben recortar manualmente con `MAXLEN` o eliminarlos con `XDEL`
