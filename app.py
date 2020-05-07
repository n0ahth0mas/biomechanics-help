# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
from time import time
import jwt
import sys
from werkzeug.utils import secure_filename

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
from sqlalchemy import and_, text
class ConfigClass(object):
    SECRET_KEY = 'xxxxyyyyyzzzzz'
    USER_UNAUTHENTICATED_ENDPOINT = 'login'
    USER_UNAUTHORIZED_ENDPOINT = 'login'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/help.db'
    USER_EMAIL_SENDER_EMAIL = "jriley9000@gmail.com"
    UPLOAD_FOLDER = os.path.abspath('static/img')
    UPLOAD_VIDEO_FOLDER = os.path.abspath('static/video')

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')
#app.secret_key = 'xxxxyyyyyzzzzz'
# app.config.from_object('config')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/help.db'
#app.config['USER_EMAIL_SENDER_EMAIL'] = "jriley9000@gmail.com"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}
ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'mov'}
#UPLOAD_FOLDER = os.path.abspath('static/img')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#UPLOAD_VIDEO_FOLDER = os.path.abspath('static/video')
#app.config['UPLOAD_VIDEO_FOLDER'] = UPLOAD_VIDEO_FOLDER
# login = LoginManager()
# login.init_app(app)
pathToDB = os.path.abspath("database/help.db")
db = SQLAlchemy(app)
print(pathToDB)
sender = "pugetsoundhelp@gmail.com"
home_url = "http://127.0.0.1:5000/"

smtpObj = smtplib.SMTP(host="smtp.gmail.com", port=587)
smtpObj.starttls()
smtpObj.login(sender, "Mouse12345!")

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


def get_user_token(email):
    # we want to use our database to get an id for this user from their email, we then use this id to generate a token that is unique to that user.
    return jwt.encode({'reset_password': email, 'exp': time() + 600}, app.config['SECRET_KEY'],
                      algorithm='HS256').decode('utf-8')


