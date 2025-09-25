import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD")
        )

        if connection.is_connected():
            print("Conexión a MySQL exitosa.")
            cursor = connection.cursor()

            cursor.execute(
                f"DROP DATABASE IF EXISTS {os.getenv('MYSQL_DB')}"
            )

            cursor.execute(
                f"CREATE SCHEMA IF NOT EXISTS {os.getenv('MYSQL_DB')} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci"
            )
            print(f"Base de datos '{os.getenv('MYSQL_DB')}' creada o ya existente.")

            cursor.execute(f"USE {os.getenv('MYSQL_DB')}")

            create_usuarios_table = """
            CREATE TABLE usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """

            cursor.execute(create_usuarios_table)
            print("Tabla 'usuarios' creada exitosamente.")

            create_viajes_table = """
            CREATE TABLE viajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(150) NOT NULL,
                descripcion TEXT,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE NOT NULL,
                creado_por INT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creado_por) REFERENCES usuarios(id) ON DELETE CASCADE
            );
            """

            cursor.execute(create_viajes_table)
            print("Tabla 'viajes' creada exitosamente.")

            create_usuarios_viajes_table = """
            CREATE TABLE usuarios_viajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                viaje_id INT NOT NULL,
                fecha_union TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (viaje_id) REFERENCES viajes(id) ON DELETE CASCADE,
                UNIQUE (usuario_id, viaje_id)
            );
            """

            cursor.execute(create_usuarios_viajes_table)
            print("Tabla 'usuarios_viajes' creada exitosamente.")

            cursor.execute("SET SQL_MODE=@OLD_SQL_MODE;")
            cursor.execute("SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;")
            cursor.execute("SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;")

            connection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada.")


if __name__ == "__main__":
    create_database()
