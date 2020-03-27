# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask, render_template, request, flash, url_for, json, session
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import sqlite3
import hashlib
from flask import g, redirect, abort
from flask import session
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from flask_user import roles_required, UserManager, UserMixin
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask import g
import datetime

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.secret_key = 'xxxxyyyyyzzzzz'
# app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/help.db'
app.config['USER_EMAIL_SENDER_EMAIL'] = "jriley9000@gmail.com"
# login = LoginManager()
# login.init_app(app)
pathToDB = os.path.abspath("database/help.db")
db = SQLAlchemy(app)
print(pathToDB)

home_url = "http://127.0.0.1:5000/"


def get_sql_alc_db():
    with app.app_context():
        return SQLAlchemy(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(pathToDB)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#
login = LoginManager()
login.init_app(app)


class Class(db.Model):
    __tablename__ = "Classes"
    classID = db.Column(db.Integer(), primary_key=True)
    className = db.Column(db.String())


class Chapter(db.Model):
    __tablename__ = 'Chapters'
    chapterID = db.Column(db.Integer(), primary_key=True)
    chapterName = db.Column(db.String())
    classID = db.Column(db.String(), db.ForeignKey('Classes.classID'))


class Section(db.Model):
    __tablename__ = 'Sections'
    sectionID = db.Column(db.Integer(), primary_key=True)
    chapterID = db.Column(db.Integer(), db.ForeignKey('Chapters.chapterID'))
    sectionName = db.Column(db.String())


class SectionImages(db.Model):
    __tablename__ = 'SectionImages'
    sectionID = db.Column(db.Integer(), db.ForeignKey('Sections.sectionID'), primary_key=True)
    imageFile = db.Column(db.String(), primary_key=True)

    class Meta:
        unique_together = (("sectionID", "imageFile"),)


class SectionBlock(db.Model):
    __tablename__ = 'SectionBlock'
    sectionBlockID = db.Column(db.Integer(), primary_key=True)
    sectionText = db.Column(db.String())
    sectionID = db.Column(db.Integer(), db.ForeignKey('Sections.sectionID'))


class Question(db.Model):
    __tablename__ = 'Questions'
    questionID = db.Column(db.Integer(), primary_key=True)
    questionText = db.Column(db.String())
    sectionID = db.Column(db.Integer(), db.ForeignKey('Sections.sectionID'))
    questionType = db.Column(db.String())


class Answer(db.Model):
    __tablename__ = 'Answers'
    answerID = db.Column(db.Integer(), primary_key=True)
    questionID = db.Column(db.Integer(), db.ForeignKey('Questions.questionID'))
    correctness = db.Column(db.String())
    answerText = db.Column(db.String())
    answerReason = db.Column(db.String())


class Video(db.Model):
    __tablename__ = 'Videos'
    sectionID = db.Column(db.Integer(), db.ForeignKey('Sections.sectionID'), primary_key=True)
    videoFile = db.Column(db.String(), primary_key=True)

    class Meta:
        unique_together = (("sectionID", "videoFile"),)


class UserClasses(db.Model):
    __tablename__ = "Enroll"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), db.ForeignKey('Users.email'))
    classID = db.Column(db.Integer(), db.ForeignKey('Classes.classID'))