def verify_reset_password_token(token):
    try:
        id = jwt.decode(token, app.config['SECRET_KEY'],
                        algorithms=['HS256'])['reset_password']
    except:
        return -1
    return id


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_video(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_VIDEO


# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

class Class(db.Model):
    __tablename__ = "Classes"
    classID = db.Column(db.Integer(), primary_key=True)
    className = db.Column(db.String())
    chapters = db.relationship("Chapter", cascade="all, delete-orphan, save-update")
    enrolled = db.relationship("UserClasses", cascade="all, delete-orphan, save-update")
    glossary = db.relationship("Glossary", cascade="all, delete-orphan, save-update")


class Chapter(db.Model):
    __tablename__ = 'Chapters'
    chapterID = db.Column(db.Integer(), primary_key=True)
    chapterName = db.Column(db.String())
    classID = db.Column(db.String(), db.ForeignKey('Classes.classID'))
    orderNo = db.Column(db.Integer())
    publish = db.Column(db.Boolean())
    sections = db.relationship("Section", cascade="all, delete-orphan, save-update")


class Section(db.Model):
    __tablename__ = 'Sections'
    sectionID = db.Column(db.Integer(), primary_key=True)
    chapterID = db.Column(db.Integer(), db.ForeignKey('Chapters.chapterID'))
    sectionName = db.Column(db.String())
    orderNo = db.Column(db.Integer())
    publish = db.Column(db.Boolean())
    sectionBlocks = db.relationship("SectionBlock", cascade="all, delete-orphan, save-update")
    questions = db.relationship("Question", cascade="all, delete-orphan, save-update")
    videos = db.relationship("Video", cascade="all, delete-orphan, save-update")


class Glossary(db.Model):
    __tablename__ = 'Glossary'
    classID = db.Column(db.Integer(), db.ForeignKey('Classes.classID'))
    termID = db.Column(db.Integer(), primary_key=True)
    term = db.Column(db.String())
    definition = db.Column(db.String())
    images = db.relationship("GlossaryImages", cascade="all, delete-orphan")


class GlossaryImages(db.Model):
    __tablename__ = 'GlossaryImages'
    termID = db.Column(db.Integer(), db.ForeignKey('Glossary.termID'), primary_key=True)
    imageFile = db.Column(db.String(), primary_key=True)

    class Meta:
        unique_together = (("termID", "imageFile"),)


class SectionBlock(db.Model):
    __tablename__ = 'SectionBlock'
    orderNo = db.Column(db.Integer())
    sectionBlockID = db.Column(db.Integer(), primary_key=True)
    sectionText = db.Column(db.String())
    sectionID = db.Column(db.Integer(), db.ForeignKey('Sections.sectionID'))
    images = db.relationship("SectionBlockImages", cascade="all, delete-orphan")


class SectionBlockImages(db.Model):
    __tablename__ = 'SectionBlockImages'
    sectionBlockID = db.Column(db.Integer(), db.ForeignKey('SectionBlock.sectionBlockID'), primary_key=True)
    imageFile = db.Column(db.String(), primary_key=True)
    xposition = db.Column(db.String())
    yposition = db.Column(db.String())

    class Meta:
        unique_together = (("sectionBlockID", "imageFile"),)


class Question(db.Model):
    __tablename__ = 'Questions'
    questionID = db.Column(db.Integer(), primary_key=True)
    questionText = db.Column(db.String())
    sectionID = db.Column(db.Integer(), db.ForeignKey('Sections.sectionID'))
    questionType = db.Column(db.String())
    orderNo = db.Column(db.Integer())
    imageFile = db.Column(db.String())
    answers = db.relationship("Answer", cascade="all, delete-orphan")


class School(db.Model):
    __tablename__ = 'School'
    schoolID = db.Column(db.Integer(), primary_key=True)
    schoolName = db.Column(db.String())
    subscription = db.Column(db.Boolean())


class Answer(db.Model):
    __tablename__ = 'Answers'
    answerID = db.Column(db.Integer(), primary_key=True)
    questionID = db.Column(db.Integer(), db.ForeignKey('Questions.questionID'))
    correctness = db.Column(db.String())
    answerText = db.Column(db.String())
    answerReason = db.Column(db.String())
    xPosition = db.Column(db.String())
    yPosition = db.Column(db.String())
    imageFile = db.Column(db.String())
    dropBoxHeightAdjustment = db.Column(db.Integer())
    dropBoxWidthAdjustment = db.Column(db.Integer())
    dropBoxColor = db.Column(db.String())


class Video(db.Model):
    __tablename__ = 'Videos'
    sectionID = db.Column(db.Integer(), db.ForeignKey('Sections.sectionID'), primary_key=True)
    videoFile = db.Column(db.String(), primary_key=True)
    orderNo = db.Column(db.Integer())

    class Meta:
        unique_together = (("sectionID", "videoFile"),)


class UserClasses(db.Model):
    __tablename__ = "Enroll"
    email = db.Column(db.String(), db.ForeignKey('Users.email'), primary_key=True)
    classID = db.Column(db.Integer(), db.ForeignKey('Classes.classID'), primary_key=True)
    lastSectionID = db.Column(db.Integer(), db.ForeignKey('Sections.sectionID'))

    class Meta:
        unique_together = (("email", "classID"),)


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
    schoolID = db.Column(db.String(), db.ForeignKey('School.schoolID'))
    roles = db.relationship('Role', secondary='User_roles')
    classes = db.relationship('Class', secondary='Enroll')
    active = True
    name = db.Column(db.String(255))

    def has_role(self, role):
        return role in self.roles

    def has_role_name(self, name):
        for role in self.roles:
            if role.name == name:
                return True
        return False

    def get_email(self):
        return self.email


user_manager = UserManager(app, get_sql_alc_db(), User)

@app.route('/')
def home():
    adminID = "3141592653589admin"
    print(query_db('SELECT * from School where schoolID="%s"' % adminID))
    if not query_db('SELECT * from School where schoolID="%s"' % adminID):
        admin = School()
        admin.schoolID = adminID
        admin.schoolName = "administrator"
        admin.subscription = True
        roleP = Role()
        roleP.id = 35
        roleP.name = "Professor"
        roleS = Role()
        roleS.id = 36
        roleS.name = "Student"
        db.session.add(admin)
        db.session.add(roleP)
        db.session.add(roleS)
        db.session.commit()

    return render_template('pages/landing.html')


@app.route('/edit-class/<classID>', methods=('GET', 'POST'))
@roles_required('Professor')
def edit_class(classID):
    formEdit = EditChapter()
    form = CreateChapter()
    form_publish = PublishChapter()
    active = School.query.filter_by(schoolID=current_user.schoolID).first()
    if not active.subscription:
        flash("Sorry, the organization you are currently enrolled for is inactive. Please contact pugetsoundhelp@gmail.com for more information")
        return redirect('/professor-home')
    if formEdit.orderNo1.data is not None and formEdit.validate():
        chapterID = formEdit.data["chapterID"]
        one_chapter = Chapter.query.filter_by(chapterID=chapterID).first()
        one_chapter.orderNo = formEdit.data["orderNo1"]
        one_chapter.chapterName = formEdit.data["chapterName"]
        db.session.commit()
        return redirect('/edit-class/%s' % classID)
    elif request.method == 'POST':
        pass
    if form.orderNo2.data is not None and form.validate():
        one_chapter = Chapter()
        one_chapter.orderNo = form.data["orderNo2"]
        one_chapter.chapterName = form.data["chapterName"]
        one_chapter.classID = classID
        one_chapter.publish = False
        db.session.add(one_chapter)
        db.session.commit()
        print(classID)
        return redirect('/edit-class/%s' % classID)
    elif request.method == 'POST':
        pass

    if not form_publish.chapterID.data == "" and form_publish.validate() and not form.validate() and form.orderNo2.data is None:
        chapterID = form_publish.data["chapterID"]
        one_chapter = Chapter.query.filter_by(chapterID=chapterID).first()
        one_chapter.publish = not one_chapter.publish
        db.session.commit()
    elif request.method == 'POST':
        pass
    className = query_db('SELECT * from Classes where classID="%s"' % classID)[0][0]
    chapters = query_db('SELECT * from Chapters where classID="%s" ORDER BY orderNo' % classID)
    sections_arrays = []
    for chapter in chapters:
        sections_arrays.append(query_db('SELECT * from Sections where chapterID="%s"' % chapter[0]))
    x_loop_must_break = False
    for chapter in chapters:
        for check in chapters:
            if not chapter[0] == check[0]:
                if chapter[3] == check[3]:
                    flash("Error: Chapter Numbers are not unique. Fix and close error message before moving on")
                    x_loop_must_break = True
                    break
        if x_loop_must_break:
            break
    return render_template('pages/edit-class.html', chapters=chapters, sections=sections_arrays, classID=classID,
                           className=className, form=form, formEdit=formEdit, form_publish=form_publish)


@app.route('/edit-class/<classID>/glossary', methods=('GET', 'POST'))
@roles_required('Professor')
def edit_glossary(classID):
    active = School.query.filter_by(schoolID=current_user.schoolID).first()
    if not active.subscription:
        flash(
            "Sorry, the organization you are currently enrolled for is inactive. Please contact pugetsoundhelp@gmail.com for more information")
        return redirect('/professor-home')
    form = CreateTerm()
    if form.term.data is not None and form.validate():
        one_entry = Glossary()
        one_entry.classID = classID
        one_entry.term = form.data["term"]
        one_entry.definition = form.data["definition"]
        db.session.add(one_entry)
        db.session.commit()
        one_image = GlossaryImages()
        one_image.termID = one_entry.termID
        image = request.files["imageFile"]
        if 'imageFile' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            img_path = os.path.join((app.config['UPLOAD_FOLDER'] + "/" + str(classID)), filename)
            image.save(img_path)
            one_image.imageFile = "/static/img/" + str(classID) + "/" + filename
        if image and GlossaryImages.query.filter_by(termID=one_image.termID).filter_by(
                imageFile=one_image.imageFile).first() is None:
            db.session.add(one_image)
            db.session.commit()

        return redirect('/edit-class/%s/glossary' % classID)
    elif request.method == 'POST':
        pass
    form_edit = EditTerm()
    if form_edit.term_e.data is not None and form_edit.validate():
        termID = form_edit.data["termID"]
        edit_term = Glossary.query.filter_by(termID=termID).first()
        edit_term.term = form_edit.data["term_e"]
        edit_term.definition = form_edit.data["definition"]
        db.session.commit()
        return redirect('/edit-class/%s/glossary' % classID)
    elif request.method == 'POST':
        pass
    form_i = CreateGlossaryImage()
    if form_i.validate_on_submit():
        one_image = GlossaryImages()
        one_image.termID = form_i.data["termID"]
        image = request.files["imageFile"]
        if 'imageFile' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            img_path = os.path.join((app.config['UPLOAD_FOLDER'] + "/" + str(classID)), filename)
            image.save(img_path)
            one_image.imageFile = "/static/img/" + str(classID) + "/" + filename
        if GlossaryImages.query.filter_by(termID=one_image.termID).filter_by(imageFile=one_image.imageFile).first() is None:
            db.session.add(one_image)
            db.session.commit()
        else:
            flash("Image already exist for that term")
        return redirect('/edit-class/%s/glossary' % classID)
    elif request.method == 'POST':
        pass

    form_delete_image = DeleteTermImage()
    if form_delete_image.validate() and form_delete_image.termID3:
        termID = form_delete_image.data["termID3"]
        imageFile = form_delete_image.data["imageFile"]
        image_to_delete = GlossaryImages.query.filter_by(termID=termID).filter_by(imageFile=imageFile).first()
        db.session.delete(image_to_delete)
        db.session.commit()
    className = query_db('SELECT * from Classes where classID="%s"' % classID)[0][0]

    terms = query_db('SELECT * from Glossary where classID="%s"' % classID)
    image_files = []
    for term in terms:
        images = query_db('SELECT * from GlossaryImages where termID="%s"' % term[1])
        for image in images:
            image_files.append(image)
    links = []
    for image_file in image_files:
        links.append((image_file[0], image_file[1], image_file[1].replace("/", "%%")))
    print(links)
    return render_template('pages/edit-glossary.html', classID=classID, form=form, terms=terms, className=className,
                           form_i=form_i, image_files=image_files, form_edit=form_edit, links=links, form_delete_image=form_delete_image)


@app.route('/edit-class/<classID>/<chapterID>', methods=('GET', 'POST'))
@roles_required('Professor')
def edit_chapter(classID, chapterID):
    active = School.query.filter_by(schoolID=current_user.schoolID).first()
    if not active.subscription:
        flash(
            "Sorry, the organization you are currently enrolled for is inactive. Please contact pugetsoundhelp@gmail.com for more information")
        return redirect('/professor-home')
    form = CreateSection()
    if form.orderNo2.data is not None and form.validate():
        one_section = Section()
        one_section.chapterID = chapterID
        one_section.orderNo = form.data["orderNo2"]
        one_section.sectionName = form.data["sectionName"]
        one_section.publish = False
        db.session.add(one_section)
        db.session.commit()
        return redirect('/edit-class/%s/%s' % (classID, chapterID))
    elif request.method == 'POST':
        pass
    form_edit = EditSection()
    if form_edit.orderNo1.data is not None and form_edit.validate():
        sectionID = form_edit.data["sectionID"]
        one_section = Section.query.filter_by(sectionID=sectionID).first()
        one_section.orderNo = form_edit.data["orderNo1"]
        one_section.sectionName = form_edit.data["sectionName"]
        db.session.commit()
        return redirect('/edit-class/%s/%s' % (classID, chapterID))
    elif request.method == 'POST':
        pass
    form_publish = PublishSection()
    if not form_publish.sectionID.data == "" and form_publish.validate() and not form.validate() and form.orderNo2.data is None:
        sectionID = form_publish.data["sectionID"]
        one_section = Section.query.filter_by(sectionID=sectionID).first()
        one_section.publish = not one_section.publish
        db.session.commit()
    elif request.method == 'POST':
        pass


    className = query_db('SELECT * from Classes where classID="%s"' % classID)[0][0]
    chapterName = query_db('SELECT chapterName from Chapters where chapterID="%s"' % chapterID)[0][0]
    sections = query_db('SELECT * from Sections where chapterID="%s"' % chapterID)

    x_loop_must_break = False
    for section in sections:
        for check in sections:
            if not section[0] == check[0]:
                if section[3] == check[3]:
                    flash("Error: Section Numbers are not unique. Fix and close error message before moving on")
                    x_loop_must_break = True
                    break
        if x_loop_must_break:
            break
    return render_template('pages/edit-chapter.html', sections=sections, chapterID=chapterID, classID=classID,
                           chapterName=chapterName, className=className, form=form, form_edit=form_edit,
                           form_publish=form_publish)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>', methods=('GET', 'POST'))
@roles_required('Professor')
def edit_section(classID, chapterID, sectionID):
    active = School.query.filter_by(schoolID=current_user.schoolID).first()
    if not active.subscription:
        flash(
            "Sorry, the organization you are currently enrolled for is inactive. Please contact pugetsoundhelp@gmail.com for more information")
        return redirect('/professor-home')
    sectionBlocks = query_db('SELECT * from SectionBlock where sectionID="%s" ORDER BY orderNo' % sectionID)
    image_files = []
    for sectionBlock in sectionBlocks:
        images = query_db('SELECT * from SectionBlockImages where sectionBlockID="%s"' % sectionBlock[0])
        for image in images:
            image_files.append(image)
    links = []
    for image_file in image_files:
        links.append((image_file[0], image_file[1], image_file[1].replace("/", "%%")))

    videos = query_db('SELECT * from Videos where sectionID="%s" ORDER BY orderNo' % sectionID)
    video_links = []
    for video in videos:
        video_links.append((video[1], video[1].replace("/", "%%%")))
    form_s = CreateSectionBlock()
    if form_s.orderNo2.data is not None and form_s.validate():
        one_section_block = SectionBlock()
        one_section_block.orderNo = form_s.data["orderNo2"]
        one_section_block.sectionText = form_s.data["sectionText"]
        one_section_block.sectionID = sectionID
        db.session.add(one_section_block)
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
    elif request.method == 'POST':
        pass
    form_edit = EditSectionBlock()
    if form_edit.orderNo1.data is not None and form_edit.validate():
        sectionBlockID = form_edit.data["sectionBlockID"]
        one_section_block = SectionBlock.query.filter_by(sectionBlockID=sectionBlockID).first()
        one_section_block.orderNo = form_edit.data["orderNo1"]
        one_section_block.sectionText = form_edit.data["text"]
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
    elif request.method == 'POST':
        pass
    form_q = CreateQuestion()
    if form_q.orderNo3.data is not None and form_q.validate_on_submit():
        one_question = Question()
        one_question.questionText = form_q.data["questionText"]
        one_question.orderNo = form_q.data["orderNo3"]
        # we need to check and make sure that the order of this question wont clash with other order conflicts
        one_question.sectionID = sectionID
        print(query_db('SELECT * from Questions where orderNo="%s"' % one_question.orderNo) is not None)
        # if query_db('SELECT * from Questions where orderNo="%s"' % one_question.orderNo) is not None:
        # then we are about to have a conflict
        # flash('Please enter a question order number that does not already exist.')
        # return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
        one_question.questionType = form_q.data["questionType"]
        if not form_q.data["imageFile2"]:
            one_question.imageFile = "/static/img/question.png"
            # we want to decline producing this form if there is no image and we are a drag and drop question
            if one_question.questionType == 'dragndrop' or one_question.questionType == 'pointnclick':
                flash('Please provide a question image for this question type.')
                return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
        else:
            image = request.files["imageFile2"]
            if 'imageFile2' not in request.files:
                return redirect(request.url)
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                img_path = os.path.join((app.config['UPLOAD_FOLDER'] + "/" + str(classID)), filename)
                image.save(img_path)
                one_question.imageFile = "/static/img/" + str(classID) + "/" + filename
        db.session.add(one_question)
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
    elif request.method == 'POST':
        pass
    form_edit_question = EditQuestion()
    if form_edit_question.orderNo5.data is not None and form_edit_question.validate_on_submit():
        questionID = form_edit_question.data["questionID"]
        one_question = Question.query.filter_by(questionID=questionID).first()
        one_question.questionText = form_edit_question.data["questionText"]
        one_question.orderNo = form_edit_question.data["orderNo5"]
        if not form_edit_question.data["questionType"] == "":
            one_question.questionType = form_edit_question.data["questionType"]
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
    elif request.method == 'POST':
        pass
    form_v = CreateVideo()
    if form_v.videoFile.data is not None and form_v.validate_on_submit():
        one_video = Video()
        one_video.sectionID = sectionID
        one_video.orderNo = form_v.data["orderNo"]
        video = request.files["videoFile"]
        if 'videoFile' not in request.files:
            return redirect(request.url)
        if video and allowed_video(video.filename):
            filename = secure_filename(video.filename)
            video_path = os.path.join((app.config['UPLOAD_VIDEO_FOLDER'] + "/" + str(classID)), filename)
            video.save(video_path)
            one_video.videoFile = "/static/video/" + str(classID) + "/" + filename
        db.session.add(one_video)
        counter=0
        if len(videos) > 0:
            for v in videos:
                counter = counter + 1
                if not allowed_video(video.filename):
                    flash("Video must be .mp4 or .mov")
                    break
                elif one_video.videoFile == v[1]:
                    flash("Video already exists for this section")
                    break

                elif counter == len(videos):
                    db.session.commit()
        else:
            db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
    elif request.method == 'POST':
        pass
    form_si = CreateSectionBlockImages()
    if form_si.sectionBlockID4.data is not None and form_si.validate_on_submit():
        if SectionBlockImages.query.filter_by(sectionBlockID=form_si.data["sectionBlockID4"]).first() is None:
            one_image = SectionBlockImages()
            one_image.sectionBlockID = form_si.data["sectionBlockID4"]
        else:
            one_image = SectionBlockImages.query.filter_by(sectionBlockID=form_si.data["sectionBlockID4"]).first()
        image = request.files["imageFile"]
        if 'imageFile' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            img_path = os.path.join((app.config['UPLOAD_FOLDER'] + "/" + str(classID)), filename)
            image.save(img_path)
            one_image.imageFile = "/static/img/" + str(classID) + "/" + filename
            one_image.xposition = form_si.data["xposition"]
            one_image.yposition = form_si.data["yposition"]
            db.session.add(one_image)
            db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
    form_delete_image = DeleteImage()
    print(form_delete_image.validate())
    print(form_delete_image.sectionBlockID2.data)
    if form_delete_image.sectionBlockID2.data is not None and form_delete_image.validate() and not form_delete_image.sectionBlockID2.data == "":
        sectionBlockID = form_delete_image.data["sectionBlockID2"]
        one_image = SectionBlockImages.query.filter_by(sectionBlockID=sectionBlockID).first()
        db.session.delete(one_image)
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))

    elif request.method == 'POST':
        pass

    form_change = ChangeImage()
    if form_change.imageFile1.data is not None and form_change.validate():
        questionID = form_change.data["questionID"]
        question_to_change = Question.query.filter_by(questionID=questionID).first()
        image = request.files["imageFile1"]
        if 'imageFile1' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            img_path = os.path.join((app.config['UPLOAD_FOLDER'] + "/" + str(classID)), filename)
            image.save(img_path)
            question_to_change.imageFile = "/static/img/" + str(classID) + "/" + filename
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
    elif request.method == 'POST':
        pass

    form_edit_video = EditVideo()
    if not form_edit_video.orderNo6.data == "" and form_edit_video.validate():
        videoFile = form_edit_video.data["videoFile"]
        one_video = Video.query.filter_by(sectionID=sectionID).filter_by(videoFile=videoFile).first()
        one_video.orderNo = form_edit_video.data["orderNo6"]
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))
    elif request.method == 'POST':
        pass

    form_delete_video = DeleteVideo()
    if form_delete_video.videoFile2.data is not None and form_delete_video.validate():
        videoFile = form_delete_video.data["videoFile2"]
        print("here")
        one_video = Video.query.filter_by(sectionID=sectionID).filter_by(videoFile=videoFile).first()
        print(one_video)
        db.session.delete(one_video)
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s' % (classID, chapterID, sectionID))

    elif request.method == 'POST':
        pass

    className = query_db('SELECT * from Classes where classID="%s"' % classID)[0][0]
    sectionName = query_db('SELECT sectionName from Sections where sectionID="%s"' % sectionID)[0][0]
    questions = query_db('SELECT * from Questions where sectionID="%s" ORDER BY orderNo' % sectionID)

    chapterName = query_db('SELECT chapterName from Chapters where chapterID="%s"' % chapterID)[0][0]
    answers = []
    for question in questions:
        answers.append(query_db('SELECT * from Answers where questionID="%s"' % question[0]))

    x_loop_must_break = False
    for sectionBlock in sectionBlocks:
        for check in sectionBlocks:
            if not sectionBlock[0] == check[0]:
                if sectionBlock[3] == check[3]:
                    flash("Error: Text Numbers are not unique. Fix and close error message before moving on")
                    x_loop_must_break = True
                    break
        if x_loop_must_break:
            break
    y_loop_must_break = False
    for question in questions:
        for check in questions:
            if not question[0] == check[0]:
                if question[4] == check[4]:
                    flash("Error: Question Numbers are not unique. Fix and close error message before moving on")
                    y_loop_must_break = True
                    break
        if y_loop_must_break:
            break
    z_loop_must_break = False
    for video in videos:
        for check in videos:
            if not video[1] == check[1]:
                if video[2] == check[2]:
                    flash("Error: Video Order Numbers are not unique. Fix and close error message before moving on")
                    z_loop_must_break = True
                    break
        if z_loop_must_break:
            break
    return render_template('pages/edit-section.html', className=className, sectionBlocks=sectionBlocks, classID=classID,
                           chapterName=chapterName, chapterID=chapterID, sectionID=sectionID, sectionName=sectionName,
                           questions=questions, answers=answers, videos=videos, form_s=form_s, form_q=form_q, form_edit_video=form_edit_video,
                           form_v=form_v, form_si=form_si, image_files=image_files, form_edit=form_edit,
                           form_edit_question=form_edit_question, form_change=form_change, links=links, video_links=video_links, form_delete_image=form_delete_image,
                           form_delete_video=form_delete_video)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>/text/<sectionBlockID>', methods=('GET', 'POST'))
