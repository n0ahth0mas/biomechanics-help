from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.fields.html5 import EmailField
from wtforms import validators


# Set your classes here.


class RegisterForm(FlaskForm):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
         EqualTo('password', message='Passwords must match')]
    )

class LoginForm(FlaskForm):
    email = EmailField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(FlaskForm):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

class StudentLoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class StudentRegForm(FlaskForm):
    fullName = StringField('Full name', validators=[DataRequired()])
    email = EmailField('Your email', validators=[DataRequired()])
    password = PasswordField('Your password', validators=[DataRequired()])
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
         EqualTo('password', message='Passwords must match')]
    )

class ProfessorRegForm(FlaskForm):
    fullName = StringField('Full name', validators=[DataRequired()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
         EqualTo('password', message='Passwords must match')]
    )

class AddClass(FlaskForm):
    class_code = StringField('Class Code', validators=[DataRequired()])

class CreateClass(FlaskForm):
    class_name = StringField('Class Name', validators=[DataRequired()])
    class_id = StringField('Class code (think password)', validators=[DataRequired()])