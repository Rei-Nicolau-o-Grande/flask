from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidade.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={
                               "placeholder": "Username",
                               "class": "form-control"
                           })

    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=50), Email()],
                        render_kw={
                            'placeholder': 'Email',
                            'class': 'form-control'
                        })

    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)],
                          render_kw={
                                'placeholder': 'Senha',
                                'class': 'form-control'
                          })
    confirmar_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')],
                                    render_kw={
                                        'placeholder': 'Confirmação de Senha',
                                        'class': 'form-control'
                                    })
    submit_criar_conta = SubmitField('Criar Conta',
                                     render_kw={
                                            'class': 'btn btn-success mt-3 mb-3',
                                     })

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Username já existe. Escolha outro.')

    def validate_email(self, email):
        email = Usuario.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email já existe. Escolha outro.')


class FormLogin(FlaskForm):

    email_login = StringField('Email', validators=[ Length(min=5, max=50), Email()],
                        render_kw={
                            "placeholder": "Email",
                            "class": "form-control",
                        })

    senha_login = PasswordField('Senha', validators=[ Length(min=6, max=20)],
                                render_kw={
                                    "placeholder": "Senha",
                                    "class": "form-control",
                                })

    lembrar = BooleanField('Lembrar',
                           render_kw={
                                 "class": "form-check-input",
                           })

    submit_login = SubmitField('Login',
                               render_kw={
                                    "class": "btn btn-primary mt-3 mb-3",
                               })


class FormEditarPerfil(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={
                               "placeholder": "Username",
                               "class": "form-control"
                           })

    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=50), Email()],
                        render_kw={
                            'placeholder': 'Email',
                            'class': 'form-control'
                        })

    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])],
                            render_kw={
                                'class': 'form-control'
                            })

    curso_python = BooleanField('Curso Python',
                                render_kw={
                                    'class': 'form-check-input'
                                })

    curso_c = BooleanField('Curso C',
                           render_kw={
                               'class': 'form-check-input'
                           })

    curso_java = BooleanField('Curso Java',
                                render_kw={
                                    'class': 'form-check-input'
                                })

    curso_javascript = BooleanField('Curso Javascript',
                                render_kw={
                                    'class': 'form-check-input'
                                })

    curso_sql = BooleanField('Curso SQL',
                             render_kw={
                                 'class': 'form-check-input'
                             })

    submit_editar_perfil = SubmitField('Editar Perfil',
                                     render_kw={
                                         'class': 'btn btn-success mt-3 mb-3',
                                     })

    def validate_username(self, username):
        if username.data != current_user.username:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError('Username já existe. Escolha outro.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = Usuario.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email já existe. Escolha outro.')

class FormCriarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=2, max=140)])
    corpo = TextAreaField('Corpo', validators=[DataRequired()])
    submit_criar_post = SubmitField('Criar Post')