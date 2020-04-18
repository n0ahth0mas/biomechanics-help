from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, IntegerField, FileField, BooleanField, SubmitField, SelectField, HiddenField
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
    orderNo2 = IntegerField('Chapter Number', validators=[DataRequired()])
    chapterName = StringField('Chapter Name', validators=[DataRequired()])


class CreateSection(FlaskForm):
    orderNo2 = IntegerField('Section Number')
    sectionName = StringField('Section Name', validators=[DataRequired()])


class CreateSectionBlock(FlaskForm):
    orderNo2 = IntegerField('Text Number', validators=[DataRequired()])
    sectionText = StringField('Section Text', validators=[DataRequired()])


class CreateQuestion(FlaskForm):
    question_type_choices = [('short', 'Short Answer'), ('multiple', 'Multiple Choice'), ('dragndrop', 'Drag and Drop')]
    orderNo3 = IntegerField('Question Number', validators=[DataRequired()])
    questionText = StringField('Question Text', validators=[DataRequired()])
    questionType = SelectField('Question Type', validators=[DataRequired()], choices=question_type_choices)
    imageFile = FileField('Image')


class CreateImage(FlaskForm):
    imageFile = FileField('Image File', validators=[DataRequired()])


class CreateVideo(FlaskForm):
    videoFile = FileField('Video File', validators=[DataRequired()])


class CreateAnswer(FlaskForm):
    correctness_choices = [('0', 'False'), ('1', 'True')]
    correctness = SelectField(validators=[DataRequired()], choices=correctness_choices)
    answerText = StringField('Answer Text', validators=[DataRequired()])
    answerReason = StringField('Answer Reason', validators=[DataRequired()])
    imageFile = FileField('Image File', validators=[DataRequired()])


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


class CreateSectionBlockImages(FlaskForm):
    xposition_choices = [('right', 'right'), ('left', 'left')]
    yposition_choices = [('above', 'above'), ('below', 'below')]
    orderNo4 = IntegerField('Text Number', validators=[DataRequired()])
    imageFile = FileField('Image File', validators=[DataRequired()])
    xposition = SelectField('X Position', choices=xposition_choices)
    yposition = SelectField('Y position', choices=yposition_choices)


class CreateGlossaryImage(FlaskForm):
    termID = HiddenField('Term ID', validators=[DataRequired()])
    imageFile = FileField('Image File', validators=[DataRequired()])


class EditClass(FlaskForm):
    classID = HiddenField()
    className = StringField(validators=[DataRequired()])
    newClassID = StringField(validators=[DataRequired()])


class EditChapter(FlaskForm):
    chapterID = HiddenField()
    orderNo1 = StringField('Chapter Number', validators=[DataRequired()])
    chapterName = StringField('Chapter Name', validators=[DataRequired()])


class EditTerm(FlaskForm):
    termID = HiddenField(validators=[DataRequired()])
    term_e = StringField('Term', validators=[DataRequired()])
    definition = StringField("Definition", validators=[DataRequired()])


class EditSection(FlaskForm):
    sectionID = HiddenField(validators=[DataRequired()])
    orderNo1 = IntegerField('Section Number', validators=[DataRequired()])
    sectionName = StringField('Section Name', validators=[DataRequired()])


class EditSectionBlock(FlaskForm):
    sectionBlockID = HiddenField(validators=[DataRequired()])
    orderNo1 = IntegerField('Section Number', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])


class EditQuestion(FlaskForm):
    question_type_choices = [('short', 'Short Answer'), ('multiple', 'Multiple Choice'), ('dragndrop', 'Drag and Drop')]
    questionID = HiddenField(validators=[DataRequired()])
    orderNo5 = IntegerField('Section Number', validators=[DataRequired()])
    questionText = StringField(validators=[DataRequired()])
    questionType = SelectField(validators=[DataRequired()], choices=question_type_choices)


class EditAnswer(FlaskForm):
    question_type_choices = [('0', 'False'), ('1', 'True')]
    answerID = HiddenField()
    correctness = SelectField(validators=[DataRequired()], choices=question_type_choices)
    answerText2 = StringField('Answer Text', validators=[DataRequired()])
    answerReason = StringField('Answer Reason', validators=[DataRequired()])


class ChangeImage(FlaskForm):
    questionID = HiddenField()
    imageFile1 = FileField(validators=[DataRequired()])


