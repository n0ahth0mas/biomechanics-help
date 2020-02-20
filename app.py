# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from user import *
import os
import sqlite3
import hashlib
from flask import g, redirect, abort
from flask import session
from flask_login import current_user, login_user, LoginManager, UserMixin
from functools import wraps

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
login = LoginManager(app)
pathToDB = os.path.abspath("studentlogin.db")
print(pathToDB)

home_url = "http://127.0.0.1:5000/"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(pathToDB)
    return db

@login.user_loader
def load_user(email):
    user_object = query_db('select * from StudentAccounts where email= ? ', [email], one=True)
    user = User(email=user_object[0], password=user_object[1], classes=user_object[2], active=True)
    return user

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


# Login required decorator.

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('home'))
    return wrap


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('pages/landing.html', homepage=True)

@app.route('/student-home')
@login_required
def student_home():
    print("called student home")
    classes = current_user.get_classes()
    print(classes)
    return render_template('pages/studentHome.html', classes=classes)


@app.route('/student-quiz')
@login_required
def student_quiz():
    return render_template('pages/placeholder.student.quiz.html')

@app.route('/professor-home')
@login_required
def professor_home():
    return render_template('layouts/professor-home.html')


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

@app.route('/professor-home')
@login_required
def profHome():
    return render_template('layouts/professor-home.html')

@app.route('/professor-login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.data["name"]
        password = form.data["password"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        print(passhash)
        # check passhash against the database
        c = db.cursor()
        c.execute('SELECT * from login WHERE username="%s" AND password="%s"' % (username, passhash))
        if c.fetchone() is not None:
            print("Welcome")
        print(username + " tried to login with passcode: " + password)
    return render_template('forms/login.html', form=form)


@app.route('/student-login', methods=('GET', 'POST'))
def studentLogin():
    form = StudentLoginForm()
    if form.validate_on_submit():
        email = form.data["email"]
        password = form.data["password"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        user_object = query_db('select * from StudentAccounts where email="%s" AND password="%s"' % (email, passhash),
                               one=True)
        if user_object is None:
            print('No such class')
        else:
            user = User(email=user_object[0], password=user_object[1], classes=user_object[2], active=True)
            login_user(user)
            if current_user.is_authenticated:
                print("current user authenticated")
            return redirect(home_url + "student-home")
    return render_template('forms/classcode.html', form=form)


@app.route('/new-professor-account', methods=['GET', 'POST'])
def new_prof_acc():
    form = ProfessorRegForm()
    if form.validate_on_submit():
        print("form was validated")
        print(form.data["fullName"])
        password = form.data["password"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        print(passhash)

        cursor.execute(
            'insert into login (username,email,password) values (?,?,?)',
            (
                form.data["fullName"],
                passhash,
                form.data["email"]
            )
        )

        print("past insertion")
    return render_template('forms/NewProfAccount.html', form=form)


@app.route('/new-student-account', methods=['GET', 'POST'])
def new_student_account():
    form = StudentRegForm()
    if form.validate_on_submit():

        password = form.data["password"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        print(passhash)

        # check that we don't already have this user registered
        user_object = query_db(
            'select * from StudentAccounts where email= ? ', [form.data["email"]], one=True)
        # insert them into the db
        if user_object is None:
            cursor = get_db().cursor()
            courses = "BioPhysics"
            password = form.data["password"]
            h = hashlib.md5(password.encode())
            passhash = h.hexdigest()
            cursor.execute(
                'INSERT INTO StudentAccounts (email,password,courses) values (?,?,?)',
                (
                    str(form.data["email"]),
                    str(passhash),
                    courses
                )
            )
            get_db().commit()
            return redirect(home_url)
        else:
            return render_template('forms/NewStudentAccount.html', form=form)
    return render_template('forms/NewStudentAccount.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
