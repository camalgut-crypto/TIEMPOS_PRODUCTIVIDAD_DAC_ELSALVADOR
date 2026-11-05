# Tiempos DAC El Salvador

Tiempos de respuesta y productividad del Departamento de Análisis de Crédito (Instacredit El Salvador, país 4).
Es una copia independiente de [Tiempos DAC Nicaragua](https://github.com/camalgut-crypto/TIEMPOS_PRODUCTIVIDAD_DAC).

Enlace: https://camalgut-crypto.github.io/TIEMPOS_PRODUCTIVIDAD_DAC_ELSALVADOR/

## Diferencias con Nicaragua

- **Datos**: mismo proyecto de Supabase, esquema propio `dac_sv`. Usuarios (`@tiemposdac-sv.local`) y sesión también van aparte.
- **Consultas**: país 4. El histórico toma desde enero de 2026 hasta el mes anterior; la consulta mensual, el mes en curso y el anterior, para seguir actualizando las solicitudes que se resuelven después de un cambio de mes.
- **Jornada**: L-V 8:00–18:00 y sábado 8:00–12:00. El sábado sigue valiendo 0.5 día hábil.
- **Metas**: PERS ≤ 30 min, PYME ≤ 50 min.
- **Productos**: PYME (`PYME` o `PYMES` en el sistema); todo lo demás es PERS: ASALARIADO, NO ASALARIADO y PERSONAL. No hay motos por el momento; para agregarlas hay que devolver MOTO a `PRODUCTOS` (`public/calculos.js`) y a `producto()` (`worker/tiempos_dac/motor.py`).
- **Feriados**: solo los nacionales de El Salvador, inamovibles: si caen domingo no se reponen. Se administran en Vacaciones y calendario.

- **Motor y Flujo Rápido**: el motor no aprueba. Es del motor lo `RECHAZADO POR MOTOR` o `PRECALIFICADO MOTOR` que no llegó a un analista, y la solicitud termina ahí. Su tiempo se mide de `PRE ANALISIS` a la primera respuesta del motor; un rechazo que llega días después de precalificar no cuenta como tiempo.
- **`PRECALIFICADO MOTOR` con analista**: productividad y tiempo son del analista, y el tiempo empieza en ANALISTA ASIGNADO.
- **Productividad**: una sola del departamento (solicitudes ÷ días disponibles de los analistas) y una por analista, porque todos atienden todos los productos. Capacidad instalada usa la misma.
- **`RECHAZADO`**: cuenta como decisión del analista y cierra su tramo.
- **Gerencia**: registra resoluciones pero no es analista; su tiempo no se le cuenta y los tramos no quedan a su nombre.
- **Sin preaprobado condicionado**: ese estado no existe en El Salvador; el menú está oculto. PENDIENTES queda con el mismo analista y su tiempo no se le cuenta.

Las demás reglas de cálculo son las de la herramienta de Nicaragua y están en `worker/tiempos_dac/motor.py` y `public/calculos.js`.

## Cómo está armado

- `public/`: la página. Cada `push` a `main` la publica en GitHub Pages.
- `supabase/schema.sql`: esquema `dac_sv` con tablas, seguridad por rol (RLS), funciones, feriados y permisos.
- `worker/`: proceso de actualización en Python. Debe correr en un equipo de la red interna, porque ahí está el datawarehouse.

## Puesta en marcha (una sola vez)

1. En Supabase › **SQL Editor**, ejecutar `supabase/schema.sql`.
2. En Supabase, agregar `dac_sv` a **Exposed schemas** (Project Settings › Data API), conservando los que ya están.
3. En el equipo de la red, desde la carpeta del proyecto:
   ```
   py -3.12 -m venv .venv
   .venv\Scripts\python -m pip install -r requirements.txt
   .venv\Scripts\python worker\generar_semilla.py
   ```
4. Ejecutar `data/semilla.sql` en el SQL Editor. Crea los usuarios iniciales y el de sistema; no se sube a Git.
5. Cargar los datos:
   ```
   .venv\Scripts\python worker\actualizar.py --historico
   .venv\Scripts\python worker\actualizar.py --una-vez
   ```
6. En la app, Administración: agregar los analistas con el nombre que trae la carga y crear sus usuarios.
7. Programar `Ejecutar actualizacion.bat` al iniciar sesión en ese equipo, como una tarea distinta a la de Nicaragua.

Las credenciales del datawarehouse son las mismas de la herramienta de Nicaragua (`modulo_garantias_sql` en el Administrador de credenciales).

## Vista previa local

```
.venv\Scripts\python worker\actualizar.py --local
.venv\Scripts\python -m http.server 3000 --directory public
```

Abrir `http://localhost:3000/?local`. Usa `public/local/datos.json` y guarda lo registrado solo en el navegador. Contraseña de todos: 12345678.
