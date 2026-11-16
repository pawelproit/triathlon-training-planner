from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from ..extensions import db
from ..models import User


class RegisterForm(FlaskForm):
    username = StringField(
        "Nazwa użytkownika",
        validators=[DataRequired(message="Podaj nazwę użytkownika."), Length(3, 40)],
    )
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Podaj adres e-mail."),
            Email(message="Nieprawidłowy adres e-mail."),
            Length(max=120),
        ],
    )
    password = PasswordField(
        "Hasło",
        validators=[
            DataRequired(message="Podaj hasło."),
            Length(min=8, message="Hasło musi mieć min. 8 znaków."),
        ],
    )
    password2 = PasswordField(
        "Powtórz hasło",
        validators=[DataRequired(), EqualTo("password", message="Hasła muszą być takie same.")],
    )
    submit = SubmitField("Zarejestruj się")

    def validate_username(self, field):
        exists = db.session.scalar(
            db.select(User).where(User.username == field.data.strip())
        )
        if exists:
            raise ValidationError("Ta nazwa użytkownika jest już zajęta.")

    def validate_email(self, field):
        exists = db.session.scalar(
            db.select(User).where(User.email == field.data.strip().lower())
        )
        if exists:
            raise ValidationError("Ten adres e-mail jest już zarejestrowany.")


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Hasło", validators=[DataRequired()])
    remember = BooleanField("Zapamiętaj mnie")
    submit = SubmitField("Zaloguj się")