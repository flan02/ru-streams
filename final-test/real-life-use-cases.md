# Casos de Uso Reales de Redis Streams

## 1. Plataformas de Trading y Criptomonedas (Order Books)

En un exchange de cripto, los precios cambian miles de veces por segundo.

* **El Problema:** Si usaras una DB convencional (como PostgreSQL), cada vez que alguien compra, tendrías que hacer un `INSERT` y bloquear la fila para que otro no compre lo mismo. Con miles de personas, la DB se "traba" (deadlocks).
* **Por qué Redis Streams:** * **Velocidad de RAM:** Las órdenes entran al Stream en microsegundos.
* **Consumer Groups:** Un grupo de consumidores se encarga de "machear" (unir) compradores con vendedores, mientras otro grupo guarda el historial en un disco lento por separado.
* **Orden Estricto:** Los IDs de los Streams garantizan que la orden que llegó primero se procese primero.

---

## 2. Sistemas de Telemetría y Rastreo (Uber / Rappi / Logística)

Imaginá 100,000 repartidores mandando su GPS cada 2 segundos.

* **El Problema:** Guardar cada coordenada GPS en una DB de disco (como MongoDB) generaría una carga de escritura (I/O) inmensa que degradaría el rendimiento de toda la app.
* **Por qué Redis Streams:** * **Absorción de Carga:** Redis actúa como un "amortiguador" (buffer). Recibe las coordenadas a toda velocidad en RAM.
* **Procesamiento en tiempo real:** Los Consumer Groups analizan el Stream para ver si un repartidor se desvió de la ruta o para calcular el tiempo estimado de llegada (ETA) al instante.
* **Capping (MAXLEN):** No necesitan el historial de hace un mes en RAM; solo los últimos 10 minutos de movimiento para que la app funcione.

---

## 3. Feed de Actividad y Notificaciones (Redes Sociales / Gaming)

Cuando un streamer famoso en Twitch empieza un vivo o alguien con millones de seguidores postea algo.

* **El Problema:** Notificar a 1 millón de personas al mismo tiempo. Una DB convencional colapsaría intentando leer quién sigue a quién y enviando los mensajes uno por uno.
* **Por qué Redis Streams:**
* **Fan-out eficiente:** Usan Streams para propagar la notificación. Los workers (consumidores) leen del Stream y empujan las notificaciones push.
* **Persistence:** A diferencia de Pub/Sub, si el usuario tiene el celular apagado, cuando lo prende, el "puntero" del consumidor en el Stream sabe qué notificaciones le faltan mostrarle.

---

## ¿Por qué elegir Redis sobre una DB "robusta"?

| Razón | Redis Streams | DB Convencional (Postgres/Mongo) |
| --- | --- | --- |
| **Latencia** | **Microsegundos** (RAM). | Milisegundos (Disco/SSD). |
| **Escritura Masiva** | Diseñada para miles de `XADD` por segundo sin despeinarse. | El disco se convierte en un "cuello de botella". |
| **Concurrencia** | Los Consumer Groups gestionan quién lee qué de forma nativa. | Requiere lógica compleja de `SELECT FOR UPDATE` o bloqueos de filas. |
| **Costo de Operación** | Muy bajo para datos "vivos" o temporales. | Alto si intentás usarla como si fuera memoria RAM. |

---

### En resumen

Elegimos Redis cuando **la velocidad de llegada de los datos es mayor a la velocidad con la que el disco puede escribirlos**, o cuando necesitamos que varios procesos se repartan el trabajo en tiempo real sin pisarse los pies.

Para todo lo que sea "histórico" o "reportes anuales", ahí sí movemos los datos del Stream a la **DB Robusta**. Redis es el **motor de carrera** para el presente, y la DB convencional es el **archivo de seguridad** para el pasado.