@roles_required('Professor')
def edit_section_block(classID, chapterID, sectionID, sectionBlockID):
    active = School.query.filter_by(schoolID=current_user.schoolID).first()
    if not active.subscription:
        flash(
            "Sorry, the organization you are currently enrolled for is inactive. Please contact pugetsoundhelp@gmail.com for more information")
        return redirect('/professor-home')
    sectionText = query_db('SELECT sectionText from Sections where sectionID="%s"' % sectionBlockID)[0][0]
    sectionBlocks = query_db('SELECT * from SectionBlock where sectionID="%s"' % sectionID)
    return render_template('pages/edit-section-block.html', sectionBlocks=sectionBlocks, classID=classID,
                           chapterID=chapterID, sectionID=sectionID, sectionName=sectionName, links=links)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>/question/<questionID>', methods=('GET', 'POST'))
@roles_required('Professor')
def edit_question(classID, chapterID, sectionID, questionID):
    active = School.query.filter_by(schoolID=current_user.schoolID).first()
    if not active.subscription:
        flash(
            "Sorry, the organization you are currently enrolled for is inactive. Please contact pugetsoundhelp@gmail.com for more information")
        return redirect('/professor-home')
    point_n_click_answer_form = PointNClickAnswer()
    drag_n_drop_image_form = UploadDragNDropImage()
    drag_n_drop_form = CreateDragNDropAnswer()
    form_a = CreateAnswer()
    form_short = CreateShortAnswer()
    local_img_path = ""
    drag_n_drop_correct = ""
    if point_n_click_answer_form.answer_box_width.data is not None and point_n_click_answer_form.validate():
        # validated point and click answer form
        point_answer = Answer()
        point_answer.questionID = questionID
        point_answer.correctness = point_n_click_answer_form.correctness.data
        point_answer.answerText = ""
        point_answer.answerReason = point_n_click_answer_form.answerReason.data
        point_answer.xPosition = point_n_click_answer_form.answerXCoord.data
        point_answer.yPosition = point_n_click_answer_form.answerYCoord.data
        point_answer.imageFile = ""
        point_answer.dropBoxHeightAdjustment = float(point_n_click_answer_form.answer_area_adjusted_height_ratio.data)
        point_answer.dropBoxWidthAdjustment = float(point_n_click_answer_form.answer_area_adjusted_width_ratio.data)
        point_answer.dropBoxColor = ""
        db.session.add(point_answer)
        db.session.commit()
    if drag_n_drop_image_form.drag_answer_image.data is not None and drag_n_drop_image_form.validate():
        image = request.files['drag_answer_image']
        drag_n_drop_correct = drag_n_drop_image_form.data["correctness"]
        if 'drag_answer_image' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            img_path = os.path.join((app.config['UPLOAD_FOLDER'] + "/" + str(classID)), filename)
            image.save(img_path)
            local_img_path = "/static/img/" + str(classID) + "/" + filename
    if drag_n_drop_form.answerImage.data is not None and drag_n_drop_form.validate():
        drag_answer = Answer()
        drag_answer.questionID = questionID
        drag_answer.correctness = drag_n_drop_form.data["correctness"]
        drag_answer.answerText = ""
        drag_answer.answerReason = drag_n_drop_form.data["answerReason"]
        drag_answer.xPosition = drag_n_drop_form.data["answerXCoord"]
        drag_answer.yPosition = drag_n_drop_form.data["answerYCoord"]
        drag_answer.imageFile = drag_n_drop_form.data["answerImage"]
        drag_answer.dropBoxHeightAdjustment = float(drag_n_drop_form.data["drop_zone_adjusted_height_ratio"])
        drag_answer.dropBoxWidthAdjustment = float(drag_n_drop_form.data["drop_zone_adjusted_width_ratio"])
        drag_answer.dropBoxColor = drag_n_drop_form.data["drop_zone_color"]
        db.session.add(drag_answer)
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s/question/%s' % (classID, chapterID, sectionID, questionID))
    if form_a.answerText.data is not None and form_a.validate():
        print("here")
        one_answer = Answer()
        one_answer.questionID = questionID
        one_answer.correctness = form_a.data["correctness"]
        one_answer.answerText = form_a.data["answerText"]
        one_answer.answerReason = form_a.data["answerReason"]
        print(form_a.data["imageFile"])
        print("here")
        image = request.files["imageFile"]
        print(image)
        print(allowed_file(image.filename))
        if 'imageFile' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            print("Yes")
            filename = secure_filename(image.filename)
            img_path = os.path.join((app.config['UPLOAD_FOLDER'] + "/" + str(classID)), filename)
            image.save(img_path)
            one_answer.imageFile = "/static/img/" + str(classID) + "/" + filename
        db.session.commit()
        db.session.add(one_answer)
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s/question/%s' % (classID, chapterID, sectionID, questionID))
    elif request.method == 'POST':
        pass
    if form_short.answerText3.data is not None and form_short.validate():
        one_answer = Answer()
        one_answer.questionID = questionID
        one_answer.answerText = form_short.data["answerText3"]
        one_answer.correctness = True
        one_answer.answerReason = form_short.data["answerReason"]
        one_answer.imageFile = form_short.data["imageFile"]
        db.session.add(one_answer)
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s/question/%s' % (classID, chapterID, sectionID, questionID))
    elif request.method == 'POST':
        pass
    form_edit = EditAnswer()
    if form_edit.answerText2.data is not None and form_edit.validate():
        answerID = form_edit.data["answerID"]
        one_answer = Answer.query.filter_by(answerID=answerID).first()
        one_answer.answerText = form_edit.data["answerText2"]
        one_answer.answerReason = form_edit.data["answerReason"]
        if not form_a.data["correctness"] == "":
            one_answer.correctness = form_edit.data["correctness"]
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s/question/%s' % (classID, chapterID, sectionID, questionID))
    elif request.method == 'POST':
        pass
    form_short_edit = EditShortAnswer()
    if form_short_edit.answerText4.data is not None and form_short_edit.validate():
        answerID = form_short_edit.data["answerID"]
        one_answer = Answer.query.filter_by(answerID=answerID).first()
        one_answer.answerText = form_short_edit.data["answerText4"]
        one_answer.answerReason = form_short_edit.data["answerReason"]
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s/question/%s' % (classID, chapterID, sectionID, questionID))
    elif request.method == 'POST':
        pass
    form_change = ChangeImage()
    if form_change.imageFile1.data is not None and form_change.validate():
        answerID = form_change.data["questionID"]
        answer_to_change = Answer.query.filter_by(answerID=questionID).first()
        image = request.files["imageFile1"]
        if 'imageFile1' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            img_path = os.path.join((app.config['UPLOAD_FOLDER'] + "/" + str(classID)), filename)
            image.save(img_path)
            answer_to_change.imageFile = "/static/img/" + str(classID) + "/" + filename
        db.session.commit()
        return redirect('/edit-class/%s/%s/%s/question/%s' % (classID, chapterID, sectionID, questionID))

    answers = query_db('SELECT * from Answers where questionID="%s"' % questionID)
    questions = query_db('SELECT questionText from Questions where questionID="%s"' % questionID)[0][0]
    chapterName = query_db('SELECT chapterName from Chapters where chapterID="%s"' % chapterID)[0][0]
    sectionName = query_db('SELECT sectionName from Sections where sectionID="%s"' % sectionID)[0][0]
    className = query_db('SELECT * from Classes where classID="%s"' % classID)[0][0]
    questionType = query_db('SELECT * from Questions where questionID="%s"' % questionID, one=True)[3]
    questionImage = query_db('SELECT * from Questions where questionID="%s"' % questionID, one=True)[5]

    return render_template('pages/edit-question.html', classID=classID, className=className, chapterID=chapterID,
                           chapterName=chapterName, sectionID=sectionID, questions=questions, answers=answers,
                           form_a=form_a, questionID=questionID, sectionName=sectionName, questionType=questionType,
                           questionImage=questionImage, drag_n_drop_form=drag_n_drop_form, form_edit=form_edit,
                           drag_n_drop_image_form=drag_n_drop_image_form, drag_n_drop_answer_image=local_img_path,
                           drag_n_drop_correct=drag_n_drop_correct, point_n_click_answer_form=point_n_click_answer_form,
                           form_change=form_change, form_short_edit=form_short_edit, form_short=form_short)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>/question/<questionID>/delete/<answerID>',
           methods=('GET', 'POST'))
