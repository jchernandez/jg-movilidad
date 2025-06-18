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