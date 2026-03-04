# 🔎 Indexación y Búsqueda: RediSearch vs. Sorted Sets

Por defecto, Redis Streams es una estructura de "solo lectura secuencial". Para buscar por el **contenido** (campos y valores) de los mensajes, debemos implementar una estrategia de indexación.

## 1. RediSearch: La Solución Nativa (Módulo)

RediSearch es un motor de búsqueda que crea índices automáticos sobre los Streams.

### Cómo funciona

1. **Definición del Índice:** Le indicas a Redis qué campos del Stream quieres rastrear.

```bash
FT.CREATE idx_usuarios ON STREAM usuarios SCHEMA rol TEXT SORTABLE edad NUMERIC

```

2.**Búsqueda:** Utilizas una sintaxis similar a SQL o Lucene.

```bash
FT.SEARCH idx_usuarios "@rol:ADMIN @edad:[18 30]"

```

### ✅ Ventajas

* **Multicampo:** Podés combinar filtros (rol AND edad AND país).
* **Full-Text Search:** Permite buscar palabras parciales o por similitud.
* **Abstracción:** No tenés que manejar estructuras extra manualmente.

---

## 2. Sorted Sets (ZSET): La Solución Manual

Si no tenés RediSearch, debés construir tu propio "índice secundario" usando un **Sorted Set**.

### Cómo funciona (Patrón de diseño)

Cada vez que guardas un mensaje en el Stream, guardas una referencia en un ZSET.

* **Score:** El valor numérico por el que querés buscar (ej. `precio` o `timestamp`).
* **Member:** El `ID` del mensaje en el Stream.

### ✅ Ventaja

* **Universal:** Funciona en cualquier versión de Redis (no requiere módulos).
* **Performance:** Es extremadamente rápido para rangos numéricos simples ($O(\log N)$).

---

## 3. ¿Cuál usar y cuándo?

| Caso de Uso | Usá RediSearch | Usá Sorted Sets (ZSET) |
| --- | --- | --- |
| **Búsqueda por Texto** | **Sí.** (ej: "buscame usuarios que se llamen 'Dan'"). | No es eficiente. |
| **Filtros Múltiples** | **Sí.** (ej: ADMIN + Argentina + Activo). | Difícil (requiere intersección de conjuntos). |
| **Rango Numérico Simple** | Es bueno. | **Excelente.** (ej: "temperaturas entre 20 y 30"). |
| **Memoria RAM** | Consume más (índices complejos). | Muy liviano. |
| **Infraestructura** | Requiere el módulo instalado. | Funciona en cualquier Redis. |

---

## 4. Consideraciones Técnicas Senior

### Sincronización (Solo para ZSETs)

Si usas Sorted Sets manualmente, tu código debe asegurar la **Atomicidad**. Si el `XADD` al Stream funciona pero el `ZADD` al índice falla, tus datos estarán corruptos.

* *Solución:* Usar **Transacciones (MULTI/EXEC)** o **Scripts de Lua** para asegurar que ambas operaciones ocurran o ninguna.

### El Costo del Índice

Recordá la regla de oro: **Cada índice que agregás es RAM que consumís.** * No indexes campos que no vas a usar para filtrar.

* Si solo necesitás el último estado de un usuario, quizás un **Hash** es mejor que un Stream indexado.

---

## 💡 Resumen para el Examen

* **RediSearch** es para búsquedas complejas, texto y filtros dinámicos.
* **Sorted Sets** son para índices secundarios manuales, principalmente numéricos o cronológicos.
* Redis Streams es **O(1)** para leer el final, pero **O(N)** para buscar contenido si no hay un índice.

---
