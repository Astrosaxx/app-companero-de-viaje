#!/usr/bin/env python3
"""
Script de instalación automática para Compañero de Viaje
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e.stderr}")
        return False

def check_python_version():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detectado")

def create_env_file():
    """Crea el archivo .env si no existe"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creando archivo .env...")
        env_content = """# Configuración de Base de Datos
MYSQL_DB=compañero_de_viaje_db
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña_mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Configuración de Seguridad
SECRET_KEY=clave_super_secreta_para_sesiones_12345

# Configuración de Desarrollo
FLASK_ENV=development
FLASK_DEBUG=True
"""
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
        print("⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales de MySQL")
    else:
        print("✅ Archivo .env ya existe")

def install_dependencies():
    """Instala las dependencias de Python"""
    if not run_command("pip install -r requirements.txt", "Instalando dependencias"):
        return False
    return True

def setup_database():
    """Configura la base de datos"""
    print("🗄️ Configurando base de datos...")
    
    # Importar después de instalar dependencias
    try:
        from app.config.mysqlconnection import connectToMySQL
        from dotenv import load_dotenv
        
        load_dotenv()
        db = os.getenv("MYSQL_DB")
        
        # Insertar roles básicos
        roles = [(1, 'Organizador'), (2, 'Participante')]
        for rol_id, nombre in roles:
            query = "INSERT IGNORE INTO roles_viaje (id, nombre) VALUES (%s, %s);"
            connectToMySQL(db).query_db(query, (rol_id, nombre))
            print(f"✅ Rol '{nombre}' insertado")
        
        print("✅ Base de datos configurada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        print("💡 Asegúrate de que MySQL esté ejecutándose y las credenciales sean correctas")
        return False

def main():
    """Función principal de instalación"""
    print("🚀 Instalando Compañero de Viaje...")
    print("=" * 50)
    
    # Verificar Python
    check_python_version()
    
    # Crear archivo .env
    create_env_file()
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error instalando dependencias")
        sys.exit(1)
    
    # Configurar base de datos
    if not setup_database():
        print("⚠️  Error configurando base de datos")
        print("💡 Puedes ejecutar manualmente: python setup_database.py")
    
    print("=" * 50)
    print("🎉 ¡Instalación completada!")
    print("")
    print("📋 Próximos pasos:")
    print("1. Edita el archivo .env con tus credenciales de MySQL")
    print("2. Ejecuta: python server.py")
    print("3. Abre tu navegador en: http://127.0.0.1:5014")
    print("")
    print("🛫 ¡Disfruta planificando tus viajes!")

if __name__ == "__main__":
    main()
