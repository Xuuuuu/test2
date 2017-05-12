#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import render_template,redirect,request,url_for,session
from modles import db,Post,User,User_info,job_info,Comment,Job_hire
from flask_login import login_required,current_user
from .port_scan import port_main
import platform
import psutil
from .ip_scan import pingt,trace_route
from admin import admin
import os
from admin.lagou.https import Http
from admin.lagou.parse import Parse
from admin.lagou.setting import headers as hd
from admin.lagou.setting import cookies as ck
from admin.python_pandas import practical_city,practical_poistion,global_education,global_experience,\
    company_financeStage,company_positiontype,company_size,city_experience_salary,city_education_num,\
    city_salary,city_education_salary,city_experience_num,hotjob_hotsalary_fivecity,hotjob_salary
import csv
import logging




logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='diary.log',
                    filemode='a')


def getInfo(url, para):
    """
    获取信息
    """
    generalHttp = Http()
    htmlCode = generalHttp.post(url, para=para, headers=hd, cookies=ck)
    generalParse = Parse(htmlCode)
    pageCount = generalParse.parsePage()
    info = []
    for i in range(1, 30):
        print('第%s页' % i)
        para['pn'] = str(i)
        htmlCode = generalHttp.post(url, para=para, headers=hd, cookies=ck)
        generalParse = Parse(htmlCode)
        info = info + getInfoDetail(generalParse)
        # time.sleep(2)
    return info


def getInfoDetail(generalParse):
    """
    信息解析
    """
    info = generalParse.parseInfo()
    return info


