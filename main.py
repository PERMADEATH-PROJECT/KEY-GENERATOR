import getpass
from logic import generate_keys
from sql_handler import SQLHandler

def main():
    """
    Main function to run the key generation and insertion process.
    """
    print("--- Generador de Claves para s30_launcher ---")

    # --- Collect user input ---
    try:
        amount_to_generate = int(input("¿Cuántas claves quieres generar?: "))
        if amount_to_generate <= 0:
            print("Por favor, introduce un número positivo.")
            return
    except ValueError:
        print("Error: Debes introducir un número entero.")
        return

    print("\n--- Credenciales de la Base de Datos ---")
    db_host = input("Host de la base de datos (ej: 192.168.1.100): ")
    db_user = input("Usuario de la base de datos: ")
    db_password = getpass.getpass("Contraseña de la base de datos: ")
    db_name = input("Nombre de la base de datos (ej: s30_launcher): ")
    
    # key generation and insertion process
    keys = generate_keys(amount_to_generate)
    
    if not keys:
        print("No se generaron claves. Saliendo.")
        return

    db_handler = SQLHandler(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    # Insert keys into the database
    db_handler.insert_keys(keys)
    
    print("\n--- Proceso finalizado ---")


if __name__ == "__main__":
    main()