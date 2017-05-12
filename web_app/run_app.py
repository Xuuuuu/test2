# -*- coding:utf-8 -*-
from flask import Flask,Blueprint
from modles import db,lm,job_info,wh

from admin import admin
from user import user
from auth import auth





# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__,template_folder='templates',static_folder='static')
#数据库配置
app.config['SECRET_KEY'] = 'haha'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/test2?charset=utf8' #这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True #设置这一项是每次请求结束后都会自动提交数据库中的变动
# app.config['WHOOSH_BASE'] = './whoosh_index'
#flask蓝图
app.register_blueprint(user)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(auth,url_prefix='/auth')



# bootstrap = Bootstrap(app)
#数据库实例化

db.init_app(app)
wh.init_app(app)

# db.create_all()

#登录
lm.session_protection = 'strong'
lm.login_view = 'auth.login'
lm.init_app(app)


if __name__ == '__main__':
    app.run('127.0.0.1',4000)