@roles_required('Professor')
def delete_answer(classID, chapterID, sectionID, questionID, answerID):
    answer_to_delete = Answer.query.filter_by(answerID=answerID).first()
    print(answer_to_delete)
    db.session.delete(answer_to_delete)
    db.session.commit()
    return render_template('pages/delete-answer.html', classID=classID, chapterID=chapterID, sectionID=sectionID,
                           questionID=questionID)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>/question/delete/<questionID>', methods=('GET', 'POST'))
@roles_required('Professor')
def delete_question(classID, chapterID, sectionID, questionID):
    question_to_delete = Question.query.filter_by(questionID=questionID).first()
    db.session.delete(question_to_delete)
    db.session.commit()
    return render_template('pages/delete-question.html', classID=classID, chapterID=chapterID, sectionID=sectionID,
                           questionID=questionID)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>/text/<sectionBlockID>/delete', methods=('GET', 'POST'))
@roles_required('Professor')
def delete_section_block(classID, chapterID, sectionID, sectionBlockID):
    section_block_to_delete = SectionBlock.query.filter_by(sectionBlockID=sectionBlockID).first()
    db.session.delete(section_block_to_delete)
    db.session.commit()
    return render_template('pages/delete-section-block.html', classID=classID, chapterID=chapterID, sectionID=sectionID,
                           sectionBlockID=sectionBlockID)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>/text/<sectionBlockID>/delete/<imageFile>',
           methods=('GET', 'POST'))
