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
    resp = verificar_sesion()
    if resp is not True:
        return resp
    
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    
    viajes = Viaje.obtener_todos()
    viajes_creados_por_usuario = [v for v in viajes if v.creado_por == usuario.id]
    viajes_unidos = Viaje.obtener_viajes_usuario(usuario.id)
    
    # Filtramos disponibles: no creados y no unidos
    ids_unidos = [v.id for v in viajes_unidos]
    viajes_disponibles = [
        v for v in viajes 
        if v.creado_por != usuario.id and v.id not in ids_unidos
    ]
    
    return render_template(
        'dashboard.html',
        usuario=usuario,
        viajes_creados_por_usuario=viajes_creados_por_usuario,
        viajes_unidos=viajes_unidos,
        viajes_disponibles=viajes_disponibles
    )

@bp.route('/crear', methods=['POST'])
def crear_viaje():
    resp = verificar_sesion()
    if resp is not True:
        return resp
    
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
    resp = verificar_sesion()
    if resp is not True:
        return resp
    
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
    resp = verificar_sesion()
    if resp is not True:
        return resp
    
    viaje_id = request.form.get('viaje_id')
    if not viaje_id:
        flash("ID de viaje no proporcionado.", 'error')
        return redirect('/travels')
    
    return redirect(f'/travels/editar/{viaje_id}')

@bp.route('/eliminar/<int:viaje_id>', methods=['POST'])
def eliminar_viaje(viaje_id):
    resp = verificar_sesion()
    if resp is not True:
        return resp
    
    viaje = Viaje.obtener_por_id(viaje_id)
    if not viaje or viaje.creado_por != session['usuario_id']:
        flash("No tienes permiso para eliminar este viaje.", 'error')
        return redirect('/travels')
    
    Viaje.eliminar_viaje(viaje_id, session['usuario_id'])
    flash("¡Viaje eliminado exitosamente!", 'exito')
    return redirect('/travels')

@bp.route('/unir/<int:viaje_id>', methods=['POST'])
def unir_viaje(viaje_id):
    resp = verificar_sesion()
    if resp is not True:
        return resp
    
    viaje = Viaje.obtener_por_id(viaje_id)
    if not viaje:
        flash("El viaje no existe.", 'error')
        return redirect('/travels')
    
    if viaje.creado_por == session['usuario_id']:
        flash("No puedes unirte a tu propio viaje.", 'error')
        return redirect('/travels')
    
    resultado = Viaje.unir_usuario(session['usuario_id'], viaje_id)
    if resultado is None:
        flash("Ya estás unido a este viaje.", 'error')
    elif resultado is False:
        flash("No se pudo unir al viaje. Inténtalo nuevamente.", 'error')
    else:
        # Verifica inmediatamente si aparece en la membresía
        unidos = Viaje.obtener_viajes_usuario(session['usuario_id'])
        if any(v.id == viaje_id for v in unidos):
            flash("¡Te has unido al viaje exitosamente!", 'exito')
        else:
            flash("No se pudo confirmar la unión al viaje.", 'error')
    return redirect('/travels')

@bp.route('/salir/<int:viaje_id>', methods=['POST'])
def salir_viaje(viaje_id):
    resp = verificar_sesion()
    if resp is not True:
        return resp
    
    viaje = Viaje.obtener_por_id(viaje_id)
    if not viaje:
        flash("El viaje no existe.", 'error')
        return redirect('/travels')
    
    Viaje.salir_usuario(session['usuario_id'], viaje_id)
    flash("¡Has salido del viaje exitosamente!", 'exito')
    return redirect('/travels')


@bp.route('/detalle/<int:viaje_id>', methods=['GET'])
def detalle_viaje(viaje_id):
    resp = verificar_sesion()
    if resp is not True:
        return resp
    
    viaje = Viaje.obtener_por_id(viaje_id)
    if not viaje:
        flash("El viaje no existe.", 'error')
        return redirect('/travels')
    
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    participantes = Usuario.obtener_usuarios_por_viaje(viaje_id)
    
    return render_template('detalle_viaje.html', viaje=viaje, usuario=usuario, participantes=participantes)

