from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, IntegerField, FileField, BooleanField, SubmitField, SelectField
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
    schoolProfCode = StringField('Your Schools Professor Code', validators=[DataRequired()])
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


class CreateChapter(FlaskForm):
    orderNo = StringField('Chapter Number')
    chapterName = StringField('Chapter Name', validators=[DataRequired()])


class CreateSection(FlaskForm):
    orderNo = StringField('Section Number')
    sectionName = StringField('Section Name', validators=[DataRequired()])


class CreateSectionBlock(FlaskForm):
    orderNo = StringField('Text Number')
    sectionText = StringField('Section Text', validators=[DataRequired()])


class CreateQuestion(FlaskForm):
    orderNo = StringField('Question Number')
    questionText = StringField('Question Text', validators=[DataRequired()])
    questionType = StringField('Question Type', validators=[DataRequired()])
    imageFile = FileField('Image')


class CreateImage(FlaskForm):
    imageFile = FileField('Image File', validators=[DataRequired()])


class CreateVideo(FlaskForm):
    videoFile = FileField('Video File', validators=[DataRequired()])


class CreateAnswer(FlaskForm):
    correctness = BooleanField()
    answerText = StringField('Answer Text', validators=[DataRequired()])
    answerReason = StringField('Answer Reason', validators=[DataRequired()])


class CreateTerm(FlaskForm):
    term = StringField('Term', validators=[DataRequired()])
    definition = StringField("Definition", validators=[DataRequired()])


class ForgotForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class CreateSectionImages(FlaskForm):
    xposition_choices = [('',''), ('right', 'right'), ('left', 'left')]
    yposition_choices = [('',''), ('above', 'above'), ('below', 'below')]
    sectionBlockID = StringField('Section Block ID', validators=[DataRequired()])
    imageFile = FileField('Image File', validators=[DataRequired()])
    xposition = SelectField('X Position', validators=[DataRequired()], choices=xposition_choices)
    yposition = SelectField('Y position', validators=[DataRequired()], choices=yposition_choices)