@roles_required('Professor')
def delete_section_block_image(classID, chapterID, sectionID, sectionBlockID, imageFile):
    imageFile = imageFile.replace("%%", "/")
    print(imageFile)
    section_block_image_to_delete = SectionBlockImages.query.filter_by(sectionBlockID=sectionBlockID).filter_by(
        imageFile=imageFile).first()
    print(section_block_image_to_delete)
    db.session.delete(section_block_image_to_delete)
    db.session.commit()
    return render_template('pages/delete-section-block-image.html', classID=classID, chapterID=chapterID,
                           sectionID=sectionID,
                           sectionBlockID=sectionBlockID, imageFile=imageFile)


@app.route('/professor-home/delete/<classID>/<studentemail>',
           methods=('GET', 'POST'))
@roles_required('Professor')
def delete_student(classID, studentemail):
    student_to_delete = UserClasses.query.filter_by(classID=classID).filter_by(email=studentemail).first()
    db.session.delete(student_to_delete)
    db.session.commit()
    return render_template('pages/delete-student.html', classID=classID)


@app.route('/edit-class/<classID>/<chapterID>/<sectionID>/delete/video/<videoFile>',
           methods=('GET', 'POST'))
@login_required
@roles_required('Professor')
def delete_video(classID, chapterID, sectionID, videoFile):
    videoFile = videoFile.replace("%%%", "/")
    print(sectionID)
    print(videoFile)
    video_to_delete = Video.query.filter_by(sectionID=sectionID).filter_by(videoFile=videoFile).first()
    print(video_to_delete)
    db.session.delete(video_to_delete)
    db.session.commit()
    return render_template('pages/delete-video.html', classID=classID, chapterID=chapterID,
                           sectionID=sectionID, vidoeFile=videoFile)



@app.route('/delete/<classID>', methods=('GET', 'POST'))
@roles_required('Professor')
def delete_class(classID):
    active = School.query.filter_by(schoolID=current_user.schoolID).first()
    if not active.subscription:
        flash(
            "Sorry, the organization you are currently enrolled for is inactive. Please contact pugetsoundhelp@gmail.com for more information")
        return redirect('/professor-home')
    class_to_delete = Class.query.filter_by(classID=classID).first()
    db.session.delete(class_to_delete)
    db.session.commit()
    # find this class' media folder and delete it
    basedir = 'static/img'
    for fn in os.listdir(basedir):
        if fn == str(classID):
            shutil.rmtree((basedir + "/" + str(classID)))
    basedirV = 'static/video'
    for fn in os.listdir(basedirV):
        if fn == str(classID):
            shutil.rmtree((basedirV + "/" + str(classID)))
    return render_template('pages/delete-class.html')


