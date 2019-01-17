from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login, app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        return role == self.rol.name

    def get_rol(self):
        return self.rol

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    rol_email = db.Column(db.String(80))
    usuarios = db.relationship('User', backref='rol', lazy='dynamic')

    def __repr__(self):
        return '<Rol {}>'.format(self.name)


@login.user_loader
def load_user(idz):
    return User.query.get(int(idz))


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    puntos_control = db.relationship('PuntoControl', backref='region', lazy='dynamic')

    def __repr__(self):
        return '<Region {}>'.format(self.name)


class Tramo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    puntos_control = db.relationship('PuntoControl', backref='tramo', lazy='dynamic')

    def __repr__(self):
        return '<Tramo {}>'.format(self.name)


class TipoRed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    puntos_control = db.relationship('PuntoControl', backref='tipo_red', lazy='dynamic')


class PuntoControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    descripcion = db.Column(db.Text())
    tipo_red_id = db.Column(db.Integer, db.ForeignKey('tipo_red.id'), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    tramo_id = db.Column(db.Integer, db.ForeignKey('tramo.id'), nullable=False)
    reportes = db.relationship('GasForm', backref='punto_control', lazy='dynamic')

    def __repr__(self):
        return '<TipoControl {}>'.format(self.name)


class TipoCombustible(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    reportes = db.relationship('GasForm', backref='tipo_combustible', lazy='dynamic')

    def __repr__(self):
        return '<TipoCombustible {}>'.format(self.name)


class ClasificacionControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    reportes = db.relationship('GasForm', backref='clasificacion_control', lazy='dynamic')

    def __repr__(self):
        return '<ClasificacionControl {}>'.format(self.name)


class ResponsableControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    reportes = db.relationship('GasForm', backref='responsable_control', lazy='dynamic')

    def __repr__(self):
        return '<ResponsableControl {}>'.format(self.name)


class Laboratorista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    reportes = db.relationship('GasForm', backref='laboratorista', lazy='dynamic')

    def __repr__(self):
        return '<Laboratorista {}>'.format(self.name)


class GasForm(db.Model):
    tipo_combustible_id = db.Column(db.Integer, db.ForeignKey('tipo_combustible.id'))
    punto_control_id = db.Column(db.Integer, db.ForeignKey('punto_control.id'))
    clasificacion_control_id = db.Column(db.Integer, db.ForeignKey('clasificacion_control.id'))
    responsable_control_id = db.Column(db.Integer, db.ForeignKey('responsable_control.id'))
    laboratorista_id = db.Column(db.Integer, db.ForeignKey('laboratorista.id'))

    id = db.Column(db.Integer, primary_key=True)
    fecha_muestra = db.Column(db.DateTime)
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)
    resultado_odorizacion = db.Column(db.Boolean)
    resultado_impurezas = db.Column(db.Boolean)
    poder_calorifico_superior = db.Column(db.Numeric(precision=5))
    poder_calorifico_inferior = db.Column(db.Numeric(precision=5))
    indice_wobbe = db.Column(db.Numeric(precision=5))
    densidad_relativa = db.Column(db.Numeric(precision=5))
    gases_inertes_pmol = db.Column(db.Numeric(precision=5))
    punto_rocio_hydrocarburos = db.Column(db.Numeric(precision=5))
    dioxido_de_carbono = db.Column(db.Numeric(precision=5))
    dioxido_de_carbono_pmol = db.Column(db.Numeric(precision=5))
    oxigeno_pvv = db.Column(db.Numeric(precision=5))
    oxigeno_pmol = db.Column(db.Numeric(precision=5))
    suluro_hidrogeno = db.Column(db.Numeric(precision=5))
    azufre_antes_odorizar = db.Column(db.Numeric(precision=5))
    azufre_despues_odorizar = db.Column(db.Numeric(precision=5))

    agua = db.Column(db.Numeric(precision=5))
    metano = db.Column(db.Numeric(precision=5))
    etano = db.Column(db.Numeric(precision=5))
    propano = db.Column(db.Numeric(precision=5))
    butano = db.Column(db.Numeric(precision=5))
    pentano = db.Column(db.Numeric(precision=5))
    hexano = db.Column(db.Numeric(precision=5))
    nitrogeno = db.Column(db.Numeric(precision=5))
    propano_e_hidrocarburos_superiores = db.Column(db.Numeric(precision=5))
    hexano_hydrocarburos = db.Column(db.Numeric(precision=5))
    hidrogeno = db.Column(db.Numeric(precision=5))
    monoxido_carobono = db.Column(db.Numeric(precision=5))
    porcentaje_vol_gas = db.Column(db.Numeric(precision=5))

    def __repr__(self):
        return '<GasForm id:{}>'.format(self.id)

    @property
    def return_quick_info(self):
        return (
            self.id,
            self.laboratorista.name,
            self.punto_control.name,
            self.fecha_muestra.strftime('%d-%m-%Y')
        )

    @property
    def return_select_value(self):
        return str(str(self.id) + " : " + self.fecha_año.strftime('%d-%m-%Y'))