class Role(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'User_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('Users.email', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('Roles.id', ondelete='CASCADE'))


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    # User Authentication fields
    email = db.Column(db.String(255), primary_key=True)
    id = email
    email_confirmed_at = datetime.datetime.now()
    password = db.Column(db.String(255))
    roles = db.relationship('Role', secondary='User_roles')
    classes = db.relationship('Class', secondary='Enroll')
    active = True
    name = db.Column(db.String(255))

    def has_role(self, role):
        return role in self.roles

    def get_email(self):
        return self.email


user_manager = UserManager(app, get_sql_alc_db(), User)


@app.route('/')
def home():
    return render_template('pages/landing.html', homepage=True)


@app.route('/edit-class/<classID>', methods=('GET', 'POST'))
@login_required
@roles_required('Professor')
def edit_class(classID):
    form = CreateChapter()
    if form.validate_on_submit():
        one_chapter = Chapter()
        one_chapter.chapterName = form.data["chapterName"]
        one_chapter.classID = classID
        db.session.add(one_chapter)
        db.session.commit()
    elif request.method == 'POST':
        flash("Error")
    className = query_db('SELECT * from Classes where classID="%s"' % classID)[0][0]
    chapters = query_db('SELECT * from Chapters where classID="%s"' % classID)
    print(chapters)
    sections_arrays = []
    for chapter in chapters:
        sections_arrays.append(query_db('SELECT * from Sections where chapterID="%s"' % chapter[0]))

    return render_template('pages/edit-class.html', chapters=chapters, sections=sections_arrays, classID=classID,
                           className=className, form=form)

@app.route('/edit-class/<classID>/<chapterID>', methods=('GET', 'POST'))
@login_required
@roles_required('Professor')
def edit_chapter(classID,chapterID):
    form = CreateSection()
    if form.validate_on_submit():
        one_section = Section()
        one_section.chapterID = chapterID
        one_section.sectionName = form.data["sectionName"]
        db.session.add(one_section)
        db.session.commit()
    elif request.method == 'POST':
        flash("Error")
    chapterName = query_db('SELECT chapterName from Chapters where chapterID="%s"' % chapterID)[0][0]
    sections = query_db('SELECT * from Sections where chapterID="%s"' % chapterID)
    return render_template('pages/edit-chapter.html', sections=sections, chapterID=chapterID, classID=classID, chapterName=chapterName, form=form)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>', methods=('GET', 'POST'))
@login_required
@roles_required('Professor')
def edit_section(classID,chapterID,sectionID):
    form_s = CreateSectionBlock()
    if form_s.validate_on_submit():
        one_section_block = SectionBlock()
        one_section_block.sectionText = form_s.data["sectionText"]
        one_section_block.sectionID = sectionID
        db.session.add(one_section_block)
        db.session.commit()
    elif request.method == 'POST':
        flash("Error")
    form_i = CreateImage()
    if form_i.validate_on_submit():
        one_image = SectionImages()
        one_image.sectionID = sectionID
        one_image.imageFile = form_i.data["imageFile"]
        db.session.add(one_image)
        db.session.commit()
    elif request.method == 'POST':
        flash("Error")
    form_q = CreateQuestion()
    if form_q.validate_on_submit():
        one_question = Question()
        one_question.questionText = form_q.data["questionText"]
        one_question.sectionID = sectionID
        one_question.questionType = form_q.data["questionType"]
        db.session.add(one_question)
        db.session.commit()
    elif request.method == 'POST':
        flash("Error")
    form_v = CreateVideo()
    if form_v.validate_on_submit():
        one_video = Video()
        one_video.sectionID = sectionID
        one_video.videoFile = form_i.data["videoFile"]
        db.session.add(one_video)
        db.session.commit()
    elif request.method == 'POST':
        flash("Error")
    sectionName = query_db('SELECT sectionName from Sections where sectionID="%s"' % sectionID)[0][0]
    sectionBlocks = query_db('SELECT * from SectionBlock where sectionID="%s"' % sectionID)
    sectionImages = query_db('SELECT imageFile from SectionImages where sectionID="%s"' % sectionID)
    questions = query_db('SELECT * from Questions where sectionID="%s"' % sectionID)
    videos = query_db('SELECT * from Videos where sectionID="%s"' % sectionID)
    answers = []
    for question in questions:
        answers.append(query_db('SELECT * from Answers where questionID="%s"' % question[0]))
    print(answers)
    return render_template('pages/edit-section.html', sectionBlocks=sectionBlocks, classID=classID, chapterID=chapterID, sectionID=sectionID, sectionName=sectionName, sectionImages=sectionImages, questions=questions, answers=answers, videos=videos, form_s=form_s, form_q=form_q, form_i=form_i, form_v=form_v)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>/text/<sectionBlockID>', methods=('GET', 'POST'))
@login_required
@roles_required('Professor')
def edit_section_block(classID,chapterID,sectionID,sectionBlockID):
    sectionText = query_db('SELECT sectionText from Sections where sectionID="%s"' % sectionBlockID)[0][0]
    sectionBlocks = query_db('SELECT * from SectionBlock where sectionID="%s"' % sectionID)
    return render_template('pages/edit-section-block.html', sectionBlocks=sectionBlocks, classID=classID, chapterID=chapterID, sectionID=sectionID, sectionName=sectionName)

@app.route('/edit-class/<classID>/<chapterID>/<sectionID>/question/<questionID>', methods=('GET', 'POST'))
@login_required
@roles_required('Professor')
def edit_question(classID,chapterID,sectionID,questionID):
    form_a = CreateAnswer()
    if form_a.validate_on_submit():
        one_answer = Answer()
        one_answer.questionID = questionID
        one_answer.correctness = form_a.data["correctness"]
        one_answer.answerText = form_a.data["answerText"]
        one_answer.answerReason = form_a.data["answerReason"]
        db.session.add(one_answer)
        db.session.commit()
    answers = query_db('SELECT * from Answers where questionID="%s"' % questionID)
    questions = query_db('SELECT * from Questions where questionID="%s"' % questionID)

    return render_template('pages/edit-question.html', classID=classID, chapterID=chapterID, sectionID=sectionID, questions=questions, answers=answers, form_a=form_a)


@app.route('/student-home', methods=('GET', 'POST'))
@login_required
@roles_required('Student')
def student_home():
    print(request.endpoint)
    # add a class form
    form = AddClass()
    if form.validate_on_submit():
        one_class = Class.query.filter_by(classID=form.data["class_code"]).one()
        current_user.classes.append(one_class)
        db.session.commit()

    # render our classes
    classes_list = []
    print(current_user.classes)
    for _class in current_user.classes:
        # we want to use the class code to get a class name from classes
        _class = query_db('SELECT * from Classes WHERE classID="%s"' % _class.classID, one=True)
        classes_list.append(_class)
    return render_template('pages/studentHome.html', name=current_user.name, form=form, classes=classes_list)


@app.route('/section/<class_id>/<chapter>/<section>', methods=['GET'])
@login_required
def section_page(class_id, chapter, section):
    if query_db('SELECT * from Enroll where email="%s" AND classID="%s"' % (session["email"], class_id)) != []:
        # get info data
        info_data = "testing"

        # get info image
        info_image = "/static/img/40.png"

        # get video file
        video = "/static/video/samplevid.mp4"
        # get quiz data
        a_list = []

        # creating a list of questions for the page
        q_list = query_db('SELECT * from Questions where sectionID="%s"' % section)

        # finding all the answers of the questions on the page
        q_image_list = []

        for questions in q_list:
            answer_id = questions[0]
            try:
                this_image = query_db('SELECT * from QuestionImages where questionID="%s"' % questions[0])[0][1]
                q_image_list.append(this_image)
            except IndexError:
                print("An index error occured")
            a_list.append(query_db('SELECT * from Answers where questionID = "{}"'.format(answer_id)))

        # q_image_list = query_db('SELECT * from QuestionImages')

        return render_template('layouts/section.html', chapter=chapter, section=section, q_list=q_list,
                               a_list=a_list, classID=class_id, q_images=q_image_list, info_data=info_data,
                               info_image=info_image, video=video)
    else:
        flash("Please enroll in a class before navigating to it.")
        return redirect(home_url)


@app.route('/student-quiz/<class_id>/<chapter>/<section>', methods=['GET'])
@login_required
def student_quiz(class_id, chapter, section):
    print("called student quiz")
    if query_db('SELECT * from Enroll where email="%s" AND classID="%s"' % (session["email"], class_id)) != []:
        a_list = []
        print(a_list)
        # creating a list of questions for the page
        q_list = query_db('SELECT * from Questions where sectionID="%s"' % section)
        # q_list2 = json.dumps(q_list)
        print(q_list)
        # finding all the answers of the questions on the page
        q_image_list = []
        for questions in q_list:
            answer_id = questions[0]
            try:
                this_image = query_db('SELECT * from QuestionImages where questionID="%s"' % questions[0])[0][1]
                q_image_list.append(this_image)
            except IndexError:
                print("An index error occured")

            print(answer_id)
            print("{}".format(answer_id))
            a_list.append(query_db('SELECT * from Answers where questionID = "{}"'.format(answer_id)))
        # a_list2 = json.dumps(a_list)

        # q_image_list = query_db('SELECT * from QuestionImages')
        print(q_image_list)
        # print(a_list)
        return render_template('layouts/studentquiz.html', chapter=chapter, section=section, q_list=q_list,
                               a_list=a_list, classID=class_id, q_images=q_image_list)
    else:
        flash("Please enroll in a class before navigating to it.")
        return redirect(home_url)


@app.route('/professor-home', methods=('GET', 'POST'))
@login_required
@roles_required('Professor')
def professor_home():
    form = CreateClass()
    if form.validate_on_submit() and query_db('SELECT * from Classes where classID="%s"' % form.data["class_id"]) == []:
        one_class = Class()
        one_class.classID = form.data["class_id"]
        one_class.className = form.data["class_name"]
        current_user.classes.append(one_class)
        db.session.add(one_class)
        db.session.commit()
    elif request.method == 'POST':
        print("thinks this is a post method!")
        flash("We're sorry but a class already exists with that code, please enter another unique code")
    # render our classes
    classes_list = []
    for _class in current_user.classes:
        # we want to use the class code to get a class name from classes
        _class = query_db('SELECT * from Classes WHERE classID="%s"' % _class.classID, one=True)
        class_tuple = (_class[0], _class[1], query_db('SELECT * from Enroll WHERE classID="%s"' % _class[1]))
        classes_list.append(class_tuple)
    print(classes_list)
    return render_template('layouts/professor-home.html', name=current_user.name, classes=classes_list, form=form)


@app.route('/student-short')
@login_required
def student_short():
    return render_template('pages/placeholder.student.short.html')


@app.route('/info-slide/<sectionID>')
@login_required
def infoSlide(sectionID):
    # slide_text = query_db('SELECT * from InfoSlide WHERE sectionID = "{}"').format(sectionID)
    # slide_images = query_db('SELECT * from InfoSlideImages WHERE sectionID = "{}"').format(sectionID)
    slide_content = []
    slide_text = [("123", "Hello World!", "456"), ("125", "Goodnight", "888")]
    # slide_images = [("123", "Pretty Picture", "456")]

    # For every object queried, if they have the same sectionID, add it to a list of tuples
    # that contains all information for the text and images that go on the same slide
    # does not account for duplicatates in multiple images going to one text and vis versa
    for x in slide_text:
        for y in slide_images:
            if x[0] == y[0]:
                slide_content.append((x, y))

    return render_template('layouts/infoSlide.html', slide_content=slide_content, sectionID=sectionID)


@app.route('/glossary/<classID>')
@login_required
def glossaryTemplate(classID):
    print(request.endpoint)
    db_terms = query_db('SELECT term from Glossary WHERE classID="{}"'.format(classID))
    db_defs = query_db('SELECT definition from Glossary WHERE classID="{}"'.format(classID))
    db_class_name = query_db('SELECT className from Classes WHERE classID="{}"'.format(classID), one=True)
    class_name = db_class_name[0]

    terms = []
    defs = []
    for term in db_terms:
        terms.append(term[0])
    for _def in db_defs:
        defs.append(_def[0])
    print(terms)
    print(defs)
    alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
             "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    termsAlpha = sorted(terms)
    defsAlpha = []
    idx = 0
    for idx, t in enumerate(termsAlpha):
        defsAlpha.append("")
        defsAlpha[idx] = defs[terms.index(t)]
        idx += 1
    return render_template('layouts/glossary-template.html', terms=termsAlpha, defns=defsAlpha, classID=classID,
                           enumerate=enumerate, alpha=alpha, class_name=class_name)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        if Role.query.filter_by(name='Professor').one() in current_user.roles:
            return redirect(home_url + "professor-home")
        elif Role.query.filter_by(name='Student').one() in current_user.roles:
            print("think that it has the role ")
            return redirect(home_url + "student-home")
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email = form.data["email"]
        password = form.data["password"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        # check passhash against the database
        user_object = query_db('SELECT * from Users WHERE email="%s" AND password="%s"' % (email, passhash), one=True)
        if user_object is None:
            flash("Unable to find user with those details, please try again")
            return render_template('forms/login.html', form=form)
        else:
            user = User.query.filter_by(id=form.email.data).one()
            print(user)
            print(user.roles)
            session["email"] = form.data["email"]
            login_user(user)
            print(current_user.email)
            if Role.query.filter_by(name='Professor').one() in current_user.roles:
                return redirect(home_url + "professor-home")
            elif Role.query.filter_by(name='Student').one() in current_user.roles:
                print("think that it has the role ")
                return redirect(home_url + "student-home")
    return render_template('forms/login.html', form=form)


@app.route('/new-professor-account', methods=['GET', 'POST'])
def new_prof_acc():
    form = ProfessorRegForm()
    if form.validate_on_submit():
        user_object = query_db('select * from Users where email= ?', [form.data["email"]], one=True)
        if user_object is None:
            password = form.data["password"]
            h = hashlib.md5(password.encode())
            passhash = h.hexdigest()
            user = User(id=form.data["email"], email=form.data["email"], name=form.data["fullName"], active=True,
                        password=passhash)
            role = Role.query.filter_by(name='Professor').one()
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email=form.email.data).first()
            session["email"] = form.data["email"]
            login_user(user)
            return redirect(home_url + "professor-home")
    return render_template('forms/NewProfAccount.html', form=form)


@app.route('/new-student-account', methods=['GET', 'POST'])
def new_student_account():
    form = StudentRegForm()
    if form.validate_on_submit():
        # check that we don't already have this user registered
        user_object = query_db('select * from Users where email= ? ', [form.data["email"]], one=True)
        # insert them into the db
        if user_object is None:
            password = form.data["password"]
            h = hashlib.md5(password.encode())
            passhash = h.hexdigest()
            user = User(
                id=form.data["email"], email=form.data["email"], name=form.data["fullName"], active=True,
                password=passhash)
            # prof_role = Role(name='Student')
            # user.roles = [prof_role]
            role = Role.query.filter_by(name='Student').one()
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            # log in the user
            user_details = User.query.filter_by(email=form.email.data).first()
            session["email"] = form.data["email"]
            login_user(user_details)
            return redirect(home_url + "student-home")
    return render_template('forms/NewStudentAccount.html', form=form)


@app.route('/professor-class-overview/<classID>')
@login_required
@roles_required('Professor')
def professor_class_home(classID):
    print("called professor class home")
    chapters = query_db('SELECT * from Chapters where classID="%s"' % classID)
    print(chapters)
    sections_arrays = []
    for chapter in chapters:
        sections_arrays.append(query_db('SELECT * from Sections where chapterID="%s"' % chapter[0]))

    questions = []
    for sectionarray in sections_arrays:
        for section in sectionarray:
            questions.append(query_db('SELECT * from Questions where sectionID="%s"' % section[0]))
    print(sections_arrays)
    print(questions)
    answers = []
    for question_array in questions:
        for question in question_array:
            answers.append(query_db('SELECT * from Answers where questionID="%s"' % question[0]))
    print(answers)
    class_name = query_db('SELECT * from Classes where classID="%s"' % classID)[0][0]
    print(class_name)
    return render_template('pages/professor_class_overview.html', chapters=chapters, sections=sections_arrays,
                           questions=questions, class_name=class_name, answers=answers, classID=classID)


@app.route('/student-class-overview/<classID>')
@login_required
@roles_required('Student')
def student_class_home(classID):
    chapters = query_db('SELECT * from Chapters where classID="%s"' % classID)
    sections_arrays = []
    for chapter in chapters:
        sections_arrays.append(query_db('SELECT * from Sections where chapterID="%s"' % chapter[0]))

    # questions = []
    # for sectionarray in sections_arrays:
    #    for section in sectionarray:
    #        questions.append(query_db('SELECT * from Questions where sectionID="%s"' % section[0]))
    # answers = []
    # for question_array in questions:
    #    for question in question_array:
    #        answers.append(query_db('SELECT * from Answers where questionID="%s"' % question[0]))
    class_name = query_db('SELECT * from Classes where classID="%s"' % classID)[0][0]
    return render_template('pages/student_class_overview.html', chapters=chapters, sections=sections_arrays,
                           class_name=class_name, classID=classID)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(home_url)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(401)
def not_authed_error(error):
    return render_template('errors/401.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.secret_key = 'xxxxyyyyyzzzzz'
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