@app.route('/edit-class/<classID>/delete/<chapterID>', methods=('GET', 'POST'))
@roles_required('Professor')
def delete_chapter(classID, chapterID):
    chapter_to_delete = Chapter.query.filter_by(chapterID=chapterID).first()
    db.session.delete(chapter_to_delete)
    db.session.commit()
    return render_template('pages/delete-chapter.html', classID=classID, chapterID=chapterID)


@app.route('/edit-class/<classID>/<chapterID>/delete/<sectionID>', methods=('GET', 'POST'))
@roles_required('Professor')
def delete_section(classID, chapterID, sectionID):
    section_to_delete = Section.query.filter_by(sectionID=sectionID).first()
    db.session.delete(section_to_delete)
    db.session.commit()
    return render_template('pages/delete-section.html', classID=classID, chapterID=chapterID, sectionID=sectionID)


@app.route('/edit-class/<classID>/glossary/delete/<termID>', methods=('GET', 'POST'))
@roles_required('Professor')
def delete_term(classID, termID):
    term_to_delete = Glossary.query.filter_by(termID=termID).first()
    db.session.delete(term_to_delete)
    db.session.commit()
    return render_template('pages/delete-term.html', classID=classID, termID=termID)


@app.route('/edit-class/<classID>/glossary/delete/image/<termID>/<imageFile>', methods=('GET', 'POST'))
@roles_required('Professor')
def delete_term_image(classID, termID, imageFile):
    imageFile = imageFile.replace("%%", "/")
    image_to_delete = GlossaryImages.query.filter_by(termID=termID).filter_by(imageFile=imageFile).first()
    db.session.delete(image_to_delete)
    db.session.commit()
    return render_template('pages/delete-term-image.html', classID=classID, termID=termID)


@app.route('/student-home', methods=('GET', 'POST'))
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
@roles_required(['Professor', 'Student'])
def section_page(class_id, chapter, section):
    prof = False
    if query_db('SELECT role_id from User_roles where user_id = "%s"' % current_user.id)[0][0] == 35:
        prof = True
    if not prof and query_db('SELECT publish from Sections where sectionID="%s"' % section) == [(0,)]:
        flash("Sorry, but the section you have chosen has not been published yet")
        return redirect('/student-class-overview/%s' % class_id)
    if query_db('SELECT * from Enroll where email="%s" AND classID="%s"' % (session["email"], class_id)) != []:
        # Section Text
        text_info = query_db('SELECT * from SectionBlock WHERE sectionID = "%s" ORDER BY orderNo' % section)
        section_text = []
        blockIDs = []

        print("classid")
        print(type(class_id))

        chapter_data = query_db('SELECT * from Chapters where chapterID ="%c"' % chapter, one=True)
        chapter_name = chapter_data[1]
        chapter_order = chapter_data[3]
        for i in text_info:
            blockIDs.append(i[0])

        for x in text_info:
            section_text.append((x[0], x[1]))

        # Section Images
        images_info = []
        idx = 0
        for j in range(len(blockIDs)):
            images_info.append(
                query_db('SELECT * from sectionBlockImages WHERE sectionBlockID = "%s"' % str(blockIDs[idx])))
            idx += 1

        section_images = []

        for y in range(len(blockIDs)):
            if images_info[y]:
                section_images.append((images_info[y][0][0], images_info[y][0][1], images_info[y][0][2]))

        # get video file
        video_files = query_db('SELECT * from Videos WHERE sectionID = "%s" ORDER BY orderNo' % section)
        print(video_files)
        # video = "/static/video/samplevid.mp4"
        # get quiz data
        a_list = []

        # creating a list of questions for the page
        questions = query_db('SELECT * from Questions where sectionID="%s" ORDER BY orderNo' % section)

        # getting rid of the questions that have no answer
        q_list = []
        for q in questions:
            if query_db('SELECT * from Answers where questionID="%s"' % q[0]):
                q_list.append(q)

        # finding all the answers of the questions on the page
        q_image_list = []

        for questions in q_list:
            answer_id = questions[0]
            a_list.append(query_db('SELECT * from Answers where questionID = "{}"'.format(answer_id)))
            # print(query_db('SELECT * from Answers where questionID = "{}"'.format(answer_id))[0][6])
            # print(query_db('SELECT * from Answers where questionID = "{}"'.format(answer_id))[0][7])

        # q_image_list = query_db('SELECT * from QuestionImages')
        print("section " + section)
        section_data = query_db('SELECT * from Sections WHERE sectionID = "%s"' % section, one=True)
        print("Section data below")
        print(section_data)
        section_name = section_data[2]
        section_order = section_data[3]

        section_before = query_db(
            'SELECT * from Sections WHERE chapterID = "%c" AND orderNo="%o"' % (chapter, section_order - 1), one=True)
        if section_before:
            section_id_before = section_before[0]
        else:
            section_id_before = []

        section_after = query_db(
            'SELECT * from Sections WHERE chapterID = "%c" AND orderNo="%o"' % (chapter, section_order + 1), one=True)
        next_ch_sect = []
        chapter_after = []
        section_id_after = []
        if not section_after:
            chapter_after = query_db(
                'SELECT * from Chapters WHERE classID = "%s" AND orderNo = "%o" ' % (class_id, chapter_order + 1),
                one=True)
            if chapter_after:
                chapter_id_after = chapter_after[0]
                next_ch_sect = query_db(
                    'SELECT * from Sections WHERE chapterID = "%s" AND orderNo = 1' % chapter_id_after, one=True)

        this_user_class = UserClasses.query.filter_by(email=current_user.id, classID=class_id).first()
        this_user_class.lastSectionID = section
        db.session.commit()
        prof = False
        if query_db('SELECT role_id from User_roles where user_id = "%s"' % current_user.id)[0][0] == 35:
            prof = True

        return render_template('layouts/section.html', chapter=chapter, section=section, q_list=q_list,
                               a_list=a_list, classID=class_id, chapter_name=chapter_name, section_order=section_order,
                               section_images=section_images, video_files=video_files, section_text=section_text,
                               section_name=section_name, section_id_before=section_id_before,
                               next_ch_sect=next_ch_sect, prof=prof,
                               chapter_after=chapter_after, section_after=section_after)
    else:
        flash("Please enroll in a class before navigating to it.")
        return redirect(home_url)


