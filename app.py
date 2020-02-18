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

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = sqlite3.connect('login.db')

cur = db.cursor()


# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('pages/landing.html', homepage=True)


@app.route('/student-quiz')
def student_quiz():
    return render_template('pages/placeholder.student.quiz.html')


@app.route('/student-short')
def student_short():
    return render_template('pages/placeholder.student.short.html')

@app.route('/info-slide')
def infoSlide():
    return render_template('layouts/infoSlide.html')

@app.route('/professor-home')
def profHome():
    return render_template('layouts/professor-home.html')

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
        print(username + " tried to login with passcode: " + password)
    return render_template('forms/login.html', form=form)

@app.route('/student-login', methods=('GET', 'POST'))
def studentLogin():
    form = ClassCodeForm()
    if form.validate_on_submit():
        userCode = form.data["classCode"]
        print("thinks we submitted the form: " + userCode)
    return render_template('forms/classcode.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


# @app.errorhandler(404)
# def not_found_error(error):
#    return render_template('errors/404.html'), 404

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
