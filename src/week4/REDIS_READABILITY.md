# 🛡️ Redis Streams: Confiabilidad y Recuperación de Errores

En un sistema distribuido, los consumidores pueden fallar (crasheos, pérdida de red). Redis Streams provee mecanismos avanzados para asegurar que **ningún mensaje se pierda** y que todos sean procesados al menos una vez (**At-least-once delivery**).

## 1. Conceptos Clave

### PEL (Pending Entries List)

Cuando un mensaje es entregado a un integrante de un **Consumer Group**, Redis lo mueve a la **PEL**. Este mensaje permanece allí hasta que el consumidor envía un `XACK`.

* Si el consumidor muere antes de procesarlo, el mensaje queda "atrapado" en la PEL.

### ACK (Acknowledgment)

Es la señal que el consumidor envía a Redis (`XACK`) para decirle: *"Ya terminé con este mensaje, podés borrarlo de la lista de pendientes"*.

---

## 2. Comandos de Inspección y Recuperación

### `XPENDING` (Inspección)

Permite ver qué mensajes están pendientes en un grupo.

* **Uso básico:** `XPENDING mystream mygroup` (Muestra cuántos hay y el rango de IDs).
* **Uso detallado:** `XPENDING mystream mygroup - + 10` (Muestra ID, consumidor actual, tiempo de inactividad y cuántas veces se entregó).

### `XCLAIM` (Recuperación)

Permite que un consumidor "reclame" un mensaje que le pertenece a otro.

* **Criterio:** Generalmente se usa el **Idle Time** (tiempo de inactividad). Si un mensaje lleva 5000ms sin actividad, otro consumidor lo reclama para sí mismo.
* **Sintaxis:** `XCLAIM <key> <group> <consumer> <min-idle-time> <ID1> <ID2>...`

---

## 3. Estrategias de Recuperación (Recovery Flow)

En tu código de Python (ej. los "BOBs"), la lógica de recuperación sigue este orden:

1. **Check de Pendientes Propios:** Al iniciar, el consumidor lee con `XREADGROUP` usando el ID `"0"`. Esto le entrega mensajes que **ya le pertenecen** pero que no confirmó (por ejemplo, si el proceso se reinició).
2. **Lectura de Nuevos:** Una vez limpia su propia PEL, empieza a leer con el ID `">"`, que trae mensajes que **nunca fueron entregados** a nadie.
3. **Auxilio a Terceros (Opcional):** Si el consumidor tiene tiempo libre, puede ejecutar `XPENDING` + `XCLAIM` para ayudar a procesar mensajes de otros compañeros que se quedaron "trabados" (Chaos Engineering).

---

## 4. Comandos de Monitoreo (`XINFO`)

Para saber qué está pasando en el Stream "desde afuera":

* `XINFO STREAM <key>`: Información general del stream (longitud, primer/último ID).
* `XINFO GROUPS <key>`: Estado de todos los Consumer Groups.
* `XINFO CONSUMERS <key> <group>`: Detalle de cada consumidor (cuántos mensajes tiene pendientes y su idle time).

---

## 🛠️ Resumen de comandos para la terminal

```bash
# Ver estado de los grupos
XINFO GROUPS numbers

# Ver quién tiene mensajes pendientes
XINFO CONSUMERS numbers primes

# Ver los 5 mensajes con más tiempo de inactividad
XPENDING numbers primes - + 5

# Reclamar un mensaje (ID 123-0) si lleva más de 1 minuto quieto
XCLAIM numbers primes BOB-0 60000 123-0

```

---
