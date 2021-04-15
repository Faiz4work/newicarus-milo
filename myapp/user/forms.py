from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, InputRequired

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])