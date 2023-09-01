import psycopg2
import getpass
from datetime import datetime

# Conexión a la base de datos PostgreSQL
def connect_to_db():
    try:
        user = input("Ingrese el nombre de usuario: ")
        password = getpass.getpass("Ingrese la contraseña: ")  # Usando getpass para ocultar la contraseña
        database = "parqueo_db"
        conn = psycopg2.connect(
            user=user,
            password=password,
            database=database
        )
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Registrar la entrada de un vehículo
def registrar_entrada(conn):
    try:
        cur = conn.cursor()

        marca = input("Ingrese la marca del vehículo: ")
        placa = input("Ingrese la placa del vehículo: ")
        color = input("Ingrese el color del vehículo: ")

        now = datetime.now()
        fecha_hora_entrada = now.strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("INSERT INTO registros (marca, placa, color, fecha_entrada) VALUES (%s, %s, %s, %s) RETURNING id;", (marca, placa, color, fecha_hora_entrada))
        registro_id = cur.fetchone()[0]
        conn.commit()

        print(f"Vehículo registrado con número de registro: {registro_id}")
    except Exception as e:
        print("Error al registrar la entrada:", e)

# Registrar la salida de un vehículo
def registrar_salida(conn):
    try:
        cur = conn.cursor()

        registro_id = int(input("Ingrese el número de registro del vehículo: "))
        now = datetime.now()
        fecha_hora_salida = now.strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("UPDATE registros SET fecha_salida = %s WHERE id = %s;", (fecha_hora_salida, registro_id))
        conn.commit()

        print("Salida registrada correctamente.")
    except Exception as e:
        print("Error al registrar la salida:", e)

# Función principal
def main():
    conn = connect_to_db()
    if conn:
        while True:
            print("1. Registrar entrada")
            print("2. Registrar salida")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                registrar_entrada(conn)
            elif opcion == "2":
                registrar_salida(conn)
            elif opcion == "3":
                conn.close()
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida, por favor seleccione una opción válida.")

if __name__ == "__main__":
    main()

