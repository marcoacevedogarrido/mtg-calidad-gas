from flask_wtf import FlaskForm
from sqlalchemy import Text
import decimal
from wtforms import SubmitField, SelectField, DateField, IntegerField, StringField, \
    SelectMultipleField, PasswordField, BooleanField, FloatField, DecimalField
from wtforms.validators import DataRequired, NumberRange, length, EqualTo, Email, ValidationError, InputRequired, Optional
from app.models import User, Laboratorista



class MainForm(FlaskForm):
    tipo_combustible = SelectField('Tipo de Combustible', choices=[('1', 'Mezcla GN/BM'),
                                                                   ('2', 'Aire Metanado'),
                                                                   ('3', 'Aire Propanado'),
                                                                   ('4', 'Biometano'),
                                                                   ('5', 'Gas de Ciudad'),
                                                                   ('6', 'Gas Natural')])

    punto_control = SelectField('Punto de control')

    clasificacion_control = SelectField('Clasificacion Control', choices=[('1', 'Analisis Laboratorio'),
                                                                          ('2', 'Cromatografia'),
                                                                          ('3', 'Cromatografia y Otros'),
                                                                          ('4', 'Punto de Control de Red'),
                                                                          ('5', 'Punto de Odorizacion en Red')])

    responsable_control = SelectField('Responsable Control', choices=[('1', 'Propio'),
                                                                      ('2', 'Proovedor'),
                                                                      ('3', 'Transportista')])

    laboratorista = SelectField('Laboratorista')

    fecha_muestra = DateField('Fecha de muestra', format='%m/%d/%Y', validators=[DataRequired()])

    resultado_odorizacion = BooleanField('Cumple Resultado odorizacion?')

    resultado_impurezas = BooleanField('Cumple Resultado impurezas?')

    poder_calorifico_superior = DecimalField('Poder calorifico superior', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    poder_calorifico_inferior = DecimalField('Poder calorifico inferior', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    indice_wobbe = DecimalField('Indice Wobbe', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    densidad_relativa = DecimalField('Densidad Relativa', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    gases_inertes_pmol = DecimalField('Gases Inertes Pmol', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    punto_rocio_hydrocarburos = DecimalField('Punto Rocio Hidrocarburos', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    dioxido_de_carbono = DecimalField('Dioxido de Carbono pvv', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    dioxido_de_carobono_pmol = DecimalField('Dioxido de Carbono pmol', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    oxigeno_pvv = DecimalField('Oxigeno pvv', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    oxigeno_pmol = DecimalField('Oxigeno Pmol', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    suluro_hidrogeno = DecimalField('Sulfuro Hidrogeno', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    azufre_antes_odorizar = DecimalField('Azufre antes Odorizar', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    azufre_despues_odorizar = DecimalField('Azufre despues Odorizar', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])

    agua = DecimalField('Agua', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    metano = DecimalField('Metano', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    etano = DecimalField('Etano', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    propano = DecimalField('Propano', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    butano = DecimalField('Butano', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    pentano = DecimalField('Pentano', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    hexano = DecimalField('Hexano', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    nitrogeno = DecimalField('Nitrogeno', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    propano_e_hidrocarburos_superiores = DecimalField('Propano e Hidrocarburos superiores', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    hexano_hydrocarburos = DecimalField('Hexano e hidrocarburos', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    hidrogeno = DecimalField('Hidrogeno', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    monoxido_carbono = DecimalField('Monoxido Carbono', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])
    porcentaje_vol_gas = DecimalField('% vol gas en el aire (Odorizacion)', places=5, rounding=decimal.ROUND_DOWN, validators=[Optional()])

    submit = SubmitField('Generar Reporte')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Entrar')


class LaboratoristaForm(FlaskForm):
    name = StringField('Nuevo Laboratista:', validators=[DataRequired(), length(min=5, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')

    @staticmethod
    def validate_email(self, email):
        laboratorista = Laboratorista.query.filter_by(email=email.data).first()
        if laboratorista is not None:
            raise ValidationError('Email ya Registrado.')


class PcontrolForm(FlaskForm):
    name = StringField('Nombre:', validators=[DataRequired(), length(min=0, max=20)])
    region_id = SelectField('Region:')
    tipo_de_red_id = SelectField('Tipo de Red:')
    tramo_id = SelectField('Tramo:')
    descripcion = StringField('Descripcion:')
    submit = SubmitField('Registrar')


class TipoRedForm(FlaskForm):
    name = StringField('Nombre:', validators=[DataRequired(), length(min=0, max=30)])
    submit = SubmitField('Registrar')


class ResponsableControlForm(FlaskForm):
    name = StringField('Responsable de Control: ', validators=[DataRequired(), length(min=0, max=30)])
    submit = SubmitField('Registrar')


class TramoForm(FlaskForm):
    name = StringField('Tramo:', validators=[DataRequired(), length(min=0, max=30)])
    submit = SubmitField('Registrar')


class RegionForm(FlaskForm):
    name = StringField('Region:', validators=[DataRequired(), length(min=0, max=30)])
    submit = SubmitField('Registrar')


class BaseUserForm(FlaskForm):
    username = StringField('Nuevo Usuario:', validators=[DataRequired(), length(min=5, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Nueva Contraseña:',
                             validators=[EqualTo('password2', message="contraseñas deben coincidir!")])
    password2 = PasswordField('Repetir Contraseña:')
    rol = SelectField('Seleccione rol:')

    submit = SubmitField('Registrar')


class UsuarioForm(BaseUserForm):
    password = PasswordField('Nueva Contraseña:',
                             validators=[InputRequired(), EqualTo('password2', message="contraseñas deben coincidir!")])
    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email ya Registrado.')

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Usuario ya Registrado.')


class ValidadorForm(FlaskForm):
    poder_calorifico_superior = FloatField('Poder Calorifico Superior - max')
    min_poder_calorifico_superior = FloatField('Poder Calorifico Superior - min')

    indice_wobbe = FloatField('Indice Wobbe max')
    min_indice_wobbe = FloatField('Indice Wobbe min')

    gases_inertes_pmol = FloatField('Gases inertes pmol')
    punto_rocio_hydrocarburos = FloatField('Punto rocio hidrocarburos')
    dioxido_de_carbono = FloatField('dioxido de carbono')
    oxigeno_pvv = FloatField('oxigeno pvv')
    suluro_hidrogeno = FloatField('sulfuro hidrogeno')
    azufre_antes_odorizar = FloatField('azufre antes de odorizar')
    azufre_despues_odorizar = FloatField('azufre despuese de odorizar')
    agua = FloatField('agua')

    # bio_min_indice_wobble = FloatField('Indice Wobbe, min', validators=[DataRequired()])
    # bio_min_metano = FloatField('Metano, min', validators=[DataRequired()])
    # bio_min_gases_inertes_pmol = FloatField('Gases inertes pmol, min', validators=[DataRequired()])
    # bio_min_punto_rocio_hydrocarburos = FloatField('Punto rocio hidrocarburos, min', validators=[DataRequired()])
    # bio_min_poder_calorifico_superior = FloatField('poder calorifico superior, min', validators=[DataRequired()])
    #
    # bio_azufre_antes_odorizar = FloatField('azufre antes de odorizar', validators=[DataRequired()])
    # bio_hidrogeno = FloatField('Hidrogeno', validators=[DataRequired()])
    # bio_hexano_hydrocarburos = FloatField('Gases inertes pmol', validators=[DataRequired()])
    # bio_poder_calorifico_superior = FloatField('Gases inertes pmol', validators=[DataRequired()])
    # bio_punto_rocio_hydrocarburos = FloatField('Gases inertes pmol', validators=[DataRequired()])
    # bio_propano_e_hidrocarburos_superiores = FloatField('Gases inertes pmol', validators=[DataRequired()])
    # bio_etano = FloatField('Gases inertes pmol', validators=[DataRequired()])
    # bio_azufre_despues_odorizar = FloatField('Gases inertes pmol', validators=[DataRequired()])
    # bio_oxigeno_pvv = FloatField('Gases inertes pmol', validators=[DataRequired()])
    # bio_gases_inertes_pmol = FloatField('Gases inertes pmol', validators=[DataRequired()])
    # bio_indice_wobbe = FloatField('Gases inertes pmol', validators=[DataRequired()])
    # bio_monoxido_carbono = FloatField('Gases inertes pmol', validators=[DataRequired()])

    submit = SubmitField('actualizar valores')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(), length(min=0, max=64)])
    submit = SubmitField('Enviar')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField('Repetir password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cambiar Password')

class SecForm(FlaskForm):
    fecha_inicio = DateField('Desde: ', format='%m/%d/%Y', validators=[DataRequired()])
    fecha_fin = DateField('Hasta: ', format='%m/%d/%Y', validators=[DataRequired()])
    submit = SubmitField('Buscar Codigo Sec')


class ReportesForm(FlaskForm):
    fecha_inicio = DateField('Desde: ', format='%m/%d/%Y', validators=[DataRequired()])
    fecha_fin = DateField('Hasta: ', format='%m/%d/%Y', validators=[DataRequired()])
    punto_control = SelectField('Punto de control:')
    submit = SubmitField('Buscar')


class InformesDiariosForm(FlaskForm):
    fecha_muestra = DateField('Fecha: ', format='%m/%d/%Y', validators=[DataRequired()])
    punto_control = SelectMultipleField('Punto de control: ')
    elemento = SelectField('Elemento o Compuesto: ', choices=[('agua', 'Agua'),
                                                              ('metano', 'Metano'),
                                                              ('etano', 'Etano'),
                                                              ('propano', 'Propano'),
                                                              ('butano', 'Butano'),
                                                              ('pentano', 'Pentano'),
                                                              ('hexano', 'Hexano'),
                                                              ('nitrogeno', 'Nitrogeno'),
                                                              ('propano_e_hidrocarburos_superiores', 'Propano e Hidrocarburos Superiores'),
                                                              ('hexano_hydrocarburos', 'Hexano Hydrocarburos'),
                                                              ('hidrogeno', 'Hidrogeno'),
                                                              ('monoxido_carobono', 'Monoxido Carobono'),
                                                              ('porcentaje_vol_gas', 'Porcentaje Vol Gas'),
                                                              ('poder_calorifico_superior', 'Poder Calorifico Superior'),
                                                              ('indice_wobbe', 'Indice Wobbe'),
                                                              ('densidad_relativa', 'Densidad Relativa'),
                                                              ('punto_rocio_hydrocarburos', 'Punto Rocio Hydrocarburos'),
                                                              ('dioxido_de_carbono', 'Dioxido de Carbono'),
                                                              ('dioxido_de_carbono_pmol', 'Dioxido de Carbono Pmol'),
                                                              ('oxigeno_pvv', 'Oxigeno Pvv'),
                                                              ('oxigeno_pmol', 'Oxigeno Pmol'),
                                                              ('suluro_hidrogeno', 'Sulfuro Hidrogeno'),
                                                              ('azufre_antes_odorizar', 'Azufre Antes Odorizar'),
                                                              ('azufre_despues_odorizar', 'Azufre Despues Odorizar'),
                                                              ])
    submit = SubmitField('Buscar')



