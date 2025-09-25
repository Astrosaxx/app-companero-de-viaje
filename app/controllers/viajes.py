from app.models.usuario_model import Usuario
from app.models.viaje_model import Viaje
from flask import render_template, redirect, request, session, Blueprint, flash

bp = Blueprint('citas', __name__, url_prefix='/travels')

def verificar_sesion():
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", 'error')
        return redirect('/')
    return True

@bp.route('/', methods=['GET'])
def dashboard():
    verificar_sesion()
    
    usuario = Usuario.obtener_por_id({'id': session['usuario_id']})
    viajes = Viaje.obtener_todos()
    viajes_creados_por_usuario = [viaje for viaje in viajes if viaje.creado_por == usuario.id]
    viajes_no_creados_por_usuario = [viaje for viaje in viajes if viaje.creado_por != usuario.id]
    viajes_unidos = []
    for viaje in viajes_no_creados_por_usuario:
        if any(uv['viaje_id'] == viaje.id and uv['usuario_id'] == usuario.id for uv in Usuario.obtener_viajes_unidos_por_usuario({'id': usuario.id})):
            viajes_unidos.append(viaje)
    viajes_disponibles = [viaje for viaje in viajes_no_creados_por_usuario if viaje not in viajes_unidos]

    
    return render_template('dashboard.html', usuario=usuario, viajes=viajes, viajes_creados_por_usuario=viajes_creados_por_usuario, viajes_unidos=viajes_unidos, viajes_disponibles=viajes_disponibles)

@bp.route('/crear', methods=['POST'])
def crear_viaje():
    verificar_sesion()
    
    if not Viaje.validar_viaje(request.form):
        return redirect('/travels')
    
    data = {
        **request.form,
        'creado_por': session['usuario_id']
    }
    Viaje.guardar_viaje(data)
    flash("¡Viaje creado exitosamente!", 'exito')
    return redirect('/travels')

@bp.route('/editar/<int:viaje_id>', methods=['GET', 'POST'])
def editar_viaje(viaje_id):
    verificar_sesion()
    
    viaje = Viaje.obtener_por_id(viaje_id)
    if not viaje or viaje.creado_por != session['usuario_id']:
        flash("No tienes permiso para editar este viaje.", 'error')
        return redirect('/travels')
    
    if request.method == 'POST':
        if not Viaje.validar_viaje(request.form):
            return redirect(f'/travels/editar/{viaje_id}')
        
        data = {
            **request.form,
            'creado_por': session['usuario_id']
        }
        Viaje.actualizar_viaje(viaje_id, data)
        flash("¡Viaje actualizado exitosamente!", 'exito')
        return redirect('/travels')
    
    return render_template('editar_viaje.html', viaje=viaje)

@bp.route('/validar_edicion', methods=['POST'])
def validar_edicion():
    verificar_sesion()
    
    viaje_id = request.form.get('viaje_id')
    if not viaje_id:
        flash("ID de viaje no proporcionado.", 'error')
        return redirect('/travels')
    
    return redirect(f'/travels/editar/{viaje_id}')

@bp.route('/eliminar/<int:viaje_id>', methods=['POST'])
def eliminar_viaje(viaje_id):
    verificar_sesion()
    
    viaje = Viaje.obtener_por_id(viaje_id)
    if not viaje or viaje.creado_por != session['usuario_id']:
        flash("No tienes permiso para eliminar este viaje.", 'error')
        return redirect('/travels')
    
    Viaje.eliminar_viaje(viaje_id)
    flash("¡Viaje eliminado exitosamente!", 'exito')
    return redirect('/travels')

@bp.route('/unir/<int:viaje_id>', methods=['POST'])
def unir_viaje(viaje_id):
    verificar_sesion()
    
    viaje = Viaje.obtener_por_id(viaje_id)
    if not viaje:
        flash("El viaje no existe.", 'error')
        return redirect('/travels')
    
    Viaje.unir_usuario(session['usuario_id'], viaje_id)
    flash("¡Te has unido al viaje exitosamente!", 'exito')
    return redirect('/travels')

@bp.route('/salir/<int:viaje_id>', methods=['POST'])
def salir_viaje(viaje_id):
    verificar_sesion()
    
    viaje = Viaje.obtener_por_id(viaje_id)
    if not viaje:
        flash("El viaje no existe.", 'error')
        return redirect('/travels')
    
    Viaje.salir_usuario(session['usuario_id'], viaje_id)
    flash("¡Has salido del viaje exitosamente!", 'exito')
    return redirect('/travels')


@bp.route('/detalle/<int:viaje_id>', methods=['GET'])
def detalle_viaje(viaje_id):
    verificar_sesion()
    
    viaje = Viaje.obtener_por_id(viaje_id)
    if not viaje:
        flash("El viaje no existe.", 'error')
        return redirect('/travels')
    
    usuario = Usuario.obtener_por_id({'id': session['usuario_id']})
    participantes = Usuario.obtener_usuarios_por_viaje(viaje_id)
    
    return render_template('detalle_viaje.html', viaje=viaje, usuario=usuario, participantes=participantes)