@app.route('/forgot', methods=('GET', 'POST'))
def forgot():
    form = ForgotForm(request.form)
    if form.validate_on_submit():
        email = str(form.data['email'])
        user_object = query_db('SELECT * from Users WHERE email="%s"' % email, one=True)
        if user_object is None:
            flash("Unable to find user with those details, please try again")
            # return render_template('forms/login.html', form=form)
            return redirect("/login")
        else:
            token = get_user_token(email)
            print(token)
            html_body = render_template('email/reset_password.html', token=token)
            html = MIMEText(html_body, 'html')
            print(html)
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = email
            msg["Subject"] = "Reset Password"
            msg.attach(html)
            smtpObj.sendmail(sender, msg["To"], msg.as_string())
            successurl = home_url + "forgot-success"
            return redirect(successurl)
            # except :
    return render_template('forms/forgotPassword.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = verify_reset_password_token(token)
    print(token)
    if user == -1:
        return redirect(home_url)
    else:
        form = ResetPasswordForm(request.form)
        if form.validate_on_submit():
            password = form.data['password']
            h = hashlib.md5(password.encode())
            hashvalue = h.hexdigest()
            user_object = User.query.filter_by(email=user).first()
            user_object.password = hashvalue
            db.session.add(user_object)
            db.session.commit()
            return redirect(home_url)
        return render_template('forms/reset_password.html', form=form)


@app.route('/forgot-success')
def forgotSuccess():
    return render_template('forms/forgotSuccess.html')


@app.route('/professor-home', methods=('GET', 'POST'))
@roles_required('Professor')
def professor_home():
    prof_join_class_form = ProfJoinClass()
    form_create = CreateClass()
    formEdit = EditClass()
    share_class_with_canvas_form = ShareClassWithCanvas()
    active = School.query.filter_by(schoolID=current_user.schoolID).first()
    if not active.subscription and (share_class_with_canvas_form.validate() or prof_join_class_form.validate() or form_create.validate_on_submit() or formEdit.validate_on_submit()):
        flash("Sorry, the organization you are currently enrolled for is inactive. Please contact pugetsoundhelp@gmail.com for more information")
        return redirect('/professor-home')

    if share_class_with_canvas_form.canvasClassCode is not None and share_class_with_canvas_form.validate():
        print("validated share form")

    if prof_join_class_form.classCode is not None and prof_join_class_form.validate():
        one_class = Class.query.filter_by(classID=prof_join_class_form.classCode.data).one()
        current_user.classes.append(one_class)
        db.session.commit()
    if form_create.validate_on_submit() and query_db(
            'SELECT * from Classes where classID="%s"' % form_create.data["class_id"]) == []:
        one_class = Class()
        one_class.classID = form_create.data["class_id"]
        one_class.className = form_create.data["class_name"]
        current_user.classes.append(one_class)
        db.session.add(one_class)
        db.session.commit()
        # create a folder for this class' images to live in
        # this helps us avoid naming conflicts with images and videos
        path = "static/img/" + str(form_create.data["class_id"])
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)
        pathV = "static/video/" + str(form_create.data["class_id"])
        try:
            os.mkdir(pathV)
        except OSError:
            print("Creation of the directory %s failed" % pathV)
        else:
            print("Successfully created the directory %s " % pathV)
        return redirect(url_for('professor_home'))
    elif request.method == 'POST' and not formEdit.validate_on_submit():
        flash("We're sorry but a class already exists with that code, please enter another unique code")
        pass
    if formEdit.newClassID.data is not None and formEdit.validate_on_submit() and query_db('SELECT * from Classes where classID="%s"' % formEdit.newClassID.data) == []:
        classID = formEdit.data["classID"]
        if query_db('SELECT * from Classes where classID="%s"' % formEdit.newClassID.data) == [] or classID == formEdit.newClassID.data:
            Class.query.filter_by(classID=classID).update(dict(classID=formEdit.newClassID.data, className=formEdit.data["className"]))
            UserClasses.query.filter_by(classID=classID).update(dict(classID=formEdit.newClassID.data))
            Chapter.query.filter_by(classID=classID).update(dict(classID=formEdit.newClassID.data))
            db.session.commit()

        # want to rename this class' image folder here
        basedir = 'static/img'
        for fn in os.listdir(basedir):
            if fn == formEdit.data["classID"]:
                os.rename(os.path.join(basedir, fn), os.path.join(basedir, str(formEdit.newClassID.data)))
        basedirV = 'static/video'
        for fn in os.listdir(basedirV):
            if fn == formEdit.data["classID"]:
                os.rename(os.path.join(basedirV, fn), os.path.join(basedirV, str(formEdit.newClassID.data)))
        return redirect('/professor-home')
    elif formEdit.newClassID.data is not None and formEdit.validate_on_submit() and not query_db('SELECT * from Classes where classID="%s"' % formEdit.newClassID.data) == []:
        flash("We're sorry but a class already exists with that code, please enter another unique code")
        classID = formEdit.data["classID"]
        Class.query.filter_by(classID=classID).update(dict(className=formEdit.data["className"]))
        db.session.commit()
        return redirect('/professor-home')
    elif request.method == 'POST':
        pass
    # render our classes
    classes_list = []
    for _class in current_user.classes:
        # we want to use the class code to get a class name from classes
        _class = query_db('SELECT * from Classes WHERE classID="%s"' % _class.classID, one=True)
        class_tuple = (_class[0], _class[1], len(query_db('SELECT * from Enroll WHERE classID="%s"' % _class[1]))-1)
        classes_list.append(class_tuple)
    admin = False
    if current_user.schoolID == "3141592653589admin":
        admin = True

    return render_template('pages/professor-home.html', name=current_user.name, classes=classes_list, form=form_create,
                           formEdit=formEdit, prof_join_class_form=prof_join_class_form,
                           share_with_canvas_form=share_class_with_canvas_form, admin=admin)


@app.route('/professor-home/<classID>/students', methods=('GET', 'POST'))
@roles_required('Professor')
def view_students(classID):
    students = query_db('SELECT * from Enroll WHERE classID="%s"' % classID)
    className = query_db('SELECT * FROM Classes where classID="%s"' % classID)[0][0]
    users = query_db('SELECT * FROM Users')
    list = []
    for user in users:
        for student in students:
            if user[0] == student[0]:
                list.append((student[0], student[2], user[2]))
    return render_template('pages/view-students.html', classID=classID, list=list, className=className)


@app.route('/administrator', methods=('GET', 'POST'))
@roles_required('Professor')
def admin():
    form = AddSchool()
    form_subscription = Subscription()
    if form.schoolID.data is not None and not form.schoolID.data == "" and form_subscription.validate() and query_db('SELECT * from School where schoolID="%s"' % form.data["schoolID"]) == []:
        one_school = School()
        one_school.schoolID = form.data["schoolID"]
        one_school.schoolName = form.data["schoolName"]
        one_school.subscription = True
        db.session.add(one_school)
        db.session.commit()
        return redirect('/administrator')
    elif request.method == 'POST':
        pass
    if not form_subscription.schoolID1.data == "" and form_subscription.validate() and not form.validate():
        schoolID = form_subscription.data["schoolID1"]
        one_school = School.query.filter_by(schoolID=schoolID).first()
        one_school.subscription = not one_school.subscription
        db.session.commit()
        return redirect('/administrator')
    elif request.method == 'POST':
        pass

    schools = query_db('SELECT * from School')
    classes = query_db('SELECT * from Classes')
    users = query_db('SELECT * from Users')

    return render_template('pages/administrator.html', name=current_user.name, form=form, schools=schools, users=len(users),
                           classes=len(classes), form_subscription=form_subscription)


@app.route('/administrator/<schoolID>/delete', methods=('GET', 'POST'))
@roles_required('Professor')
def delete_school(schoolID):
    school_to_delete = School.query.filter_by(schoolID=schoolID).first()
    db.session.delete(school_to_delete)
    db.session.commit()
    return render_template('pages/delete-school.html', schoolID=schoolID)


