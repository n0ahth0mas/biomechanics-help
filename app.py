# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask, render_template, request, flash, url_for
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

class UserClasses(db.Model):
    __tablename__ = "Enroll"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), db.ForeignKey('Users.email'))
    classCode = db.Column(db.Integer(), db.ForeignKey('Classes.classCode'))

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
    # User fields
    active = True
    name = db.Column(db.String(255))

user_manager = UserManager(app, get_sql_alc_db(), User)

@app.route('/')
def home():
    return render_template('pages/landing.html', homepage=True)

@app.route('/student-home', methods=('GET', 'POST'))
@login_required
@roles_required('Student')
def student_home():
    #add a class form
    form = AddClass()
    if form.validate_on_submit():
        _class = query_db('SELECT * from Classes WHERE classCode="%s"' % form.data["class_code"], one=True)
        current_user.classes.append(Class(classCode=form.data["class_code"], className=_class[0]))
        db.session.commit()

    #render our classes
    classes_list = []
    print(current_user.classes)
    for _class in current_user.classes:
        classes_list.append(_class.name)
    return render_template('pages/studentHome.html', name=current_user.name, form=form, classes=classes_list)


@app.route('/student-quiz')
@login_required
def student_quiz():
    return render_template('pages/placeholder.student.quiz.html')


@app.route('/professor-home')
@login_required
@roles_required('Professor')
def professor_home():
    return render_template('layouts/professor-home.html', name=current_user.name)


@app.route('/student-short')
@login_required
def student_short():
    return render_template('pages/placeholder.student.short.html')


@app.route('/info-slide')
@login_required
def infoSlide():
    return render_template('layouts/infoSlide.html')


@app.route('/glossary-template')
@login_required
def glossaryTemplate():
    return render_template('layouts/glossary-template.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/professor-login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(home_url + "professor-home")
    if form.validate_on_submit():
        email = form.data["email"]
        password = form.data["password"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        print(passhash)
        # check passhash against the database
        user_object = query_db('SELECT * from Users WHERE email="%s" AND password="%s"' % (email, passhash), one=True)
        if user_object is None:
            print("No such class")
            flash("Something went wrong, please try again")
            return render_template('forms/login.html', form=form)
        else:
            user = User(id=form.data["email"], email=form.data["email"], name=user_object[2], active=True,
                        password=passhash)
            login_user(user)
            return redirect(home_url + "professor-home")
    return render_template('forms/login.html', form=form)


@app.route('/student-login', methods=('GET', 'POST'))
def studentLogin():
    form = StudentLoginForm()
    if current_user.is_authenticated:
        return redirect(home_url + "student-home")
    if form.validate_on_submit():
        email = form.data["email"]
        password = form.data["password"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        user_object = query_db('select * from Users where email="%s" AND password="%s"' % (email, passhash),
                               one=True)
        if user_object is None:
            print('No such class')
            return render_template('forms/classcode.html', form=form)
        else:
            user = User(id=form.data["email"], email=form.data["email"], name=user_object[2], active=True, password=passhash)
            login_user(user)
            return redirect(home_url + "student-home")
    return render_template('forms/classcode.html', form=form)


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
            user.roles = [Role(name="Professor")]
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
            prof_role = Role(name='Student')
            user.roles = [prof_role]
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