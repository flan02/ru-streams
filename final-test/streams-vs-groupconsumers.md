# 🛰️ Redis Pub/Sub vs. Redis Streams

Comparativa técnica de modelos de mensajería en Redis.

---

## 1. Cuadro Comparativo

| Característica | Pub/Sub | Redis Streams |
| :--- | :--- | :--- |
| **Modelo** | Disparar y olvidar (Fire & Forget) | Registro histórico (Log-based) |
| **Persistencia** | **No.** Mensajes efímeros en RAM. | **Sí.** Persistente en RAM (y disco vía RDB/AOF). |
| **Consumo de Historia** | No puede recuperar mensajes pasados. | Permite leer desde cualquier punto del tiempo. |
| **Garantía de Entrega** | "At-most-once" (Se entrega si estás online). | "At-least-once" (Vía ACKs y PEL). |
| **Balanceo de Carga** | No. Todos los suscriptores reciben todo. | Sí. Vía **Consumer Groups**. |

---

## 2. Diferencias Conceptuales

### Pub/Sub (Publicador/Suscriptor)

Es un sistema de mensajería **sin estado** (*stateless*).

* Si un mensaje se publica y no hay suscriptores conectados en ese milisegundo, el mensaje **desaparece**.
* Es ideal para notificaciones en tiempo real, chats rápidos o disparadores de eventos donde la pérdida de un dato ocasional no es crítica.

### Redis Streams

Es un sistema de mensajería **con estado** (*stateful*).

* El stream funciona como una cinta de grabación. Los mensajes quedan guardados cronológicamente.
* Permite que múltiples consumidores lean a su propio ritmo. Si un consumidor se desconecta, al volver puede retomar exactamente donde dejó.

---

## 3. ¿Cuándo usar cada uno?

### Usá Pub/Sub cuando

* Necesitás latencia ultra-baja y no te importa la persistencia.
* Querés notificar a miles de clientes en milisegundos (Fan-out masivo).
* Ejemplo: Notificar un "Typing..." en un chat o una actualización de precio en un dashboard.

### Usá Streams cuando

* La integridad de los datos es vital. Cada mensaje debe ser procesado.
* Necesitás repartir el trabajo entre varios procesos (Consumer Groups).
* Necesitás auditoría o historial de lo que pasó.
* Ejemplo: Procesamiento de transacciones, telemetría de sensores o logs de sistema.

---

## 💡 Tip de Examen

Si la pregunta menciona **"Consumer Groups"**, **"XACK"** o **"Persistence"**, la respuesta es **Streams**. Si menciona **"SUBSCRIBE"** o **"PUBLISH"**, es el modelo antiguo de **Pub/Sub**