def processInfo(info, para):
    """
    信息存储
    """
    logging.error('Process start')
    try:
        csvFile = open("../web_app/admin/jobInfo.csv", 'wt', encoding = 'utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(( 'companyName','industryField','positionName','jobNature','createTime','financeStage',\
                          'companyLabelList','companySize','city','district','positionType','education',\
                          'positionAdvantage','Salary','salaryMax','salaryMin','salaryAvg','workYear'))

        # file = open('test.txt', 'a')
        # file.write(title)
        for p in info:
            Salary = p['positionSalary']
            Salary = Salary.split('-')
            if len(Salary) == 1:
                salaryMax = int(Salary[0][:Salary[0].find('k')])
            else:
                 salaryMax = int(Salary[1][:Salary[1].find('k')])

            salaryMin = int(Salary[0][:Salary[0].find('k')])
            salaryAvg = (salaryMax + salaryMin) / 2
            writer.writerow(( str(p['companyName']) ,str(p['industryField']) ,str(p['positionName']),str(p['jobNature']),\
                              str(p['createTime']),str(p['companyStage']) , str(p['companyLabelList']),str(p['companySize']) ,\
                              str(p['city']) , str(p['district']) , str(p['positionType']),str(p['positionEducation']), \
                              str(p['positionAdvantage']) ,str(p['positionSalary']) ,salaryMax,salaryMin,salaryAvg,\
                              str(p['positionWorkYear'])))
            infos = job_info(companyName= str(p['companyName']) ,industryField=str(p['industryField']) ,positionName=str(p['positionName']),\
                                     jobNature=str(p['jobNature']),createTime= str(p['createTime']),financeStage=str(p['companyStage']) , \
                                     companyLabelList=str(p['companyLabelList']),companySize=str(p['companySize']) , city=str(p['city']) , \
                                     district=str(p['district']) , positionType=str(p['positionType']),education=str(p['positionEducation']),\
                                     positionAdvantage=str(p['positionAdvantage']) ,Salary=str(p['positionSalary']) ,salaryMax=salaryMax,\
                                     salaryMin=salaryMin,salaryAvg=salaryAvg, workYear=str(p['positionWorkYear']))
            db.session.add(infos)
        db.session.commit()

        csvFile.close()
        return True
    except:
        logging.error('Process except')
        return None


def lagou_main(url, para):
    """
    主函数逻辑
    """
    logging.error('Main start')
    if url:
        info = getInfo(url, para)             # 获取信息
        flag = processInfo(info, para)             # 信息储存
        return flag
    else:
        return None










@admin.route('/',methods=['GET','POST'])
@admin.route('/index',methods=['GET','POST'])
@login_required
def index():
    if current_user.username !='admin':
        return redirect(url_for('user.index'))

    user_num = User.query.count()
    comment_num = Comment.query.count()
    post_num = Post.query.count()
    job_num = job_info.query.count()
    hire_num = Job_hire.query.count()
    info_num = User_info.query.count()

    if request.method == 'POST':
        action_name = request.form['action']
        print(action_name)
        if action_name == 'scrapy':
            url = 'https://www.lagou.com/jobs/positionAjax.json?'
            para = {'first': 'true','pn': '1'}
            result = job_info.query.first()
            print(result)
            if result is None:
                flag = lagou_main(url, para)
                if flag: print('爬取成功' )
                else: print('爬取失败' )
                db.session.close()
            else:
                for info in job_info.query.all():
                    db.session.delete(info)
                for info in Job_hire.query.all():
                    db.session.delete(info)
                flag = lagou_main(url, para)
                if flag:
                    print('爬取成功' )
                else:
                    print('爬取失败' )
                db.session.close()
        else:
            practical_city()
            practical_poistion()
            global_education()
            global_experience()
            company_financeStage()
            company_positiontype()
            company_size()
            city_experience_salary()
            city_education_num()
            city_salary()
            city_education_salary()
            city_experience_num()
            hotjob_hotsalary_fivecity()
            hotjob_salary()
    return render_template('admin/index.html',usr_num=user_num,comment_num=comment_num,post_num=post_num,\
                           job_num = job_num ,hire_num=hire_num,info_num=info_num)

@admin.route('/user_profile',methods=['GET','POST'])
@login_required
def user_profile():
    if current_user.username !='admin':
        return redirect(url_for('user.index'))

    user_job_data = Job_hire.query.all()
    if request.method == 'POST':
        info_id = request.form['info_id']
        User_info.query.filter_by(id=info_id).delete()
        db.session.commit()
        return redirect(url_for('admin.user_profile',data=user_job_data))
    return render_template('admin/user_profile.html',data=user_job_data)


@admin.route('/product',methods=['GET','POST'])
@login_required
def product():
    if current_user.username !='admin':
        return redirect(url_for('user.index'))
    val1 = ''
    val2 = ''
    val3 = ''
    val4 = ''
    val5 = ''
    server = port_main()
    if request.method == 'GET':
        if 80 in server:
            val1 = 1
        else:
            val1 = 0
        print(val1)

        if 21 in server:
            val2 = 1
        else:
            val2 = 0
        print(val2)

        if 53 in server:
            val3 = 1
        else:
            val3 = 0
            print(val3)
        if 22 in server:
            val4 = 1
        else:
            val4 = 0
        print(val4)

        if 10 in server:
            val5 = 1
        else:
            val5 = 0
        print(val5)
    if request.method =='POST':
        text = request.form['text']
        os.system(text)
        print(text)
        server2 = port_main()
        if 80 in server2:
            val1 = 1
        else:
            val1 = 0
        print(val1)

        if 20 in server2:
            val2 = 1
        else:
            val2 = 0
        print(val2)

        if  53 in server2:
            val3 = 1
        else:
            val3 = 0
            print(val3)
        if 22 in server2:
            val4 = 1
        else:
            val4 = 0
        print(val4)

        if  110 in server2:
            val5 = 1
        else:
            val5 = 0
        print(val5)
        return redirect(url_for('admin.product',var1 =val1,var2=val2,var3=val3,var4=val4,var5=val5))
    return render_template('admin/product.html',var1 =val1,var2=val2,var3=val3,var4=val4,var5=val5,)


@admin.route('/actions',methods=['GET','POST'])
@login_required
def actions():
    if current_user.username !='admin':
        return redirect(url_for('user.index'))

    var1 = ''
    var2= ''
    if request.method == 'POST':
        if request.form['text1']:
            network = request.form['text1']
            print(network)
            var1 = pingt(network)
            print(var1)
            return render_template('admin/actions.html',var2=var1,var3=var2)
        if request.form['text2']:
            ipaddr = request.form['text2']
            print(ipaddr)
            var2 = trace_route(ipaddr)
            print(var2)
            return render_template('admin/actions.html',var2=var1,var3=var2)
    return render_template('admin/actions.html',var2=var1,var3=var2)


@admin.route('/commnet_edit',methods=['GET','POST'])
@login_required
def commnet_edit():
    if current_user.username !='admin':
        return redirect(url_for('user.index'))
    commnent_data = Comment.query.all()
    if request.method == 'POST':
        info_id = request.form['info_id']
        Comment.query.filter_by(id=info_id).delete()
        db.session.commit()
        return redirect(url_for('admin.commnet_edit',data=commnent_data))
    return render_template('admin/commnet_edit.html',data = commnent_data)


@admin.route('/edit_posts_doc',methods=['GET','POST'])
@login_required
def edit_posts_doc():
    if current_user.username !='admin':
        return redirect(url_for('user.index'))
    info_data = Post.query.all()
    if request.method == 'POST':
        data_id = request.form['data_id']
        print(data_id)
        Post.query.filter_by(id=data_id).delete()
        db.session.commit()
        return redirect(url_for('admin.edit_posts_doc',data=info_data))

    return render_template('admin/edit_posts_doc.html',data=info_data)

@admin.route('/deploy',methods=['GET','POST'])
@login_required
def deploy():
    if current_user.username !='admin':
        return redirect(url_for('user.index'))

    #system
    val_ver = platform.platform()               #获取操作系统名称及版本号
    val_sys = platform.architecture()               #获取操作系统的位数
    val_machine = platform.machine()                   #计算机类型
    val_node = platform.node()                      #计算机的网络名称，'hongjie-PC'
    #CPU
    cpu_info = psutil.cpu_times()                  #显示cpu的整个信息
    cpu_count = psutil.cpu_count()                  #获取cpu的逻辑个数
    cpu_count_true =psutil.cpu_count( logical=False )# 获取cpu的物理个数
    cpu_per = psutil.cpu_percent()                   #cpushiyonglv
    #Memery
    mem = psutil.virtual_memory()                   #获取内存的完整信息
    memtotal = mem.total                            #获取内存总数
    mem_free = mem.free                             #获取空闲的内存信息
    mem_use = mem.used                              #获取使用内存
    mem_per = mem.percent                           #检测内存使用的比例
    #Disk
    disk_all=psutil.disk_partitions()                        #获取磁盘的完整信息
    disk_info = psutil.disk_usage('/')                          #获取/分区的状态
    #use_time
    import  datetime
    psutil.boot_time()                              #以linux时间格式返回,获取开机时间
    use_time = datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H: %M: %S") #转换成自然时间格式

    return render_template('admin/deploy.html',var_ver=val_ver,var_sys=val_sys,ver_machine=val_machine,ver_node=val_node,
                           cpuinfo=cpu_info,cpucount=cpu_count,cpucounttrue=cpu_count_true,cpuper=cpu_per,memtot=memtotal,memper=mem_per,
                           memfree=mem_free,memuse=mem_use,diskall=disk_all,diskinfo=disk_info,usetime=use_time)

@admin.route('/device',methods=['GET','POST'])
@login_required
def device():
    if current_user.username !='admin':
        return redirect(url_for('user.index'))

    return render_template('admin/device.html')

@admin.route('/user_edit',methods = ['GET','POST'])
@login_required
def user_edit():
    if current_user.username !='admin':
        return redirect(url_for('user.index'))

    user_data = User_info.query.all()
    if request.method == 'POST':
        info_id = request.form['info_id']
        User_info.query.filter_by(id=info_id).delete()
        db.session.commit()
        return redirect(url_for('admin.user_edit',data=user_data))
    return render_template('admin/user_edit.html',data = user_data)