@app.route('/edit-student-profile', methods=('GET', 'POST'))
@roles_required('Student')
def edit_student_profile():
    form_password = ProfilePassword()
    current_school = School.query.filter_by(schoolID=current_user.schoolID).first()
    if form_password.validate():
        password = form_password.data["oldpassword"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        # check passhash against the database
        user_object = query_db('SELECT * from Users WHERE email="%s" AND password="%s"' % (current_user.id, passhash), one=True)
        if user_object is None:
            flash("Unable to find user with those details, please try again")
            return redirect('/edit-student-profile')
        else:
            user = User.query.filter_by(id=current_user.id).one()
            newpassword = form_password.data["password"]
            h = hashlib.md5(newpassword.encode())
            passhash = h.hexdigest()
            user.password = passhash
            db.session.commit()
            login_user(user)
            return redirect('/edit-student-profile')
    return render_template('pages/edit-student-profile.html', current_user=current_user,
                           form_password=form_password, current_school=current_school)


@app.route('/edit-profile', methods=('GET', 'POST'))
@roles_required('Professor')
def edit_profile():
    form = EditProfessorRegForm()
    form_school = ProfileSchool()
    form_password = ProfilePassword()
    current_school = School.query.filter_by(schoolID=current_user.schoolID).first()
    if form.validate():
        current_user.name = form.data["fullName"]
        db.session.commit()
        return redirect('/edit-profile')
    if form_school.validate():
        if School.query.filter_by(schoolID=form_school.data["code"]).first() is not None:
            current_user.schoolID = form_school.data["code"]
            db.session.commit()
            return redirect('/edit-profile')
        else:
            flash("Unable to find school with those details, please try again")
            return redirect('/edit-profile')
        return redirect('/edit-profile')
    if form_password.validate():
        password = form_password.data["oldpassword"]
        h = hashlib.md5(password.encode())
        passhash = h.hexdigest()
        # check passhash against the database
        user_object = query_db('SELECT * from Users WHERE email="%s" AND password="%s"' % (current_user.id, passhash), one=True)
        if user_object is None:
            flash("Unable to find user with those details, please try again")
            return redirect('/edit-profile')
        else:
            user = User.query.filter_by(id=current_user.id).one()
            newpassword = form_password.data["password"]
            h = hashlib.md5(newpassword.encode())
            passhash = h.hexdigest()
            user.password = passhash
            db.session.commit()
            login_user(user)
            return redirect('/edit-profile')
    return render_template('pages/edit-profile.html', current_user=current_user, form=form, form_school=form_school,
                           form_password=form_password, current_school=current_school)


@app.route('/student-short')
def student_short():
    return render_template('pages/placeholder.student.short.html')


@app.route('/glossary/<classID>')
@roles_required(['Student', 'Professor'])
def glossaryTemplate(classID):
    db_gloss = query_db('SELECT * from Glossary WHERE classID="{}" ORDER BY term'.format(classID))
    db_class_name = query_db('SELECT className from Classes WHERE classID="{}"'.format(classID), one=True)

    class_name = db_class_name[0]
    ids = []
    terms = []
    defs = []
    images = []

    for x in db_gloss:
        ids.append(x[1])
        terms.append((x[2]))
        defs.append(x[3])

    #for y in range(len(ids)):
    #    print("thinks it should get another glossary image from the db")
    #    temp = query_db('SELECT * from GlossaryImages WHERE termID = "%s"' % str(ids[y]))
    #    if temp != []:
    #        images.append(temp)
    for this_id in ids:
        images.append(query_db('SELECT * from GlossaryImages WHERE termID = "%s"' % this_id))

    alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
             "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    termsAlpha = sorted(terms)
    defsAlpha = []
    idsAlpha = []

    for idx, t in enumerate(termsAlpha):
        defsAlpha.append("")
        defsAlpha[idx] = defs[terms.index(t)]
        idsAlpha.append("")
        idsAlpha[idx] = ids[terms.index(t)]
        idx += 1

    gloss = []
    for i in range(len(terms)):
        gloss.append((idsAlpha[i], termsAlpha[i], defsAlpha[i]))

    presentAlpha = []
    for _letter in alpha:
        for _term in termsAlpha:
            if _term[0] == _letter:
                presentAlpha.append(_letter)
                break

    return render_template('layouts/glossary-template.html', classID=classID, gloss=gloss,
                           enumerate=enumerate, alpha=presentAlpha, class_name=class_name, images=images)


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
        print(user_object)
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
    return render_template('forms/login.html', form=form, noNav=True)


@app.route('/new-professor-account', methods=['GET', 'POST'])
def new_prof_acc():
    form = ProfessorRegForm()
    if form.validate_on_submit():
        user_object = query_db('select * from Users where email= ?', [form.data["email"]], one=True)
        # this lets us verify that the professor is actually working at a particular school before they make an account
        school_code = query_db('select * from School where schoolID= ?', [form.data["schoolProfCode"]], one=True)
        print(school_code)
        if not school_code[2]:
            flash("Sorry, the organization is currently inactive. Please contact pugetsoundhelp@gmail.com for more information")
            return render_template('forms/NewProfAccount.html', form=form)
        if user_object is None and school_code is not None:
            password = form.data["password"]
            h = hashlib.md5(password.encode())
            passhash = h.hexdigest()
            user = User(id=form.data["email"], email=form.data["email"], name=form.data["fullName"], active=True,
                        password=passhash)
            user.schoolID = school_code[0]
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
    organizations = query_db('SELECT schoolID, schoolName FROM School')
    choices = [('', 'Select your Organization'), ('N/A', 'Other')]
    for organization in organizations:
        if not organization[0] == "3141592653589admin":
            choices.append(organization)

    form.organization.choices = choices
    if form.validate_on_submit():
        # check that we don't already have this user registered
        user_object = query_db('select * from Users where email= ? ', [form.data["email"]], one=True)
        # insert them into the db
        if user_object is None:
            password = form.data["password"]
            h = hashlib.md5(password.encode())
            passhash = h.hexdigest()
            user = User(
                id=form.data["email"], email=form.data["email"], name=form.data["fullName"], schoolID=form.data["organization"], active=True,
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
@roles_required('Professor')
def professor_class_home(classID):
    print("called professor class home")
    # get chapters in order like we should
    chapters = query_db('SELECT * from Chapters where classID="%s" ORDER by "orderNo"' % classID)
    print(chapters)
    # 2d array of sections, also in order like they should be
    sections_arrays = []
    for chapter in chapters:
        sections_arrays.append(query_db('SELECT * from Sections where chapterID="%s" ORDER by "orderNo" ' % chapter[0]))

    # 3d array of questions, ordered by orderNo
    questions = []
    for sectionarray in sections_arrays:
        for section in sectionarray:
            questions.append(query_db('SELECT * from Questions where sectionID="%s" ORDER by "orderNo" ' % section[0]))
    print(sections_arrays)
    print(questions)
    # 3d array of answers
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
@roles_required('Student')
def student_class_home(classID):
    chapters = query_db('SELECT * from Chapters where classID="%s" ORDER by "orderNo"' % classID)
    sections_arrays = []
    for chapter in chapters:
        sections_arrays.append(query_db('SELECT * from Sections where chapterID="%s" ORDER by "orderNo"' % chapter[0]))
    # questions = []
    # for sectionarray in sections_arrays:
    #    for section in sectionarray:
    #        questions.append(query_db('SELECT * from Questions where sectionID="%s"' % section[0]))
    # answers = []
    # for question_array in questions:
    #    for question in question_array:
    #        answers.append(query_db('SELECT * from Answers where questionID="%s"' % question[0]))
    class_name = query_db('SELECT * from Classes where classID="%s"' % classID)[0][0]
    last_section_ID = \
        query_db("SELECT * from Enroll where email='%s' AND classID='%s'" % (current_user.id, classID), one=True)[2]
    if last_section_ID is None:
        # this means that we have yet to start this class
        # we want to default to the first section in the first chapter of this class
        first_chapter_ID = \
            query_db("SELECT * from Chapters where classID='%s' AND orderNo='%s'" % (classID, 1), one=True)[0]
        first_section_ID = \
            query_db("SELECT * from Sections where chapterID='%s' AND orderNo='%s'" % (first_chapter_ID, 1), one=True)[
                0]
        last_section_ID = first_section_ID
        last_chapter_ID = first_chapter_ID
    else:
        last_chapter_ID = query_db("SELECT * from Sections where sectionID='%s'" % last_section_ID, one=True)[1]
    print(last_chapter_ID)
    return render_template('pages/student_class_overview.html', chapters=chapters, sections=sections_arrays,
                           class_name=class_name, classID=classID, last_chapter_ID=last_chapter_ID,
                           last_section_ID=last_section_ID)

@app.route("/tutorial")
@roles_required(['Student', 'Professor'])
def tutorial():
    return render_template('layouts/main-tutorial.html')

@app.route("/about-the-developers")
@roles_required(['Student', 'Professor'])
def developers():
    return render_template('/layouts/about-the-devs.html')


@app.route("/logout")
@roles_required(['Student', 'Professor'])
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

# Default port: want to switch this
if __name__ == '__main__':
    #app.secret_key = 'xxxxyyyyyzzzzz'
    app.run(threaded=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
