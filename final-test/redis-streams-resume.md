# 🚀 Redis Streams Certification Cheat Sheet

Resumen técnico para el examen de **Redis University**.

---

## 1. Comandos de Inserción y Anatomía (`XADD`)

* **ID Format:** `<millisecondsTime>-<sequenceNumber>`. Ejemplo: `1738360000000-0`.
* **Auto-ID:** El uso de `*` en `XADD` permite que Redis asigne el ID basado en el tiempo actual.
* **Inmutabilidad:** Los IDs deben ser estrictamente crecientes. No se pueden insertar IDs menores al último existente.
* **Capping:** `MAXLEN ~ 1000` evita que el Stream agote la RAM (la `~` hace que el recorte sea aproximado pero mucho más rápido).

## 2. Estrategias de Lectura

* **XREAD:** Lectura simple (Fan-out). Todos los clientes ven los mismos mensajes.
* **XREADGROUP:** Lectura competitiva (Load Balancing). Los mensajes se reparten entre los miembros del grupo.
* **ID `>`:** Indica a Redis que entregue solo mensajes nuevos (que nunca fueron entregados a nadie).
* **ID `0`:** Indica a Redis que entregue los mensajes en la **PEL** (mensajes pendientes de confirmación para ese consumidor específico).

## 3. Confiabilidad y Recuperación

* **PEL (Pending Entries List):** Almacén interno de mensajes entregados pero que aún no recibieron un `XACK`.
* **XACK:** Confirma el procesamiento y elimina el mensaje de la PEL. Vital para evitar el doble procesamiento.
* **XPENDING:** Permite inspeccionar qué mensajes están "trabados", quién los tiene y su *Idle Time*.
* **XCLAIM:** Permite que un consumidor sano tome la propiedad de un mensaje pendiente de otro consumidor (útil en casos de crasheo).
* **XINFO:** El comando fundamental para diagnosticar el estado de Streams, Grupos y Consumidores.

## 4. Arquitectura Interna

* **Radix Tree:** La estructura de datos de bajo nivel que permite a Redis manejar millones de IDs de forma eficiente.
* **Path Compression:** La técnica que ahorra memoria RAM al compartir prefijos comunes entre IDs correlativos.

---

## 💡 Tips de Examen

* **Streams vs Pub/Sub:** Los Streams son persistentes y permiten recuperar historia; Pub/Sub es "disparar y olvidar".
* **Consumer Groups:** Son exclusivos de Streams. No existen en Pub/Sub.
* **MKSTREAM:** Opción en `XGROUP CREATE` para crear el stream automáticamente si no existe todavía.
