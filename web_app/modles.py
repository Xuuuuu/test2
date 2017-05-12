# -*- coding:utf-8 -*-
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemyplus as whooshalchemy
from jieba.analyse import ChineseAnalyzer
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

wh = whooshalchemy
lm = LoginManager()
db = SQLAlchemy()



class role(UserMixin,db.Model):
    __tablename__ = 'role'
    id = db.Column(db.String(45), primary_key=True)
    admin = db.Column(db.String(255))
    user = db.Column(db.String(255))
    admin_role = db.relationship('admin_role',\
                                 backref='admin_role',lazy = 'dynamic')
    user_role = db.relationship('user_role',\
                                backref='user_role',lazy ='dynamic')




    def __init__(self,admin,):



class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    admin = db.Column(db.String(45), db.ForeignKey('role.admin'))
    user = db.Column(db.String(45), db.ForeignKey('role.user'))

    admin_role = db.relationship('User',
        back_populates='user_info')

    user_info = db.relationship(
        'User_info',
        backref='user_info',
        lazy = 'dynamic')
    job_hire = db.relationship(
        'Job_hire',
        backref='job_hire',
        lazy = 'dynamic')
    posts = db.relationship(
        'Post',
        backref='users',
        lazy='dynamic')
    comments = db.relationship(
        'Comment',
        backref='comments',
        lazy='dynamic')

    def __init__(self, username, password):
        self.id = str(uuid4())
        self.username = username
        self.password = self.set_password(password)

    def set_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return (self.id).encode()

    def __repr__(self):
        """Define the string format for instance of User."""
        return " `{}`".format(self.username)

@lm.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class Post(db.Model):
    """Represents Proected posts."""
    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    desc = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
    # Establish contact with Comment's ForeignKey: post_id
    comments = db.relationship(
        'Comment',
        backref='posts',
        lazy='dynamic')
    user = db.relationship(
        'User',
        back_populates='posts')




     # many to many: posts <==> tags
    # tags = db.relationship(
    #     'Tag',
    #     secondary=posts_tags,
    #     backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title,text,publish_date,desc,user_id):
        self.id=uuid4()
        self.text = text
        self.title = title
        self.desc = desc
        self.publish_date = publish_date
        self.user_id = user_id

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)


class Comment(db.Model):
    """Represents Proected comments."""

    __tablename__ = 'comments'
    id = db.Column(db.String(45), primary_key=True)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))

    # one to many: user <==> posts
    user = db.relationship(
        'User',
        back_populates='comments')

    def __init__(self, text,date_time,post_id,user_id):
        self.id = str(uuid4())
        self.text = text
        self.date = date_time
        self.post_id = post_id
        self.user_id = user_id

    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.id)


class User_info(db.Model):

    __tablename__ = 'user_info'

    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.Text())
    email = db.Column(db.String(45))
    phone = db.Column(db.String(45))

    ethn = db.Column(db.String(45))
    location = db.Column(db.String(255))
    education = db.Column(db.String(255))

    about_me = db.Column(db.Text())

    school = db.Column(db.String(255))
    school_text = db.Column(db.Text())

    company = db.Column(db.String(255))
    company_text = db.Column(db.Text())


    info_id = db.Column(db.String(45), db.ForeignKey('users.id'))

    info = db.relationship(
        'User',
        back_populates='user_info')

    def __init__(self, name,email,phone,ethn,location,education,about_me,school
                 ,school_text,company,company_text,info_id):
        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.ethn = ethn
        self.location = location
        self.education = education
        self.about_me = about_me
        self.school = school
        self.school_text = school_text
        self.company = company
        self.company_text = company_text
        self.info_id = info_id

    def __repr__(self):
        return '<Model id `{}`>'.format(self.info_id)



class job_info(db.Model):

    __tablename__ = 'job_info'
    __searchable__ = ['city','companyName','positionName']
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.String(45), primary_key=True)
    companyName    =db.Column(db.String(45))
    industryField  = db.Column(db.String(45))
    positionName   = db.Column(db.String(45))
    jobNature      = db.Column(db.String(45))
    createTime     = db.Column(db.String(255))
    education      = db.Column(db.String(255))
    financeStage  = db.Column(db.String(45))
    companyLabelList = db.Column(db.String(255))
    companySize = db.Column(db.String(45))
    city = db.Column(db.String(255))
    district = db.Column(db.String(45))
    positionType = db.Column(db.String(45))
    positionAdvantage = db.Column(db.String(45))
    Salary = db.Column(db.String(45))
    salaryMax = db.Column(db.Integer())
    salaryMin = db.Column(db.Integer())
    salaryAvg = db.Column(db.Integer())
    workYear = db.Column(db.String(45))

    jobinfo = db.relationship(
        'Job_hire',
        backref='jobinfo',
        lazy = 'dynamic')


    def __init__(self,companyName,industryField,positionName,jobNature,createTime,financeStage,\
                          companyLabelList,companySize,city,district,positionType,education,\
                          positionAdvantage,Salary,salaryMax,salaryMin,salaryAvg,workYear):
        self.id = str(uuid4())
        self.companyName = companyName
        self.industryField =industryField
        self.positionName =positionName
        self.jobNature = jobNature
        self.createTime = createTime
        self.financeStage = financeStage
        self.companyLabelList = companyLabelList
        self.companySize = companySize
        self.city = city
        self.district = district
        self.positionType = positionType
        self.education = education
        self.positionAdvantage = positionAdvantage
        self.Salary = Salary
        self.salaryMax = salaryMax
        self.salaryMin = salaryMin
        self.salaryAvg =salaryAvg
        self.workYear = workYear

    def __repr__(self):
        return '<Model job_info `{}`>'.format(self.id)



class Job_hire(db.Model):
    __tablename__ = 'job_hire'
    id = db.Column(db.String(45), primary_key=True)
    companyName    =db.Column(db.String(45))
    positionName   = db.Column(db.String(45))
    createTime     = db.Column(db.String(255))
    usr_id = db.Column(db.String(45), db.ForeignKey('users.id'))
    jobs_id = db.Column(db.String(45), db.ForeignKey('job_info.id'))
    usr = db.relationship(
        'User',
        back_populates ='job_hire')

    jobs = db.relationship(
        'job_info',
        back_populates ='jobinfo')



    def __init__(self, usr_id,jobs_id,companyName,positionName,createTime):
        self.id=uuid4()
        self.usr_id = usr_id
        self.jobs_id = jobs_id
        self.companyName = companyName
        self.positionName = positionName
        self.createTime = createTime

    def __repr__(self):
        return "<Model job_hire `{}`>".format(self.id)

