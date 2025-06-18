import psycopg2
import csv
import argparse
import datetime

def crear_base_de_datos():
    """
    Función para crear la base de datos si no existe.
    """
    # Conexión al servidor PostgreSQL
    conn = psycopg2.connect(
        dbname="datos_movilidad",  # Conéctate a la base de datos predeterminada
        user="user1",
        password="password1",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True  # Habilitar autocommit para crear la base de datos
    cursor = conn.cursor()

    # Crear la base de datos si no existe
    cursor.execute("""
        SELECT 1 FROM pg_database WHERE datname = 'datos_movilidad';
    """)
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE datos_movilidad;")
        print("Base de datos 'datos_movilidad' creada exitosamente.")
    else:
        print("La base de datos 'datos_movilidad' ya existe.")

    cursor.close()
    conn.close()

def verificar_y_crear_tabla():
    print("Conectando a la base datos_movilidad para verificar tabla...")
    conn = psycopg2.connect(
        dbname="datos_movilidad",
        user="user1",
        password="password1",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'transacciones'
        );
    """)
    exists = cursor.fetchone()[0]

    if not exists:
        print("Tabla no existe, creando tabla...")
        cursor.execute("""
            CREATE TABLE transacciones (
                id_transaccion_organismo BIGINT,
                provider INT,
                tipo_tarjeta INT,
                numero_serie_hex VARCHAR(50),
                fecha_hora_transaccion TIMESTAMP,
                linea INT,
                estacion INT,
                autobus VARCHAR(10),
                ruta INT,
                equipo INT,
                tipo_equipo INT,
                location_id TEXT,
                tipo_transaccion INT,
                saldo_antes_transaccion INT,
                monto_transaccion INT,
                saldo_despues_transaccion INT,
                perfil1 INT,
                perfil2 INT,
                perfil3 INT,
                sam_serial_hex_ultima_recarga VARCHAR(50),
                sam_serial_hex VARCHAR(50),
                contador_recargas INT,
                contador_validaciones INT,
                event_log TEXT,
                load_log TEXT,
                purchase_log TEXT,
                mac TEXT,
                counter_value INT,
                counter_amount INT,
                sam_counter INT,
                environment TEXT,
                environment_issuer_id TEXT,
                contract TEXT,
                contract_tariff INT,
                contract_sale_sam TEXT,
                contract_restrict_time INT,
                contract_validity_start_date DATE,
                contract_validity_duration INT
            );
        """)
        conn.commit()  # Muy importante hacer commit aquí!
        print("Tabla 'transacciones' creada exitosamente.")
    else:
        print("La tabla 'transacciones' ya existe.")

    cursor.close()
    conn.close()


def cargar_datos(csv_path):
    """
    Función para cargar datos desde un archivo CSV a la base de datos PostgreSQL.
    """
    conn = psycopg2.connect(
        dbname="datos_movilidad",
        user="user1",
        password="password1",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Leer el archivo CSV e insertar los datos
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Saltar la cabecera
        for row in reader:
            #print(f"Procesando fila: {row}")  # Imprime la fila para depuración
            try:
                if len(row) != 38:
                    raise ValueError(f"La fila no tiene 38 columnas: {len(row)} columnas encontradas")

                # Conversión de fecha
                try:
                    row[4] = datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass

                try:
                    row[36] = datetime.datetime.strptime(row[36], "%Y-%m-%d").date()
                except Exception:
                    pass

                cursor.execute("""
                    INSERT INTO transacciones (
                        id_transaccion_organismo, provider, tipo_tarjeta, numero_serie_hex,
                        fecha_hora_transaccion, linea, estacion, autobus, ruta, equipo,
                        tipo_equipo, location_id, tipo_transaccion, saldo_antes_transaccion,
                        monto_transaccion, saldo_despues_transaccion, perfil1, perfil2, perfil3,
                        sam_serial_hex_ultima_recarga, sam_serial_hex, contador_recargas,
                        contador_validaciones, event_log, load_log, purchase_log, mac,
                        counter_value, counter_amount, sam_counter, environment,
                        environment_issuer_id, contract, contract_tariff, contract_sale_sam,
                        contract_restrict_time, contract_validity_start_date, contract_validity_duration
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, tuple(row))
            except Exception as e:
                print(f"Error al insertar fila: {row}")
                print(f"Detalle del error: {e}")
                conn.rollback()  # <- ROLLBACK para limpiar el estado
            else:
                conn.commit()  # <- COMMIT si no hubo error
    # Confirmar cambios y cerrar conexión
    cursor.close()
    conn.close()


if __name__ == "__main__":
    # Configurar argparse para recibir la ruta del archivo como parámetro
    parser = argparse.ArgumentParser(description="Cargar datos desde un archivo CSV a PostgreSQL.")
    parser.add_argument("csv_path", help="Ruta del archivo CSV")
    args = parser.parse_args()

    # Crear la base de datos si no existe
    crear_base_de_datos()
    verificar_y_crear_tabla()

    # Llamar a la función para cargar los datos
    cargar_datos(args.csv_path)