from app.config.mysqlconnection import connectToMySQL
from flask import flash
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv("MYSQL_DB")

class Viaje:
    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo'].capitalize()
        self.descripcion = data['descripcion']
        self.fecha_inicio = data['fecha_inicio']
        self.fecha_fin = data['fecha_fin']
        self.creado_por = data['creado_por']
        self.fecha_creacion = data['fecha_creacion']

    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM viajes;"
        resultados = connectToMySQL(db).query_db(query)
        viajes = [cls(viaje) for viaje in resultados]
        return viajes
    
    @classmethod
    def guardar_viaje(cls, data):
        query = """
        INSERT INTO viajes (titulo, descripcion, fecha_inicio, fecha_fin, creado_por) 
        VALUES (%(titulo)s, %(descripcion)s, %(fecha_inicio)s, %(fecha_fin)s, %(creado_por)s);
        """
        resultado = connectToMySQL(db).query_db(query, data)
        return resultado
    
    @classmethod
    def unir_usuario(cls, usuario_id, viaje_id):
        # Verificar que el viaje existe
        viaje = cls.obtener_por_id(viaje_id)
        if not viaje:
            return False
        
        # Evitar duplicados
        existe_q = "SELECT 1 FROM usuarios_viajes WHERE usuario_id=%(usuario_id)s AND viaje_id=%(viaje_id)s;"
        data = {"usuario_id": usuario_id, "viaje_id": viaje_id}
        existe = connectToMySQL(db).query_db(existe_q, data)
        if existe:
            return None
        
        # Unir usuario con rol_id = 2 (participante)
        query = """
            INSERT INTO usuarios_viajes (usuario_id, viaje_id, rol_id)
            VALUES (%(usuario_id)s, %(viaje_id)s, 2);
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def salir_usuario(cls, usuario_id, viaje_id):
        query = """
            DELETE FROM usuarios_viajes
            WHERE usuario_id = %(usuario_id)s AND viaje_id = %(viaje_id)s;
        """
        data = {
            "usuario_id": usuario_id,
            "viaje_id": viaje_id
        }
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def obtener_viajes_usuario(cls, usuario_id):
        query = """
            SELECT v.* FROM viajes v
            JOIN usuarios_viajes uv ON v.id = uv.viaje_id
            WHERE uv.usuario_id = %(usuario_id)s;
        """
        data = {"usuario_id": usuario_id}
        resultados = connectToMySQL(db).query_db(query, data)
        return [cls(r) for r in resultados] if resultados else []

    @classmethod
    def usuario_ya_unido(cls, usuario_id, viaje_id):
        """Verifica si un usuario ya está unido a un viaje específico"""
        query = """
            SELECT 1 FROM usuarios_viajes 
            WHERE usuario_id = %(usuario_id)s AND viaje_id = %(viaje_id)s;
        """
        data = {"usuario_id": usuario_id, "viaje_id": viaje_id}
        resultado = connectToMySQL(db).query_db(query, data)
        return bool(resultado)


    
    @classmethod
    def obtener_por_id(cls, viaje_id):
        query = "SELECT * FROM viajes WHERE id = %(id)s;"
        data = {'id': viaje_id}
        resultado = connectToMySQL(db).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])
    
    @classmethod
    def actualizar_viaje(cls, viaje_id, data):
        query = """
        UPDATE viajes SET titulo = %(titulo)s, descripcion = %(descripcion)s, 
                           fecha_inicio = %(fecha_inicio)s, fecha_fin = %(fecha_fin)s 
        WHERE id = %(id)s AND creado_por = %(creado_por)s;
        """
        data['id'] = viaje_id
        resultado = connectToMySQL(db).query_db(query, data)
        return resultado
    
    @classmethod
    def eliminar_viaje(cls, viaje_id, usuario_id):
        # Borrar relaciones primero por integridad referencial
        connectToMySQL(db).query_db("DELETE FROM usuarios_viajes WHERE viaje_id = %(id)s;", {'id': viaje_id})
        query = "DELETE FROM viajes WHERE id = %(id)s AND creado_por = %(creado_por)s;"
        data = {'id': viaje_id, 'creado_por': usuario_id}
        resultado = connectToMySQL(db).query_db(query, data)
        return resultado
    
    @classmethod
    def obtener_viajes_creados_por_usuario(cls, usuario_id):
        query = "SELECT * FROM viajes WHERE creado_por = %(usuario_id)s;"
        data = {'usuario_id': usuario_id}
        resultados = connectToMySQL(db).query_db(query, data)
        viajes = [cls(viaje) for viaje in resultados]
        return viajes
    
    @classmethod
    def obtener_viajes_unidos_por_usuario(cls, usuario_id):
        query = """
        SELECT v.* FROM viajes v
        JOIN usuarios_viajes uv ON v.id = uv.viaje_id
        WHERE uv.usuario_id = %(usuario_id)s;
        """
        data = {'usuario_id': usuario_id}
        resultados = connectToMySQL(db).query_db(query, data)
        viajes = [cls(viaje) for viaje in resultados]
        return viajes
    
    @staticmethod
    def validar_viaje(viaje):
        is_valid = True
        if len(viaje['titulo']) < 3:
            flash("El título debe tener al menos 3 caracteres.", 'viaje')
            is_valid = False
        if len(viaje['descripcion']) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", 'viaje')
            is_valid = False
        if not viaje['fecha_inicio']:
            flash("La fecha de inicio es obligatoria.", 'viaje')
            is_valid = False
        if not viaje['fecha_fin']:
            flash("La fecha de fin es obligatoria.", 'viaje')
            is_valid = False
        elif viaje['fecha_inicio'] and viaje['fecha_fin']:
            if viaje['fecha_fin'] < viaje['fecha_inicio']:
                flash("La fecha de fin no puede ser anterior a la fecha de inicio.", 'viaje')
                is_valid = False
        return is_valid