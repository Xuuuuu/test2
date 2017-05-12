# # -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import  Length, EqualTo,DataRequired
from wtforms import ValidationError
from modles import User
#
#
#
class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message='用户名不可为空'), Length(3, 9)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='用户名不可为空')])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('注册')

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')
#
#
# # class PasswordResetRequestForm(form):
# #     email = StringField('Email', validators=[Required(), Length(1, 64),
# #                                              Email()])
# #     submit = SubmitField('Reset Password')
# #
# #
# # class PasswordResetForm(form):
# #     username = StringField('username', validators=[Required(), Length(1, 64),
# #                                              Email()])
# #     password = PasswordField('New Password', validators=[
# #         Required(), EqualTo('password2', message='Passwords must match')])
# #     password2 = PasswordField('Confirm password', validators=[Required()])
# #     submit = SubmitField('Reset Password')
#
#     # def validate_email(self, field):
#     #     if User.query.filter_by(email=field.data).first() is None:
#     #         raise ValidationError('Unknown email address.')
#
#
#
#
