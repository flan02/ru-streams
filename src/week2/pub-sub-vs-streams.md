# Redis Pub/Sub vs. Streams

---

## 🔄 Redis Pub/Sub vs. Streams: ¿Cuál elegir?

Aunque ambos se utilizan para la mensajería, funcionan de maneras fundamentalmente diferentes. Aquí te explico las claves para decidir cuál usar en tus proyectos.

### 1. Conceptos Fundamentales

| Característica | Pub/Sub | Streams |
| --- | --- | --- |
| **Modelo** | "Disparar y olvidar" (Fire & Forget) | Registro histórico (Log-based) |
| **Persistencia** | **No.** Si no hay nadie escuchando, el mensaje se pierde. | **Sí.** Los mensajes se guardan en RAM hasta que decidas borrarlos. |
| **Entrega** | Envía el mensaje a todos los suscriptores actuales. | Permite que diferentes consumidores lean a su propio ritmo. |
| **Estado** | Stateless (Sin estado). | Stateful (Mantiene el historial y el estado de lectura). |

---

### 2. Diferencias Clave

#### **Persistencia y Memoria**

* **Pub/Sub:** Es puramente efímero. Imaginalo como una **estación de radio**: si sintonizás tarde, no podés escuchar lo que pasaron hace 5 minutos.
* **Streams:** Funcionan como un **log de transacciones**. Los mensajes permanecen en el Stream incluso después de ser leídos, lo que permite recuperar datos históricos.

#### **Grupos de Consumidores (Consumer Groups)**

* **Pub/Sub:** No tiene concepto de grupos. Si 10 suscriptores escuchan un canal, los 10 reciben el mismo mensaje.
* **Streams:** Permite crear **Consumer Groups**. Esto permite repartir el trabajo entre varios procesos (como hicimos en el curso con el `consumer` y el `consumer-average`), asegurando que un mensaje sea procesado por un solo integrante del grupo si es necesario.

#### **Garantía de Entrega (ACKs)**

* **Pub/Sub:** No hay garantía. Redis no sabe si el suscriptor recibió el mensaje.
* **Streams:** Implementa el concepto de **Acknowledgment (ACK)**. El consumidor debe avisar a Redis que procesó el mensaje correctamente (`XACK`). Si el consumidor muere antes de avisar, el mensaje queda en una lista de "pendientes" (PEL) para ser re-procesado.

---

### 3. Casos de Uso

#### **Usa Pub/Sub cuando:**

* Necesitás notificaciones instantáneas de baja latencia donde **no importa** perder un mensaje si el cliente está desconectado.
* Ejemplos: Chats en tiempo real (donde solo importa lo que pasa ahora), disparadores de UI, o sistemas de señalización.

#### **Usa Streams cuando:**

* Necesitás un historial de eventos confiable.
* Necesitás **escalar el procesamiento** (muchos consumidores trabajando sobre los mismos datos).
* Ejemplos: Procesamiento de pagos, telemetría de sensores, registros de auditoría o sistemas donde el orden y la persistencia son críticos.

---

### Resumen para el desarrollador

> "Si necesitás que el mensaje llegue **ahora** a quien esté conectado, usá **Pub/Sub**. Si necesitás que el mensaje **se procese sí o sí**, incluso si el servidor se reinicia, usá **Streams**."
