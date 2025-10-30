import mysql.connector
from mysql.connector import Error

class SQLHandler:
    """
    Class to handle SQL database operations for inserting keys into the 'invites' table.
    """
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def _connect(self):
        """Stablish the connection to the database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                collation='utf8mb4_general_ci' 
            )
            if self.connection.is_connected():
                print("🔌 Conexión a la base de datos MariaDB establecida.")
                return True
        except Error as e:
            print(f"❌ Error al conectar a MariaDB: {e}")
            return False

    def _disconnect(self):
        """Close the connection if it's open."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Conexión a la base de datos cerrada.")

    def insert_keys(self, keys: list):
        """
        Insert a list of keys into the 'invites' table.
        """
        if not keys:
            print("⚠️ No hay claves para insertar.")
            return

        if not self._connect():
            return
            
        cursor = self.connection.cursor()
        
        # SQL insert query
        query = "INSERT INTO invites (code) VALUES (%s)"
        
        # Prepare data for insertion
        data_to_insert = [(key,) for key in keys]

        try:
            print(f"💾 Insertando {len(keys)} clave(s) en la base de datos...")
            cursor.executemany(query, data_to_insert)
            self.connection.commit() # Confirm the changes
            print(f"✅ ¡Éxito! Se insertaron {cursor.rowcount} claves en la tabla 'invites'.")
        
        except Error as e:
            print(f"❌ Error de SQL al insertar claves: {e}")
            self.connection.rollback() # Revert changes if there's an error
        finally:
            cursor.close()
            self._disconnect()