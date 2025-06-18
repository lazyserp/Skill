from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Email,EqualTo,Length


class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(),Length(min=4,max=25)])
    email = StringField('Email',validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(),EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])
    submit = SubmitField('Login')
    