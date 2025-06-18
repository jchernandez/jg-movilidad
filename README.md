# 🚍 Importador de Datos de Movilidad a PostgreSQL
Este script en Python permite cargar datos de transacciones de movilidad desde un archivo CSV a una base de datos PostgreSQL. Automatiza la creación de la base de datos y la tabla si no existen, y maneja errores durante la carga.

# 📦 Requisitos
- PostgreSQL (Mac o Windows)
- Python 3.8 o superior
- Acceso a terminal (macOS/Linux) o PowerShell (Windows)

# 🐘 Instalación de PostgreSQL
En macOS (usando Homebrew)
```bash
brew install postgresql
brew services start postgresql
```
En Windows
Descarga el instalador desde: https://www.postgresql.org/download/windows/
Durante la instalación, elige una contraseña fácil de recordar (ej: password1) y guarda el puerto (por defecto es 5432).
Finaliza y asegúrate de que el servicio esté iniciado.

👤 Crear usuario y base de datos
Abre una terminal (macOS/Linux) o SQL Shell (psql) en Windows.
Escribe lo siguiente para crear un usuario:
``` sql
CREATE USER user1 WITH PASSWORD 'password1';
ALTER USER user1 CREATEDB;
```
# 🐍 Instalación de Python 3 y entorno virtual
En MacOS
```bash
brew install 
```
En Windows
Descarga Python desde: https://www.python.org/downloads/
Durante la instalación, marca la opción "Add Python to PATH".
Luego en PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\activate
```
# 📂 Ya en el proyecto
```bash
cd datos-movilidad
python -m venv venv
source venv/bin/activate  # o en Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

# ▶️ Cómo usar el programa
Con tu archivo CSV listo (y con cabecera), ejecuta:

```bash
python cargar_csv.py archivo.csv
```
Reemplaza archivo.csv por el nombre de tu archivo real.

# 🧪 Qué hace el script
- Verifica si existe la base de datos datos_movilidad. Si no, la crea.
- Conecta como user1 con contraseña password1.
- Crea la tabla transacciones si no existe.
- Carga cada fila del CSV y maneja errores automáticamente.

# 📌 Notas importantes
- Asegúrate de que tu archivo CSV tenga exactamente 38 columnas.
- Si el script falla al insertar una fila, mostrará el error y continuará con la siguiente.

# 🧹 Reiniciar desde cero (opcional)
Si quieres borrar todo y empezar de nuevo:

```sql
DROP DATABASE datos_movilidad;
DROP USER user1;
```

# Como usar la BD

# 🔎 1. Consultas básicas

Conectarse a la base de datos
Abre tu terminal (o psql en Windows desde el menú de inicio si instalaste PostgreSQL con PgAdmin) y ejecuta:

```bash
psql -U user1 -d datos_movilidad
```

📌 Nota: Si PostgreSQL te pide contraseña, escribe password1 (o la que hayas definido).

Una vez dentro, verás algo como:

```text
datos_movilidad=#
```

Ya estás dentro del cliente interactivo de PostgreSQL y puedes ejecutar SQL directamente.


Obtener los primeros 10 registros:
```sql
SELECT * FROM transacciones LIMIT 10;
````
Ver cuántas transacciones hay:
```sql
SELECT COUNT(*) FROM transacciones;
```
Ver los distintos tipos de tarjeta:
```sql
SELECT DISTINCT tipo_tarjeta FROM transacciones;
```
# 📅 2. Consultas por fecha
Transacciones realizadas en un día específico:
```sql
SELECT * 
FROM transacciones 
WHERE fecha_hora_transaccion::date = '2025-06-07';
```
Rango de fechas:
```sql
SELECT * 
FROM transacciones 
WHERE fecha_hora_transaccion BETWEEN '2025-06-01' AND '2025-06-07';
```
# 📊 3. Agregaciones y estadísticas
Total de transacciones por línea:
```sql
SELECT linea, COUNT(*) AS total_transacciones 
FROM transacciones 
GROUP BY linea 
ORDER BY total_transacciones DESC;
```
Saldo promedio antes de la transacción por tipo de tarjeta:
```sql
SELECT tipo_tarjeta, AVG(saldo_antes_transaccion) AS saldo_promedio
FROM transacciones
GROUP BY tipo_tarjeta
ORDER BY saldo_promedio DESC;
```
Suma de montos por día:
```sql
SELECT fecha_hora_transaccion::date AS fecha, SUM(monto_transaccion) AS total_monto
FROM transacciones
GROUP BY fecha
ORDER BY fecha;
```
# 🚍 4. Consultas por ruta o estación
Transacciones por estación específica (ej. estación 16):
```sql
SELECT * FROM transacciones WHERE estacion = 16;
```
Top 5 rutas más utilizadas:
```sql
SELECT ruta, COUNT(*) AS total
FROM transacciones
GROUP BY ruta
ORDER BY total DESC
LIMIT 5;
```
# 🧪 5. Consultas de control y diagnóstico
Transacciones donde el saldo después es negativo o nulo (posibles errores):
```sql
SELECT * 
FROM transacciones 
WHERE saldo_despues_transaccion <= 0;
Fila con el monto de transacción más alto:
```
```sql
SELECT * 
FROM transacciones 
ORDER BY monto_transaccion DESC 
LIMIT 1;
```
# 🧩 6. Consultas de contrato
Transacciones con contratos válidos actualmente (fecha actual dentro de la vigencia):
```sql
SELECT * 
FROM transacciones 
WHERE contract_validity_start_date IS NOT NULL
  AND contract_validity_duration > 0
  AND CURRENT_DATE BETWEEN contract_validity_start_date 
                      AND contract_validity_start_date + contract_validity_duration;
```