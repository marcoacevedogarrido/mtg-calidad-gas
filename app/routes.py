from functools import wraps
from flask import render_template, redirect, flash, request, jsonify, abort
from flask_login import login_user, current_user, login_required, logout_user
import flask_admin.contrib.sqla
from flask_admin.contrib import sqla
from flask import url_for
from werkzeug.urls import url_parse
import json
from datetime import datetime, timedelta
from app import admin, app, excel
from app.forms import MainForm, LoginForm, UsuarioForm, LaboratoristaForm, PcontrolForm, TipoRedForm, \
    ResponsableControlForm, TramoForm, RegionForm, ValidadorForm, SecForm, BaseUserForm, \
    ReportesForm, InformesDiariosForm
from app.models import *
from app.helpers.server_data import *
from app.forms import ResetPasswordRequestForm
from app.email import send_email, send_password_reset_email
from app.forms import ResetPasswordForm

if app.debug:
    @app.before_first_request
    def create_user():
        print("running debug mode DB and scripts")
        db.drop_all()
        db.create_all()

        # Create test user
        new_rol = Rol(name='admin', rol_email='admin@test.net')
        db.session.add(new_rol)
        new_rol = Rol(name='operador', rol_email='operadores@test.net')
        db.session.add(new_rol)
        db.session.commit()

        new_user = User(username="admin", email="admin@test.net", rol_id=1)

        new_user.set_password('password')
        db.session.add(new_user)
        db.session.commit()

        # Create base data
        create_region(db)
        create_tramo(db)
        create_tipo_red(db)
        create_punto_control(db)
        create_tipo_combustible(db)
        create_clasificacion_control(db)
        create_responsable_control(db)
        create_laboratorista(db)





def check_rol(role='ANY'):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user_rol = current_user.get_rol().name
            if user_rol != role:
                return abort(404)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route('/', methods=['GET', 'POST'])
@login_required
def main():
    forms_data = GasForm.query.all()
    forms_data_tables = [g.return_quick_info for g in forms_data]

    form = SecForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            fecha_inicio_parsed = datetime.strptime(str(form.fecha_inicio.data), "%Y-%m-%d")
            fecha_fin_parsed = datetime.strptime(str(form.fecha_fin.data), "%Y-%m-%d")

            if (fecha_fin_parsed - fecha_inicio_parsed).days < 0:
                flash("La fecha de inicio no puede superar la fecha de fin")
                return redirect(url_for('main'))

            forms_data = GasForm.query.filter(
                GasForm.fecha_muestra.between(fecha_inicio_parsed, fecha_fin_parsed)).all()
            forms_data_tables = [g.return_quick_info for g in forms_data]
            print(forms_data_tables)
            return render_template('index.html', forms_data=forms_data_tables, form=form)
        else:
            print(form.errors)
    return render_template('index.html', forms_data=forms_data_tables, form=form)


@app.route('/api/punto_control/<nombre>')
@login_required
def api_punto_control(nombre):
    punto_control = PuntoControl.query.filter_by(name=nombre).first_or_404()
    return jsonify([punto_control.tipo_red.name,
                    punto_control.region.name,
                    punto_control.tramo.name])


@app.route('/formulario', methods=['GET', 'POST'])
@login_required
def formulario():
    form = MainForm()
    form.laboratorista.choices = [(str(l.id), l.name) for l in Laboratorista.query.order_by('name')]
    form.punto_control.choices = [(p.name, p.descripcion) for p in PuntoControl.query.order_by('name')]

    if request.method == 'POST':
        if form.validate_on_submit():
            punto_control = PuntoControl.query.filter_by(name=form.punto_control.data).first()
            print(form.poder_calorifico_superior.data)
            new_gas_form = GasForm(
                tipo_combustible_id=form.tipo_combustible.data,
                punto_control_id=punto_control.id,
                clasificacion_control_id=form.clasificacion_control.data,
                responsable_control_id=form.responsable_control.data,
                laboratorista_id=form.laboratorista.data,
                fecha_muestra=form.fecha_muestra.data,
                resultado_odorizacion=form.resultado_odorizacion.data,
                resultado_impurezas=form.resultado_impurezas.data,
                poder_calorifico_superior=form.poder_calorifico_superior.data,
                poder_calorifico_inferior=form.poder_calorifico_inferior.data,
                indice_wobbe=form.indice_wobbe.data,
                densidad_relativa=form.densidad_relativa.data,
                gases_inertes_pmol=form.gases_inertes_pmol.data,
                punto_rocio_hydrocarburos=form.punto_rocio_hydrocarburos.data,
                dioxido_de_carbono=form.dioxido_de_carbono.data,
                dioxido_de_carbono_pmol=form.dioxido_de_carobono_pmol.data,
                oxigeno_pvv=form.oxigeno_pvv.data,
                oxigeno_pmol=form.oxigeno_pmol.data,
                suluro_hidrogeno=form.suluro_hidrogeno.data,
                azufre_antes_odorizar=form.azufre_antes_odorizar.data,
                azufre_despues_odorizar=form.azufre_despues_odorizar.data,
                agua=form.agua.data,
                metano=form.metano.data,
                etano=form.etano.data,
                propano=form.propano.data,
                butano=form.butano.data,
                pentano=form.pentano.data,
                hexano=form.hexano.data,
                nitrogeno=form.nitrogeno.data,
                propano_e_hidrocarburos_superiores=form.propano_e_hidrocarburos_superiores.data,
                hexano_hydrocarburos=form.hexano_hydrocarburos.data,
                hidrogeno=form.hidrogeno.data,
                monoxido_carobono=form.monoxido_carbono.data,
                porcentaje_vol_gas=form.porcentaje_vol_gas.data
            )
            db.session.add(new_gas_form)
            db.session.commit()
            return jsonify({'status': 'ok'})
        else:
            return jsonify(form.errors)

    title = 'Creacion nuevo registro calidad del gas'
    return render_template('formulario.html', form=form, title=title)


