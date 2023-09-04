import psycopg2
import getpass
from datetime import datetime

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(database='postgres', user='postgres', password='12345', host='localhost', port='5432')
cur = conn.cursor()

def connect_to_db():
    return conn

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


 # Generar Reporte Ganancias       
def generar_reporte_ganancias(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) * 5.00 FROM registros WHERE fecha_salida IS NOT NULL;")
        total_ganancias = cur.fetchone()[0]

        print(f"Ganancias totales hasta la fecha: ${total_ganancias:.2f}")
    except Exception as e:
        print("Error al generar el reporte de ganancias:", e)

# Generar Reporte de Vehículos
def generar_reporte_vehiculos(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT marca, COUNT(*) FROM registros GROUP BY marca;")
        resultados = cur.fetchall()

        print("Reporte de Vehículos:")
        for marca, cantidad in resultados:
            print(f"{marca}: {cantidad}")
    except Exception as e:
        print("Error al generar el reporte de vehículos:", e)

# Función principal
def main():
    conn = connect_to_db()
    if conn:
        while True:
            print("1. Registrar entrada")
            print("2. Registrar salida")
            print("3. Generar Reporte Ganancias")
            print("4. Generar Reporte de Vehículos")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                registrar_entrada(conn)
            elif opcion == "2":
                registrar_salida(conn)
            elif opcion == "3":
                generar_reporte_ganancias(conn)
            elif opcion == "4":
                generar_reporte_vehiculos(conn)
            elif opcion == "5":
                conn.close()
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida, por favor seleccione una opción válida.")

if __name__ == "__main__":
    main()

