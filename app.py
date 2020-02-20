# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import sqlite3
import hashlib
from flask import g, redirect, abort
from flask import session
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

pathToDB = os.path.abspath("studentlogin.db")
print(pathToDB)

home_url = "http://127.0.0.1:5000/"
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

# Login required decorator.

def login_required(test):
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap



# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('pages/landing.html', homepage=True)


@app.route('/student-quiz')
def student_quiz():
    try:
        session["logged_in"]
        return render_template('pages/placeholder.student.quiz.html')
    except KeyError:
        return abort(401)


@app.route('/student-short')
def student_short():
    try:
        session["logged_in"]
        return render_template('pages/placeholder.student.short.html')
    except KeyError:
        return abort(401)

@app.route('/info-slide')
def infoSlide():
    try:
        session["logged_in"]
        return render_template('layouts/infoSlide.html')
    except KeyError:
        return abort(401)

@app.route('/glossary-template')
def glossaryTemplate():
    return render_template('layouts/glossary-template.html')

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/professor-login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.data["name"]
        password = form.data["password"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        print(passhash)
        #check passhash against the database
        c = db.cursor()
        c.execute('SELECT * from login WHERE username="%s" AND password="%s"' % (username, passhash))
        if c.fetchone() is not None:
            print("Welcome")
        print(username + " tried to login with passcode: " + password)
    return render_template('forms/login.html', form=form)

@app.route('/student-login', methods=('GET', 'POST'))
def studentLogin():
    form = ClassCodeForm()
    if form.validate_on_submit():
        user_code = form.data["classCode"]

        class_object = query_db('select * from ClassCodes where ClassCode = ?',
                                [user_code], one=True)
        if class_object is None:
            print('No such class')
        else:
            session["logged_in"] = True
            return redirect(home_url + "student-quiz")
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
