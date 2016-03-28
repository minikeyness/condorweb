from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):

    username = StringField('uname', validators=[DataRequired()])
    password = PasswordField('pwd', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