@app.route('/formulario/<int:id>')
@login_required
def read_form(id):
    gasform = GasForm.query.filter_by(id=id).first_or_404()

    form = MainForm()
    form.laboratorista.choices = [(str(l.id), l.name) for l in Laboratorista.query.order_by('name')]
    form.punto_control.choices = [(p.name, p.descripcion) for p in PuntoControl.query.order_by('name')]

    form.punto_control.data = gasform.punto_control.name
    form.tipo_combustible.data = str(gasform.tipo_combustible_id)
    form.clasificacion_control.data = str(gasform.clasificacion_control_id)
    form.responsable_control.data = str(gasform.responsable_control_id)
    form.laboratorista.data = str(gasform.laboratorista_id)
    form.fecha_muestra.data = gasform.fecha_muestra
    form.resultado_odorizacion.data = gasform.resultado_odorizacion
    form.resultado_impurezas.data = gasform.resultado_impurezas
    form.poder_calorifico_superior.data = gasform.poder_calorifico_superior
    form.poder_calorifico_inferior.data = gasform.poder_calorifico_inferior
    form.indice_wobbe.data = gasform.indice_wobbe
    form.densidad_relativa.data = gasform.densidad_relativa
    form.gases_inertes_pmol.data = gasform.gases_inertes_pmol
    form.punto_rocio_hydrocarburos.data = gasform.punto_rocio_hydrocarburos
    form.dioxido_de_carbono.data = gasform.dioxido_de_carbono
    form.dioxido_de_carobono_pmol.data = gasform.dioxido_de_carbono_pmol
    form.oxigeno_pvv.data = gasform.oxigeno_pvv
    form.oxigeno_pmol.data = gasform.oxigeno_pmol
    form.suluro_hidrogeno.data = gasform.suluro_hidrogeno
    form.azufre_antes_odorizar.data = gasform.azufre_antes_odorizar
    form.azufre_despues_odorizar.data = gasform.azufre_despues_odorizar
    form.agua.data = gasform.agua
    form.metano.data = gasform.metano
    form.etano.data = gasform.etano
    form.propano.data = gasform.propano
    form.butano.data = gasform.butano
    form.pentano.data = gasform.pentano
    form.hexano.data = gasform.hexano
    form.nitrogeno.data = gasform.nitrogeno
    form.propano_e_hidrocarburos_superiores.data = gasform.propano_e_hidrocarburos_superiores
    form.hexano_hydrocarburos.data = gasform.hexano_hydrocarburos
    form.hidrogeno.data = gasform.hidrogeno
    form.monoxido_carbono.data = gasform.monoxido_carobono
    form.porcentaje_vol_gas.data = gasform.porcentaje_vol_gas

    punto_control = PuntoControl.query.filter_by(id=gasform.punto_control_id).first()
    tipo_red = punto_control.tipo_red.name
    region = punto_control.region.name
    tramo = punto_control.tramo.name

    title = 'Registro calidad del gas id {}'.format(gasform.id)
    return render_template('formulario_readonly.html',
                           form=form,
                           title=title,
                           tipo_red=tipo_red,
                           region=region,
                           tramo=tramo,
                           readonly=True
                           )


