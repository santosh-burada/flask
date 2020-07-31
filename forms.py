from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from email_validator import validate_email, EmailNotValidError


class RegForm(FlaskForm):
    Username = StringField('username', validators=[DataRequired(), Length(min=3, max=20)])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Conform_pwd = PasswordField('Conform Password', validators=[DataRequired(), EqualTo('Password')])
    Submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Remember = BooleanField('Remember Me')
    Submit = SubmitField('Sign up')
