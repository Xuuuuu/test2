# # -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,  SelectField,\
    SubmitField,DateField
from wtforms.validators import Required, Length, Email, Regexp,DataRequired
from wtforms import ValidationError
from modles import User

class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    desc = StringField('Desc',validators=[DataRequired()])
    text = TextAreaField('Content',validators= [DataRequired()])

class EditProfileForm(FlaskForm):

    name = StringField('姓名', validators=[Length(0, 64)])
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    phone =StringField('联系方式', validators=[Length(11)])


    ethn = StringField('民族', validators=[Length(0, 64)])
    location = StringField('地理位置', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    education = StringField('学历', validators=[Length(0, 64)])

    school = StringField('学校', validators=[Length(0, 64)])
    school_text = TextAreaField('教育经历')

    company = StringField('公司', validators=[Length(0, 64)])
    company_text = TextAreaField('工作经验')