@app.route('/mantenedores/eformulario/<int:eformulario_id>', methods=['POST', 'GET'])
@login_required
def eformulario_edit(eformulario_id):
    edited_gasform = GasForm.query.filter_by(id=eformulario_id).first_or_404()
    form = MainForm()
    form.laboratorista.choices = [(str(l.id), l.name) for l in Laboratorista.query.order_by('name')]
    form.punto_control.choices = [(p.name, p.descripcion) for p in PuntoControl.query.order_by('name')]

    if form.validate_on_submit():
        punto_control = PuntoControl.query.filter_by(name=form.punto_control.data).first()
        edited_gasform.tipo_combustible_id = form.tipo_combustible.data
        edited_gasform.punto_control_id = punto_control.id
        edited_gasform.clasificacion_control_id = form.clasificacion_control.data
        edited_gasform.responsable_control_id = form.responsable_control.data
        edited_gasform.laboratorista_id = form.laboratorista.data
        edited_gasform.fecha_muestra = form.fecha_muestra.data
        edited_gasform.resultado_odorizacion = form.resultado_odorizacion.data
        edited_gasform.resultado_impurezas = form.resultado_impurezas.data
        edited_gasform.poder_calorifico_superior = form.poder_calorifico_superior.data
        edited_gasform.poder_calorifico_inferior = form.poder_calorifico_inferior.data
        edited_gasform.indice_wobbe = form.indice_wobbe.data
        edited_gasform.densidad_relativa = form.densidad_relativa.data
        edited_gasform.gases_inertes_pmol= form.gases_inertes_pmol.data
        edited_gasform.punto_rocio_hydrocarburos = form.punto_rocio_hydrocarburos.data
        edited_gasform.dioxido_de_carbono = form.dioxido_de_carbono.data
        edited_gasform.dioxido_de_carobono_pmol = form.dioxido_de_carobono_pmol.data
        edited_gasform.oxigeno_pvv = form.oxigeno_pvv.data
        edited_gasform.oxigeno_pmol = form.oxigeno_pmol.data
        edited_gasform.suluro_hidrogeno = form.suluro_hidrogeno.data
        edited_gasform.azufre_antes_odorizar = form.azufre_antes_odorizar.data
        edited_gasform.azufre_despues_odorizar = form.azufre_despues_odorizar.data
        edited_gasform.agua = form.agua.data
        edited_gasform.metano = form.metano.data
        edited_gasform.etano = form.etano.data
        edited_gasform.propano = form.propano.data
        edited_gasform.butano = form.butano.data
        edited_gasform.pentano = form.pentano.data
        edited_gasform.hexano = form.hexano.data
        edited_gasform.nitrogeno = form.nitrogeno.data
        edited_gasform.propano_e_hidrocarburos_superiores = form.propano_e_hidrocarburos_superiores.data
        edited_gasform.hexano_hydrocarburos = form.hexano_hydrocarburos.data
        edited_gasform.hidrogeno = form.hidrogeno.data
        edited_gasform.monoxido_carbono = form.monoxido_carbono.data
        edited_gasform.porcentaje_vol_gas = form.porcentaje_vol_gas.data
        db.session.add(edited_gasform)
        db.session.commit()
        flash('Formulario editado')
        return redirect(url_for('read_form', id=eformulario_id))

    form.tipo_combustible.data = str(edited_gasform.tipo_combustible_id)
    form.punto_control.data = str(edited_gasform.punto_control_id)
    form.clasificacion_control.data = str(edited_gasform.clasificacion_control_id)
    form.responsable_control.data = str(edited_gasform.responsable_control_id)
    form.laboratorista.data = str(edited_gasform.laboratorista_id)
    form.fecha_muestra.data = edited_gasform.fecha_muestra
    form.resultado_odorizacion.data = edited_gasform.resultado_odorizacion
    form.resultado_impurezas.data = edited_gasform.resultado_impurezas
    form.poder_calorifico_superior.data = edited_gasform.poder_calorifico_superior
    form.poder_calorifico_inferior.data = edited_gasform.poder_calorifico_inferior
    form.indice_wobbe.data = edited_gasform.indice_wobbe
    form.densidad_relativa.data = edited_gasform.densidad_relativa
    form.gases_inertes_pmol.data = edited_gasform.gases_inertes_pmol
    form.punto_rocio_hydrocarburos.data = edited_gasform.punto_rocio_hydrocarburos
    form.dioxido_de_carbono.data = edited_gasform.dioxido_de_carbono
    form.dioxido_de_carobono_pmol.data = edited_gasform.dioxido_de_carbono_pmol
    form.oxigeno_pvv.data = edited_gasform.oxigeno_pvv
    form.oxigeno_pmol.data = edited_gasform.oxigeno_pmol
    form.suluro_hidrogeno.data = edited_gasform.suluro_hidrogeno
    form.azufre_antes_odorizar.data = edited_gasform.azufre_antes_odorizar
    form.azufre_despues_odorizar.data = edited_gasform.azufre_despues_odorizar
    form.agua.data = edited_gasform.agua
    form.metano.data = edited_gasform.metano
    form.etano.data = edited_gasform.etano
    form.butano.data = edited_gasform.butano
    form.pentano.data = edited_gasform.pentano
    form.hexano.data = edited_gasform.hexano
    form.nitrogeno.data = edited_gasform.nitrogeno
    form.propano_e_hidrocarburos_superiores.data = edited_gasform.propano_e_hidrocarburos_superiores
    form.hexano_hydrocarburos.data = edited_gasform.hexano_hydrocarburos
    form.monoxido_carbono.data = edited_gasform.monoxido_carobono
    form.porcentaje_vol_gas.data = edited_gasform.porcentaje_vol_gas
    return render_template('mantenedores/eformulario.html', form=form, edited_gasform=edited_gasform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/mantenedores')
@check_rol("admin")
def mantenedores():
    return render_template('mantenedores.html')


@app.route('/mantenedores/laboratoristas')
@login_required
@check_rol("admin")
def laboratorista():
    laboratorista = Laboratorista.query.all()
    return render_template('mantenedores/lista_laboratorista.html', laboratorista=laboratorista)


@app.route('/mantenedores/laboratorista/crear', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def laboratorista_create():
    form = LaboratoristaForm()
    if form.validate_on_submit():
        new_laboratorista = Laboratorista(name=form.name.data, email=form.email.data)
        db.session.add(new_laboratorista)
        db.session.commit()
        flash('Laboratorista Registrado!')
        return redirect(url_for('laboratorista'))
    return render_template('mantenedores/reg_laboratorista.html', form=form, create_laboratorista=create_laboratorista)


@app.route('/matenedores/laboratorista/<int:laboratorista_id>', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def laboratorista_edit(laboratorista_id):
    edited_laboratorista = Laboratorista.query.filter_by(id=laboratorista_id).first_or_404()
    form = LaboratoristaForm()

    if form.validate_on_submit():
        edited_laboratorista.name = form.name.data
        edited_laboratorista.email = form.email.data
        db.session.add(edited_laboratorista)
        db.session.commit()
        flash('Laboratorista editado')
        return redirect(url_for('laboratorista'))

    form.name.data = edited_laboratorista.name
    form.email.data = edited_laboratorista.email
    return render_template('mantenedores/laboratorista.html', form=form, edited_laboratorista=edited_laboratorista)


@app.route('/matenedores/laboratorista/<int:laboratorista_id>/delete', methods=['GET'])
@login_required
@check_rol("admin")
def laboratista_delete(laboratorista_id):
    edited_laboratorista = Laboratorista.query.filter_by(id=laboratorista_id).first_or_404()
    db.session.delete(edited_laboratorista)
    db.session.commit()
    flash('Laboratorista eliminado')
    return redirect(url_for('laboratorista'))


@app.route("/mantenedores/puntoscontrol")
@login_required
@check_rol("admin")
def pcontrol():
    puntoscontrol = PuntoControl.query.all()
    return render_template("mantenedores/lista_pcontrol.html", puntoscontrol=puntoscontrol)


@app.route('/matenedores/pcontrol/<int:pcontrol_id>', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def pcontrol_edit(pcontrol_id):
    edited_punto_control = PuntoControl.query.filter_by(id=pcontrol_id).first_or_404()
    form = PcontrolForm()
    form.tipo_de_red_id.choices = [(str(p.id), p.name) for p in TipoRed.query.all()]
    form.region_id.choices = [(str(p.id), p.name) for p in Region.query.all()]
    form.tramo_id.choices = [(str(p.id), p.name) for p in Tramo.query.all()]

    if form.validate_on_submit():
        edited_punto_control.name = form.name.data
        edited_punto_control.region_id = form.region_id.data
        edited_punto_control.tipo_red_id = form.tipo_de_red_id.data
        edited_punto_control.tramo_id = form.tramo_id.data
        edited_punto_control.descripcion = form.descripcion.data
        db.session.add(edited_punto_control)
        db.session.commit()
        flash('Punto de Control editado')
        return redirect(url_for('pcontrol'))

    form.name.data = edited_punto_control.name
    form.region_id.data = str(edited_punto_control.region_id)
    form.tipo_de_red_id.data = str(edited_punto_control.tipo_red_id)
    form.tramo_id.data = str(edited_punto_control.tramo_id)
    form.descripcion.data = edited_punto_control.descripcion
    return render_template('mantenedores/pcontrol.html', form=form, edited_punto_control=edited_punto_control)


@app.route('/matenedores/pcontrol/crear', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def pcontrol_create():
    form = PcontrolForm()
    form.tipo_de_red_id.choices = [(str(p.id), p.name) for p in TipoRed.query.all()]
    form.region_id.choices = [(str(p.id), p.name) for p in Region.query.all()]
    form.tramo_id.choices = [(str(p.id), p.name) for p in Tramo.query.all()]
    if form.validate_on_submit():
        new_punto_control = PuntoControl(name=form.name.data,
                                         region_id=form.region_id.data,
                                         tipo_red_id=form.tipo_de_red_id.data,
                                         tramo_id=form.tramo_id.data,
                                         descripcion=form.descripcion.data)
        db.session.add(new_punto_control)
        db.session.commit()
        flash('Punto de Control Creado!')
        return redirect(url_for('pcontrol'))
    return render_template('mantenedores/reg_pcontrol.html', form=form, create_punto_control=create_punto_control)


@app.route('/matenedores/pcontrol/<int:pcontrol_id>/delete', methods=['GET'])
@login_required
@check_rol("admin")
def pcontrol_delete(pcontrol_id):
    edited_puntocontrol = PuntoControl.query.filter_by(id=pcontrol_id).first_or_404()
    db.session.delete(edited_puntocontrol)
    db.session.commit()
    flash('Punto de Control eliminado')
    return redirect(url_for('pcontrol'))


@app.route("/mantenedores/tiposred")
@login_required
@check_rol("admin")
def tipored():
    tiposred = TipoRed.query.all()
    return render_template("mantenedores/lista_tipored.html", tiposred=tiposred)


@app.route('/matenedores/tipored/<int:tipored_id>', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def tipored_edit(tipored_id):
    edited_tipo_red = TipoRed.query.filter_by(id=tipored_id).first_or_404()
    form = TipoRedForm()

    if form.validate_on_submit():
        edited_tipo_red.name = form.name.data
        db.session.add(edited_tipo_red)
        db.session.commit()
        flash('Tipo de Red editado')
        return redirect(url_for('tipored'))

    form.name.data = edited_tipo_red.name
    return render_template('mantenedores/tipored.html', form=form, edited_tipo_red=edited_tipo_red)


@app.route('/matenedores/tipored/crear', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def tipored_create():
    form = TipoRedForm()

    if form.validate_on_submit():
        new_tipo_red = TipoRed(name=form.name.data)
        db.session.add(new_tipo_red)
        db.session.commit()
        flash('Tipo de Red Creado!')
        return redirect(url_for('tipored'))
    return render_template('mantenedores/reg_tipored.html', form=form, create_tipo_red=create_tipo_red)


@app.route('/matenedores/tipored/<int:tipored_id>/delete', methods=['GET'])
@login_required
@check_rol("admin")
def tipored_delete(tipored_id):
    edited_tipored = TipoRed.query.filter_by(id=tipored_id).first_or_404()
    db.session.delete(edited_tipored)
    db.session.commit()
    flash('Tipo de Red eliminado')
    return redirect(url_for('tipored'))


@app.route("/mantenedores/rescontrol")
@login_required
@check_rol("admin")
def rcontrol():
    rescontrol = ResponsableControl.query.all()
    return render_template("mantenedores/lista_rcontrol.html", rescontrol=rescontrol)


@app.route('/matenedores/rcontrol/<int:rcontrol_id>', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def rcontrol_edit(rcontrol_id):
    edited_responsable_control = ResponsableControl.query.filter_by(id=rcontrol_id).first_or_404()
    form = ResponsableControlForm()

    if form.validate_on_submit():
        edited_responsable_control.name = form.name.data
        db.session.add(edited_responsable_control)
        db.session.commit()
        flash('Responsable de Control editado')
        return redirect(url_for('rcontrol'))

    form.name.data = edited_responsable_control.name
    return render_template('mantenedores/rcontrol.html', form=form,
                           edited_responsable_control=edited_responsable_control)


@app.route('/matenedores/rcontrol/crear', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def rcontrol_create():
    form = ResponsableControlForm()

    if form.validate_on_submit():
        new_responsable_control = ResponsableControl(name=form.name.data)
        db.session.add(new_responsable_control)
        db.session.commit()
        flash('Responsable de Control Creado!')
        return redirect(url_for('rcontrol'))
    return render_template('mantenedores/reg_rcontrol.html', form=form,
                           create_responsable_control=create_responsable_control)


@app.route('/matenedores/rcontrol/<int:rcontrol_id>/delete', methods=['GET'])
@login_required
@check_rol("admin")
def rcontrol_delete(rcontrol_id):
    edited_rcontrol = ResponsableControl.query.filter_by(id=rcontrol_id).first_or_404()
    db.session.delete(edited_rcontrol)
    db.session.commit()
    flash('Responsable de Control eliminado')
    return redirect(url_for('rcontrol'))


@app.route("/mantenedores/tramos")
@login_required
@check_rol("admin")
def tramo():
    tramos = Tramo.query.all()
    return render_template("mantenedores/lista_tramo.html", tramos=tramos)


@app.route('/matenedores/tramo/<int:tramo>', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def tramo_edit(tramo):
    edited_t_tramo = Tramo.query.filter_by(id=tramo).first_or_404()
    form = TramoForm()

    if form.validate_on_submit():
        edited_t_tramo.name = form.name.data
        db.session.add(edited_t_tramo)
        db.session.commit()
        flash('Tramo editado')
        return redirect(url_for('tramo'))

    form.name.data = str(edited_t_tramo.name)
    return render_template('mantenedores/tramo.html', form=form, edited_t_tramo=edited_t_tramo)


@app.route('/matenedores/tramo/crear', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def tramo_create():
    form = TramoForm()
    if form.validate_on_submit():
        new_t_tramo = Tramo(name=form.name.data)
        db.session.add(new_t_tramo)
        db.session.commit()
        flash('Tramo Creado!')
        return redirect(url_for('tramo'))
    return render_template('mantenedores/reg_tramo.html', form=form, create_t_tramo=create_tramo)


@app.route('/matenedores/tramo/<int:tramo_id>/delete', methods=['GET'])
@login_required
@check_rol("admin")
def tramo_delete(tramo_id):
    edited_tramo = Tramo.query.filter_by(id=tramo_id).first_or_404()
    db.session.delete(edited_tramo)
    db.session.commit()
    flash('Tramo eliminado')
    return redirect(url_for('tramo'))


@app.route("/mantenedores/regiones")
@login_required
@check_rol("admin")
def region():
    regiones = Region.query.all()
    return render_template("mantenedores/lista_region.html", regiones=regiones)


@app.route('/matenedores/region/<int:region>', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def region_edit(region):
    edited_r_region = Region.query.filter_by(id=region).first_or_404()
    form = RegionForm()

    if form.validate_on_submit():
        edited_r_region.region = form.region.data
        db.session.add(edited_r_region)
        db.session.commit()
        flash('Region editada')
        return redirect(url_for('region'))
    else:
        print(form.errors)
    form.name.data = str(edited_r_region.name)
    return render_template('mantenedores/region.html', form=form, edited_r_region=edited_r_region)


@app.route('/matenedores/region/crear', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def region_create():
    form = RegionForm()
    if form.validate_on_submit():
        new_r_region = Region(name=form.name.data)
        db.session.add(new_r_region)
        db.session.commit()
        flash('Region Creada!')
        return redirect(url_for('region'))
    return render_template('mantenedores/reg_region.html', form=form, create_r_region=create_region)


@app.route('/matenedores/region/<int:region_id>/delete', methods=['GET'])
@login_required
@check_rol("admin")
def region_delete(region_id):
    edited_region = Region.query.filter_by(id=region_id).first_or_404()
    db.session.delete(edited_region)
    db.session.commit()
    flash('Region eliminada')
    return redirect(url_for('region'))


@app.route('/administrador/usuario')
@login_required
@check_rol("admin")
@check_rol("admin")
def usuario():
    usuario = User.query.all()
    return render_template('administrador/lista_usuario.html', usuario=usuario)


@app.route('/administrador/usuario/crear', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def usuario_create():
    form = UsuarioForm()
    form.rol.choices = [(str(l.id), l.name) for l in Rol.query.order_by('name')]
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            rol_id=form.rol.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuario Registrado!')
        return redirect(url_for('usuario'))
    return render_template('administrador/reg_usuario.html', form=form)


@app.route('/administrador/usuario/<int:usuario_id>', methods=['POST', 'GET'])
@login_required
@check_rol("admin")
def usuario_edit(usuario_id):
    edited_usuario = User.query.filter_by(id=usuario_id).first_or_404()
    form = BaseUserForm()
    form.rol.choices = [(str(l.id), l.name) for l in Rol.query.order_by('name')]

    if form.validate_on_submit():
        edited_usuario.username = form.username.data
        edited_usuario.email = form.email.data
        edited_usuario.rol_id = form.rol.data
        if form.password.data:
            edited_usuario.set_password(form.password.data)
        db.session.add(edited_usuario)
        db.session.commit()
        flash('Usuario editado')
        return redirect(url_for('usuario'))

    form.username.data = edited_usuario.username
    form.email.data = edited_usuario.email
    form.rol.data = str(edited_usuario.rol_id)
    return render_template('administrador/usuario.html', form=form, edited_usuario=edited_usuario)


@app.route('/administrador/usuario/<int:usuario_id>/delete', methods=['GET'])
@login_required
@check_rol("admin")
def usuario_delete(usuario_id):
    edited_usuario = User.query.filter_by(id=usuario_id).first_or_404()
    db.session.delete(edited_usuario)
    db.session.commit()
    flash('Usuario eliminado')
    return redirect(url_for('usuario'))


@app.route('/mantenedores/validadores', methods=['GET', 'POST'])
@login_required
@check_rol("admin")
def validadores():
    form = ValidadorForm()
    data = json.load(open('app/variables/validador.json', 'r'))

    if form.validate_on_submit():
        for elem in form:
            if elem.id != "csrf_token" and elem.id != 'submit':
                if elem.id.split('_')[0] == "min":
                    data['normal']['validador_inferior'][elem.id[4:]] = elem.data
                else:
                    data['normal']['validador_superior'][elem.id] = elem.data

        newdata = open('app/variables/validador.json', 'w+')
        newdata.write(json.dumps(data))
        newdata.close()
        flash('datos guardados')
        return redirect(url_for('main'))

    for elem in form:
        if elem.id != "csrf_token" and elem.id != 'submit':
            if elem.id.split('_')[0] == "min":
                elem.data = data['normal']['validador_inferior'][elem.id[4:]]
            else:
                elem.data = data['normal']['validador_superior'][elem.id]

    form.poder_calorifico_superior_min = data['normal']['validador_inferior']['poder_calorifico_superior']
    form.indice_wobbe_min = data['normal']['validador_inferior']['indice_wobbe']

    return render_template('mantenedores/validadores.html', form=form)


@app.route('/api/validadores')
@login_required
def get_validadores():
    data = json.load(open('app/variables/validador.json', 'r'))
    return jsonify(data)


@app.route('/informes/elementos', methods=['GET','POST'])
def reportes_elementos():
    forms_data = GasForm.query.all()
    puntoscontrol = PuntoControl.query.order_by('name').all()
    form = ReportesForm()
    form.punto_control.choices = [(str(p.id), p.descripcion) for p in puntoscontrol]

    if request.method == 'POST':
        if form.validate_on_submit():
            fecha_inicio_parsed = datetime.strptime(str(form.fecha_inicio.data), "%Y-%m-%d")
            fecha_fin_parsed = datetime.strptime(str(form.fecha_fin.data), "%Y-%m-%d")

            if (fecha_fin_parsed - fecha_inicio_parsed).days < 0:
                return jsonify({"error": "La fecha de inicio no puede superar la fecha de fin"})
            forms_database = GasForm.query.filter(
                GasForm.fecha_muestra.between(fecha_inicio_parsed, fecha_fin_parsed)).all()

            response = {
                'fecha_muestra': [],
                'indices': {
                    'poder_calorifico_superior': [],
                    'poder_calorifico_inferior': [],
                    'indice_wobbe': [],
                    'densidad_relativa': [],
                    'gases_inertes_pmol': [],
                    'punto_rocio_hydrocarburos': [],
                    'resultado_odorizacion': [],
                    'resultado_impurezas': []
                },
                'elementos': {
                    'agua': [],
                    'metano': [],
                    'etano': [],
                    'propano': [],
                    'butano': [],
                    'pentano': [],
                    'hexano': [],
                    'nitrogeno': [],
                    'propano_e_hidrocarburos_superiores': [],
                    'hexano_hydrocarburos': [],
                    'hidrogeno': [],
                    'monoxido_carobono': [],
                    'porcentaje_vol_gas': []
                },
                'laboratorista': {
                    'laboratorista': []
                }
            }

            for gasform in forms_database:
                response['fecha_muestra'].append(gasform.fecha_muestra.strftime('%d-%m-%Y'))
                response['indices']['poder_calorifico_superior'].append(str(gasform.poder_calorifico_superior)),
                response['indices']['poder_calorifico_inferior'].append(str(gasform.poder_calorifico_inferior)),
                response['indices']['indice_wobbe'].append(str(gasform.indice_wobbe)),
                response['indices']['densidad_relativa'].append(str(gasform.densidad_relativa)),
                response['indices']['gases_inertes_pmol'].append(str(gasform.gases_inertes_pmol)),
                response['indices']['punto_rocio_hydrocarburos'].append(str(gasform.punto_rocio_hydrocarburos)),
                response['indices']['resultado_odorizacion'].append(str(gasform.resultado_odorizacion)),
                response['indices']['resultado_impurezas'].append(str(gasform.resultado_impurezas)),

                response['elementos']['agua'].append(str(gasform.agua)),
                response['elementos']['metano'].append(str(gasform.metano)),
                response['elementos']['etano'].append(str(gasform.etano)),
                response['elementos']['propano'].append(str(gasform.propano)),
                response['elementos']['butano'].append(str(gasform.butano)),
                response['elementos']['pentano'].append(str(gasform.pentano)),
                response['elementos']['hexano'].append(str(gasform.hexano)),
                response['elementos']['nitrogeno'].append(str(gasform.nitrogeno)),
                response['elementos']['propano_e_hidrocarburos_superiores'].append(str(gasform.propano_e_hidrocarburos_superiores)),
                response['elementos']['hexano_hydrocarburos'].append(str(gasform.hexano_hydrocarburos)),
                response['elementos']['hidrogeno'].append(str(gasform.hidrogeno)),
                response['elementos']['monoxido_carobono'].append(str(gasform.monoxido_carobono)),
                response['elementos']['porcentaje_vol_gas'].append(str(gasform.porcentaje_vol_gas)),

            return jsonify(response)
        else:
            print(form.fecha_inicio.data)
            print(form.punto_control.data)
            print(form.errors)
    return render_template('informes/grafico_elementos.html', form=form, puntoscontrol=puntoscontrol, forms_data=forms_data)


@app.route('/informes/codigo_sec', methods=['GET', 'POST'])
@login_required
def sec():
    forms_data = GasForm.query.all()
    forms_data_tables = [g.return_quick_info for g in forms_data]
    form_data_tables_ids = [g.id for g in forms_data]

    form = SecForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            fecha_inicio_parsed = datetime.strptime(str(form.fecha_inicio.data), "%Y-%m-%d")
            fecha_fin_parsed = datetime.strptime(str(form.fecha_fin.data), "%Y-%m-%d")

            if (fecha_fin_parsed - fecha_inicio_parsed).days < 0:
                flash("La fecha de inicio no puede superar la fecha de fin")
                return redirect(url_for('main'))

            forms_data = GasForm.query.filter(
                GasForm.fecha_muestra.between(fecha_inicio_parsed, fecha_fin_parsed)).all()
            forms_data_tables = [g.return_quick_info for g in forms_data]
            form_data_tables_ids = [g.id for g in forms_data]
            print(forms_data_tables)
            return render_template('informes/codigosec.html',
                                   forms_data=forms_data_tables, form=form, form_data_tables_ids=form_data_tables_ids)
        else:
            print(form.errors)
    return render_template('informes/codigosec.html', forms_data=forms_data_tables, form=form, form_data_tables_ids=form_data_tables_ids)


@app.route('/informes/codigo_sec/csv',)
@login_required
def sec_download_csv():
    req_data = request.args.getlist('id_formulario')

    if not req_data:
        return "NO DATA"

    response_array = []

    for gasform_id in req_data:
        gas_form = GasForm.query.filter_by(id=gasform_id).first()

        params_trama = []
        trama_sec = ";"

        params_trama.append("121")  # parametro por defecto, ID Empresa
        params_trama.append(str(gas_form.punto_control.region.name))
        params_trama.append(str(gas_form.punto_control.tramo.id))
        params_trama.append(str(gas_form.punto_control.tipo_red.id))
        params_trama.append(str(gas_form.tipo_combustible.id))
        params_trama.append(str(gas_form.punto_control.name))
        params_trama.append(str(gas_form.punto_control.descripcion))
        params_trama.append(str(gas_form.clasificacion_control.id))
        params_trama.append(str(gas_form.responsable_control.id))
        params_trama.append("IDM" + str(gas_form.id + 9000))
        params_trama.append("1")
        params_trama.append(str(gas_form.fecha_muestra.strftime('%d-%m-%Y')))
        resultado_odorizacion = 1 if gas_form.resultado_odorizacion else 0
        params_trama.append(str(resultado_odorizacion))
        resultado_impurezas = 1 if gas_form.resultado_impurezas else 0
        params_trama.append(str(resultado_impurezas))
        params_trama.append(str(gas_form.poder_calorifico_superior))
        params_trama.append(str(gas_form.poder_calorifico_inferior))
        params_trama.append(str(gas_form.indice_wobbe))
        params_trama.append(str(gas_form.densidad_relativa))
        params_trama.append(str(gas_form.gases_inertes_pmol))
        params_trama.append(str(gas_form.punto_rocio_hydrocarburos))
        params_trama.append(str(gas_form.dioxido_de_carbono))
        params_trama.append(str(gas_form.dioxido_de_carbono_pmol))
        params_trama.append(str(gas_form.oxigeno_pvv))
        params_trama.append(str(gas_form.oxigeno_pmol))
        params_trama.append(str(gas_form.suluro_hidrogeno))
        params_trama.append(str(gas_form.azufre_antes_odorizar))
        params_trama.append(str(gas_form.azufre_despues_odorizar))
        params_trama.append(str(gas_form.agua))
        params_trama.append(str(gas_form.metano))
        params_trama.append(str(gas_form.etano))
        params_trama.append(str(gas_form.propano))
        params_trama.append(str(gas_form.butano))
        params_trama.append(str(gas_form.pentano))
        params_trama.append(str(gas_form.hexano))
        params_trama.append(str(gas_form.nitrogeno))
        params_trama.append(str(gas_form.propano_e_hidrocarburos_superiores))
        params_trama.append(str(gas_form.hexano_hydrocarburos))
        params_trama.append(str(gas_form.hidrogeno))
        params_trama.append(str(gas_form.monoxido_carobono))

        response = trama_sec.join(params_trama).replace('None', '')

        response_array.append([str(gas_form.punto_control.name), response])

    return excel.make_response_from_array(response_array, "csv", file_name=u"codigo_sec")


@app.route('/formulario/<int:id_formulario_gas>/getform', methods=['GET'])
@login_required
def getform(id_formulario_gas):
    gas_form = GasForm.query.filter_by(id=id_formulario_gas).first_or_404()

    #  FORMATO DE TRAMAS A ENTREGAR AL CLIENTE - CODIGO SEC
    # <Id_empresa>;<Region>;<Id_Tramo>;<Id_Tipo_Red>;<Id_Tipo_Combustible>;<Id_Punto_Control>;
    # <Descripcion_Punto_Control>;<Clasificacion_Control>;<Responsable_Control>;<Id_Muestra>;
    # <Id_Certificado>;<Fecha_Informe>;<Odorizacion>;<Impurezas>;<Poder_Calorifico>;
    # <Indice_Wobbe>;<Densidad_Relativa>;<Gases_Inertes_pmol>;<Punto_Rocio_Hydrocarburos>;
    # <Dioxido_Carbono>;<Dioxido_Carbono_pmol>;<Oxigeno_ppv>;<Oxigeno_pmol>;
    # <Sulfuro_Hydrogeno>;<Azufre_antes_Odorizar>;<Azufre_Despues_Odorizar>;<Agua>;<Metano>;
    # <Etano>;<Proano>;<Butano>;<Pentano>;<Hexano>;<Nitrogeno>;
    # <Propano_e_Hydrocarburos_Superiores>;<Hexano_Hydrocarburos>;<Hidrogeno>;<Monoxido_Carbono>;

    params_trama = []
    trama_sec = ";"
    params_trama.append("121")  # parametro por defecto, ID Empresa
    params_trama.append(str(gas_form.punto_control.region.name))
    params_trama.append(str(gas_form.punto_control.tramo.id))
    params_trama.append(str(gas_form.punto_control.tipo_red.id))
    params_trama.append(str(gas_form.tipo_combustible.id))
    params_trama.append(str(gas_form.punto_control.name))
    params_trama.append(str(gas_form.punto_control.descripcion))
    params_trama.append(str(gas_form.clasificacion_control.id))
    params_trama.append(str(gas_form.responsable_control.id))
    params_trama.append("IDM" + str(gas_form.id+9000))
    params_trama.append("1")
    params_trama.append(str(gas_form.fecha_muestra.strftime('%d-%m-%Y')))
    resultado_odorizacion = 1 if gas_form.resultado_odorizacion else 0
    params_trama.append(str(resultado_odorizacion))
    resultado_impurezas = 1 if gas_form.resultado_impurezas else 0
    params_trama.append(str(resultado_impurezas))
    params_trama.append(str(gas_form.poder_calorifico_superior))
    params_trama.append(str(gas_form.poder_calorifico_inferior))
    params_trama.append(str(gas_form.indice_wobbe))
    params_trama.append(str(gas_form.densidad_relativa))
    params_trama.append(str(gas_form.gases_inertes_pmol))
    params_trama.append(str(gas_form.punto_rocio_hydrocarburos))
    params_trama.append(str(gas_form.dioxido_de_carbono))
    params_trama.append(str(gas_form.dioxido_de_carbono_pmol))
    params_trama.append(str(gas_form.oxigeno_pvv))
    params_trama.append(str(gas_form.oxigeno_pmol))
    params_trama.append(str(gas_form.suluro_hidrogeno))
    params_trama.append(str(gas_form.azufre_antes_odorizar))
    params_trama.append(str(gas_form.azufre_despues_odorizar))
    params_trama.append(str(gas_form.agua))
    params_trama.append(str(gas_form.metano))
    params_trama.append(str(gas_form.etano))
    params_trama.append(str(gas_form.propano))
    params_trama.append(str(gas_form.butano))
    params_trama.append(str(gas_form.pentano))
    params_trama.append(str(gas_form.hexano))
    params_trama.append(str(gas_form.nitrogeno))
    params_trama.append(str(gas_form.propano_e_hidrocarburos_superiores))
    params_trama.append(str(gas_form.hexano_hydrocarburos))
    params_trama.append(str(gas_form.hidrogeno))
    params_trama.append(str(gas_form.monoxido_carobono))

    response = trama_sec.join(params_trama).replace('None', '')

    return jsonify({"Trama_SEC": response})


@app.route("/download/<int:id_formulario_gas>/csv", methods=['GET'])
def download_file(id_formulario_gas):
    gas_form = GasForm.query.filter_by(id=id_formulario_gas).first_or_404()
    if request.method == 'GET':

        params_trama = []
        trama_sec = ";"
        params_trama.append("121")  # parametro por defecto, ID Empresa
        params_trama.append(str(gas_form.punto_control.region.name))
        params_trama.append(str(gas_form.punto_control.tramo.id))
        params_trama.append(str(gas_form.punto_control.tipo_red.id))
        params_trama.append(str(gas_form.tipo_combustible.id))
        params_trama.append(str(gas_form.punto_control.name))
        params_trama.append(str(gas_form.punto_control.descripcion))
        params_trama.append(str(gas_form.clasificacion_control.id))
        params_trama.append(str(gas_form.responsable_control.id))
        params_trama.append("IDM" + str(gas_form.id + 9000))
        params_trama.append("1")
        params_trama.append(str(gas_form.fecha_muestra.strftime('%d-%m-%Y')))
        resultado_odorizacion = 1 if gas_form.resultado_odorizacion else 0
        params_trama.append(str(resultado_odorizacion))
        resultado_impurezas = 1 if gas_form.resultado_impurezas else 0
        params_trama.append(str(resultado_impurezas))
        params_trama.append(str(gas_form.poder_calorifico_superior))
        params_trama.append(str(gas_form.poder_calorifico_inferior))
        params_trama.append(str(gas_form.indice_wobbe))
        params_trama.append(str(gas_form.densidad_relativa))
        params_trama.append(str(gas_form.gases_inertes_pmol))
        params_trama.append(str(gas_form.punto_rocio_hydrocarburos))
        params_trama.append(str(gas_form.dioxido_de_carbono))
        params_trama.append(str(gas_form.dioxido_de_carbono_pmol))
        params_trama.append(str(gas_form.oxigeno_pvv))
        params_trama.append(str(gas_form.oxigeno_pmol))
        params_trama.append(str(gas_form.suluro_hidrogeno))
        params_trama.append(str(gas_form.azufre_antes_odorizar))
        params_trama.append(str(gas_form.azufre_despues_odorizar))
        params_trama.append(str(gas_form.agua))
        params_trama.append(str(gas_form.metano))
        params_trama.append(str(gas_form.etano))
        params_trama.append(str(gas_form.propano))
        params_trama.append(str(gas_form.butano))
        params_trama.append(str(gas_form.pentano))
        params_trama.append(str(gas_form.hexano))
        params_trama.append(str(gas_form.nitrogeno))
        params_trama.append(str(gas_form.propano_e_hidrocarburos_superiores))
        params_trama.append(str(gas_form.hexano_hydrocarburos))
        params_trama.append(str(gas_form.hidrogeno))
        params_trama.append(str(gas_form.monoxido_carobono))

        return excel.make_response_from_array([
            ["Nombre del Punto Control", "Codigo Sec"],
            [str(gas_form.punto_control.name), trama_sec.join(params_trama)]
        ],
            "csv", file_name=u"codigo_sec")


@app.route('/test_api/<mensaje>')
def test_api(mensaje):
    print(mensaje)
    return "OK"


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Revise su cuenta de correo para cambiar su password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


@app.route('/informes/informesdiarios', methods=['GET', 'POST'])
@login_required
def informes_diarios():
    form = InformesDiariosForm()
    form.punto_control.choices = [(str(p.id), p.descripcion) for p in PuntoControl.query.order_by('name')]

    if request.method == 'POST':
        if form.validate_on_submit():

            resp = [['Nombre Punto Control', 'Valor', 'Fecha', 'Elemento']]
            for punto_control_id in form.punto_control.data:
                row = []
                punto_control = PuntoControl.query.filter_by(id=punto_control_id).first()
                fecha_muestra = datetime.strptime(str(form.fecha_muestra.data), "%Y-%m-%d")
                row.append(punto_control.name)
                gasform = GasForm.query.filter_by(fecha_muestra=fecha_muestra, punto_control_id=punto_control_id).first()
                if gasform:
                    row.append(getattr(gasform, form.elemento.data))
                else:
                    row.append('')
                resp.append(row)
                row.append(str(fecha_muestra.strftime('%d-%m-%Y')))
                row.append(form.elemento.data)
            print(resp)
            return excel.make_response_from_array(resp,"csv", file_name=u"informe_diario")
        return render_template('informes/informesdiarios.html', form=form)
    return render_template('informes/informesdiarios.html', form=form)

