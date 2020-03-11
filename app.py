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
#app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/help.db'
app.config['USER_EMAIL_SENDER_EMAIL'] = "jriley9000@gmail.com"
#login = LoginManager()
#login.init_app(app)
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
    className = db.Column(db.String(), unique=True)

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

@app.route('/edit-class/<class_id>')
def edit_class(class_id):
    #we want to get this class from the database
    #we want to display all of its sections here
    this_class = query_db('SELECT * from Classes where classID="%s"' % class_id, one=True)

    chapters = query_db('SELECT * from Chapters where classID="%s"' % class_id)
    section_array = [[]]
    #initialize sections in our class datastructure
    #for chapter in chapters:
        #section_array.append(query_db('SELECT * from Sections where chapterID="%s"' % chapter[0]))

    #questions = [[[]]]
    #for chapter in section_array:
    #    for section in chapter:
    #        questions.append()


    return render_template('pages/edit-class.html')

@app.route('/student-home', methods=('GET', 'POST'))
@login_required
@roles_required('Student')
def student_home():
    print(request.endpoint)
    #add a class form
    form = AddClass()
    if form.validate_on_submit():
        one_class = Class.query.filter_by(classID=form.data["class_code"]).one()
        current_user.classes.append(one_class)
        db.session.commit()

    #render our classes
    classes_list = []
    print(current_user.classes)
    for _class in current_user.classes:
        #we want to use the class code to get a class name from classes
        _class = query_db('SELECT * from Classes WHERE classID="%s"' % _class.classID, one=True)
        classes_list.append(_class)
    return render_template('pages/studentHome.html', name=current_user.name, form=form, classes=classes_list)


@app.route('/student-quiz/<class_id>/<chapter>/<section>', methods=['GET'])
@login_required
def student_quiz(class_id, chapter, section):
    if query_db('SELECT * from Enroll where email="%s" AND classID="%s"' % (session["email"], class_id)) != []:
        a_list = []
        #creating a list of questions for the page
        q_list = query_db('SELECT * from Questions where sectionID="%s"' % section)
        q_list2 = json.dumps(q_list)
        #finding all the answers of the questions on the page
        for questions in q_list:
            answer_id = questions[0]
            print(answer_id)
            print("{}".format(answer_id))
            a_list.append(query_db('SELECT * from Answers where questionID = "{}"'.format(answer_id)))
        a_list2 = json.dumps(a_list)
        return render_template('pages/placeholder.student.quiz.html', chapter=chapter, section=section, q_list=q_list2,
                               a_list=a_list2, classID=class_id)
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


@app.route('/info-slide')
@login_required
def infoSlide():
    return render_template('layouts/infoSlide.html')

@app.route('/glossary/<classID>')
@login_required
def glossaryTemplate(classID):
    db_terms = query_db('SELECT term from Glossary WHERE classID="{}"'.format(classID))
    db_defs = query_db('SELECT definition from Glossary WHERE classID="{}"'.format(classID))
    db_class_name = query_db('SELECT className from Classes WHERE classID="{}"'.format(classID), one=True)
    class_name = db_class_name[0]

    #terms = ["Physics", "Braden"]
    #defs = ["science of physics", "cool dude"]
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
        idx+=1
    return render_template('layouts/glossary-template.html', terms=termsAlpha, defns=defsAlpha, classID=classID,
                            enumerate=enumerate, alpha=alpha, class_name=class_name)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
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
            user = User(id=form.data["email"], email=form.data["email"], name=user_object[2], active=True,
                        password=passhash)
            session["email"] = form.data["email"]
            login_user(user)
            print(current_user.email)
            if current_user.is_authenticated:
                if query_db('SELECT * from User_roles WHERE user_id="%s" AND role_id="%s"' % (email, 35),
                                       one=True):
                    print("thinks that it has the role Professor")
                    return redirect(home_url + "professor-home")
                elif query_db('SELECT * from User_roles WHERE user_id="%s" AND role_id="%s"' % (email, 36),
                                       one=True):
                    print("think that it has the role ")
                    return redirect(home_url + "student-home")
                else:
                    print("couldnt find any roles associated with this user")
                    return redirect(home_url)
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
            user = User(id=form.data["email"], email=form.data["email"], name=form.data["fullName"], active=True, password=passhash)
            role = Role.query.filter_by(name='Professor').one()
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email=form.email.data).first()
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
            #prof_role = Role(name='Student')
            #user.roles = [prof_role]
            role = Role.query.filter_by(name='Student').one()
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            #log in the user
            user_details = User.query.filter_by(email=form.email.data).first()
            login_user(user_details)
            return redirect(home_url + "student-home")
    return render_template('forms/NewStudentAccount.html', form=form)


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