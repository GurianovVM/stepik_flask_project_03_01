from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, InputRequired, Length


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', [InputRequired(message='Введите ваше Имя'),
                                    Length(min=2, message='Слишком короткое имя')])
    address = StringField('Адрес', [InputRequired(message='Введите ваш адресс'),
                                    Length(min=3, message='Слишком короткий адресс')])
    email = StringField('Электропочта', [Email(message='Введите ваш email')])
    phone = StringField('Телефон', [InputRequired(message='Введите телефон'),
                                    Length(min=4, max=15, message='Длина от 4 до 15')])
    submit = SubmitField('Оформить заказ')


class LoginForm(FlaskForm):
    email = StringField('Электропочта', [Email(message='Введите ваш email')])
    password = StringField('Пароль', [InputRequired(message='Введите пароль')])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('Электропочта', [Email(message='Введите ваш email')])
    password = StringField('Пароль', [InputRequired(message='Введите пароль'),
                                      Length(min=6, message='Минимальная длина пароля 6 символов')])
    submit = SubmitField('Войти')
