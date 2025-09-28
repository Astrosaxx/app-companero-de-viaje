from app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from bcrypt import checkpw
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]+$')

class Usuario:
    """
    Clase que representa a un usuario y sus operaciones en la base de datos.
    """
    db = os.getenv("MYSQL_DB") 

    def __init__(self, data):
        """
        Constructor: inicializa los atributos del usuario
        """
        self.id= data['id']
        self.nombre = data['nombre'].capitalize()
        self.apellido = data['apellido'].capitalize()
        self.email = data['email']
        self.password = data['password']
        self.fecha_registro = data['fecha_registro']

    @classmethod
    def guardar_usuario(cls, data):
        """
        Guardar un nuevo usuario en la base de datos
        """
        #Normaliza nombre y apellido aantes de guardar
        data['nombre'] = data['nombre'].capitalize()
        data['apellido'] = data['apellido'].capitalize()
        query = "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s,%(email)s,%(password)s);"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        return resultado
    @classmethod
    def obtener_por_email(cls, data):
        """
        Buscar un usuario por su email.
        """
        query = "SELECT * FROM usuarios WHERE email =%(email)s;"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])
    
   
    @classmethod
    def obtener_por_id(cls, usuario_id):
        """
        Buscar un usuario por su ID
        """
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {"id": usuario_id}
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])
   
    @staticmethod
    def validar_registro(usuario):
        """
        Valida los datos del formulario de registro.
        Devuelve True si todo es válido, False se hay errores (y los muestra con flash).
        """
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(Usuario.db).query_db(query,usuario)
        if resultado:
            flash("El email ya está registro.",'registro')
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Formato de email es inválido.", 'registro')
            is_valid = False
        if len(usuario ['nombre'])<3:
            flash("El nombre debe tener al menos 3 caracteres.", 'registro')
            is_valid =False
        if len(usuario['apellido'])< 3:
            flash("El apellido debe tener al menos 3 caractaeres.", 'registro')
            is_valid = False
        if len(usuario['password'])<8:
            flash("La contraseña debe tener al menos 8 caracteres.", 'registro')
            is_valid = False
        if usuario['password'] != usuario['confirm_password']:
            flash("Las contraseña no coinciden.", 'registro')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validar_login(usuario):
        """
        Valida los datos del formulario de login.
        Devuelve True si todo es válido, False se hay errores (y los muestra con flash).
        """
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(Usuario.db).query_db(query, usuario)
        if not resultado:
            flash("Email no registrado.", 'login')
            is_valid = False
        elif not checkpw(usuario['password'].encode(), resultado[0]['password'].encode()):
            flash("Contraseña incorrecta.", 'login')
            is_valid = False
        return is_valid

    @classmethod
    def obtener_usuarios_por_viaje(cls, viaje_id):
        """
        Lista los usuarios que se unieron a un viaje (incluye creador si está en la tabla de relación).
        """
        query = (
            "SELECT u.* FROM usuarios u "
            "JOIN usuarios_viajes uv ON u.id = uv.usuario_id "
            "WHERE uv.viaje_id = %(viaje_id)s;"
        )
        resultados = connectToMySQL(cls.db).query_db(query, {"viaje_id": viaje_id})
        return [cls(r) for r in resultados] if resultados else []

    @classmethod
    def actualizar_usuario(cls, data, usuario_id):
        """
        Actualizar información del usuario
        """
        query = """
        UPDATE usuarios SET nombre = %(nombre)s, apellido = %(apellido)s, 
                           email = %(email)s WHERE id = %(id)s;
        """
        data['id'] = usuario_id
        resultado = connectToMySQL(cls.db).query_db(query, data)
        return resultado

    @staticmethod
    def validar_actualizacion(data, usuario_id):
        """
        Validar datos para actualización de usuario
        """
        is_valid = True
        
        # Validar email si ha cambiado
        query = "SELECT email FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL(Usuario.db).query_db(query, {'id': usuario_id})
        email_actual = resultado[0]['email'] if resultado else ''
        
        if data['email'] != email_actual:
            query = "SELECT * FROM usuarios WHERE email = %(email)s;"
            resultado = connectToMySQL(Usuario.db).query_db(query, data)
            if resultado:
                flash("El email ya está registrado.", 'error')
                is_valid = False
        
        if not EMAIL_REGEX.match(data['email']):
            flash("Formato de email es inválido.", 'error')
            is_valid = False
            
        if len(data['nombre']) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", 'error')
            is_valid = False
            
        if len(data['apellido']) < 3:
            flash("El apellido debe tener al menos 3 caracteres.", 'error')
            is_valid = False
            
        return is_valid
    
    
    @classmethod
    def obtener_viajes_unidos_por_usuario(cls, usuario_id):
        """
        Devuelve todos los viajes en los que un usuario está unido
        """
        query = """
            SELECT v.* FROM viajes v
            JOIN usuarios_viajes uv ON v.id = uv.viaje_id
            WHERE uv.usuario_id = %(usuario_id)s;
        """
        data = {"usuario_id": usuario_id}
        resultados = connectToMySQL(cls.db).query_db(query, data)
        return [cls(resultado) for resultado in resultados] if resultados else []