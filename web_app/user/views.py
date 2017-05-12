# -*- coding:utf-8 -*-
from flask import Flask,render_template,send_file, redirect, url_for, abort, flash, request,\
    current_app, session
from flask_login import login_required, current_user
from .forms import CommentForm,EditProfileForm,PostForm
from user import user
from modles import Post,Comment,User,db,User_info,job_info,Job_hire
from datetime import datetime


@user.route('/', methods = ['GET', 'POST'])
@user.route('/index',methods = ['GET', 'POST'])
@user.route('/index/<int:page>', methods = ['GET', 'POST'])
def index(page = 1):
    jobinfo = job_info.query.paginate(page, 10,False)
    if request.method == 'POST':
        keyword = request.form['keyword']
        jobinfo= jobinfo.query.whoosh_search(keyword).paginate(page, 10,False)
    return render_template('index.html',jobinfo=jobinfo )




@user.route('/hire_job/<string:job_id>',methods = ('GET', 'POST'))
@login_required
def hire_job(job_id):
    info =job_info.query.filter_by(id=job_id).first()
    if request.method == 'POST':
        jobId = request.form['job_id']
        usr_id = session['user_id']
        companyName = request.form['companyName']
        positionName =request.form['positionName']
        createTime = request.form['createTime']
        jobs_insert = Job_hire(usr_id=usr_id,jobs_id=jobId,companyName=companyName,\
                               positionName=positionName,createTime=createTime)
        test_info = Job_hire.query.filter_by(usr_id=usr_id,jobs_id=jobId).first()
        if test_info is not None:
            return redirect(url_for('user.hire_job',info=info,job_id=jobId))
        db.session.add(jobs_insert)
        db.session.commit()
        return redirect(url_for('user.index'))
    return render_template('hire_job.html',info=info,job_id=job_id )




@user.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@user.route('/work')
def work():
    return render_template('work.html')

@user.route('/post')
@user.route('/post/<int:page>')
@login_required
def post(page = 1):
    if current_user :
        posts = Post.query.order_by(
            Post.publish_date.desc()
        ).paginate(page, 10)
        # print(posts.items)
        recent = db.session.query(Post).order_by(
            Post.publish_date.desc()
        ).limit(5).all()
        return render_template('about.html',posts = posts,recent=recent)
    else:
        return redirect(url_for('au'))


@user.route('/post_doc/<string:post_id>', methods=('GET', 'POST'))
@login_required
def post_doc(post_id):
    form = CommentForm()
    user_id = session['user_id']
    print(user_id)

    if request.method == 'POST':
        post = Post.query.get_or_404(post_id) #查询当前页的内容
        comment_text = form.body.data
        date_time = datetime.now()
        user_id = session['user_id']
        new_comment = Comment(text=comment_text,date_time=date_time,post_id=post_id,user_id=user_id)
        db.session.add(new_comment)
        db.session.commit()

    post = Post.query.get_or_404(post_id) #查询当前页的内容
    comments = post.comments.order_by(Comment.date.desc()).all()#获取当前页的评论
    recent = db.session.query(Post).order_by(
        Post.publish_date.desc()
    ).limit(5).all()

    return render_template('post_doc.html', post=post,comments=comments,
                           recent=recent,postid=post.id,form=form)


@user.route('/user_profile/<string:username>',)
@login_required
def user_profile(username):
    user_id = session['user_id']
    print(user_id)
    # user_data = User.query.filter_by(username=username).first_or_404()
    # posts = user_data.posts.order_by(Post.publish_date.desc()).all()
    info =User_info.query.filter_by(info_id=user_id).first()
    recent = db.session.query(Post).order_by(
            Post.publish_date.desc()
        ).limit(5).all()

    return render_template('user_profile.html',
                           user=user, recent=recent,info=info)

@user.route('/edit_post', methods=('GET', 'POST'))
@login_required
def edit_post():
    username = current_user.username
    user_data = User.query.filter_by(username=username).first_or_404()
    posts = user_data.posts.order_by(Post.publish_date.desc()).paginate(1, 10)

    if request.method == 'POST':
        post_id = request.form['post_id']
        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
        return redirect(url_for('user.edit_post',posts=posts))

    return render_template('user_profile_post.html',posts=posts)

@user.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    user_id = session['user_id']
    info =User_info.query.filter_by(info_id=user_id).first()
    if request.method == 'POST':
        name = form.name.data
        email= form.email.data
        phone= form.phone.data
        ethn = form.ethn.data
        location = form.location.data
        education = form.education.data
        about_me= form.about_me.data
        school = form.school.data
        school_text = form.school_text.data
        company = form.company.data
        company_text = form.company_text.data

        info_id = session['user_id']
        info = User_info.query.filter_by(info_id=user_id).first()
        print(info)
        if info is None:
            usr_info = User_info(name=name,email=email,phone=phone,
                                 ethn=ethn,location=location,education=education,
                                 about_me=about_me,school=school,school_text=school_text,
                                 company=company,company_text=company_text,info_id=info_id)
            print(usr_info)
            db.session.add(usr_info)
            db.session.commit()
            return redirect(url_for('user.user_profile',username=current_user.username))
        else:
            user_id = session['user_id']
            info =User_info.query.filter_by(info_id=user_id).first_or_404()
            info_new = {}
            info_new['name'] = name
            info_new['email'] = email
            info_new['phone'] = form.phone.data
            info_new['ethn'] = ethn
            info_new['location'] = location
            info_new['education'] = education
            info_new['about_me'] = about_me
            info_new['school'] =school
            info_new['school_text'] = school_text
            info_new['company'] = company
            info_new['company_text'] = company_text
            form.school_text.data = info.school_text
            db.session.query(User_info).update(info_new)
            db.session.commit()
            print(info_new)
            print(current_user.username)
            return redirect(url_for('user.user_profile',username=current_user.username))

    return render_template('user_profile_info.html',forms=form,info=info)

@user.route('/new', methods=('GET', 'POST'))
def new_post():
    forms = PostForm()
    post_id = session['user_id']
    post_data =Post.query.filter_by(id=post_id).first()

    if request.method == 'POST':
        title = forms.title.data
        desc = forms.desc.data
        text = forms.text.data
        pub_time = datetime.now()

        post_id = session['user_id']
        post_data =Post.query.filter_by(id=post_id).first()
        print(post_data)
        if post_data is None:
            posts = Post(title=title,desc=desc,text=text,publish_date=pub_time,user_id=post_id)
            db.session.add(posts)
            db.session.commit()
            return redirect(url_for('user.edit_post'))
        else:
            new_post = {}
            new_post['title'] = title
            new_post['desc'] = desc
            new_post['publish_date'] = pub_time
            new_post['text'] = text
            new_post['user_id'] = post_id
            db.session.query(Post).update(new_post)
            db.session.commit()
            return redirect(url_for('user.edit_post'))
    return render_template('new_post.html',foms=forms,posts=post_data)

@user.route('/edit/<post_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def edit(post_id):
    forms = PostForm()
    post = Post.query.get_or_404(post_id) #查询当前页的内容
    if request.method == 'post':
        title = forms.title.data
        desc = forms.desc.data
        text = forms.text.data
        new_post = {}
        new_post['title'] = title
        new_post['desc'] = desc
        new_post['text'] = text
        db.session.query(Post).update(new_post)
        db.session.commit()
        return redirect(url_for('user.edit_post'))
    return render_template('edit_post.html',posts=post,forms=forms,post_id=post_id)

@user.route('/user_job_hire',methods = ('GET', 'POST'))
@login_required
def user_job_hire():
    username = current_user.username
    user_data = User.query.filter_by(username=username).first_or_404()
    job_data = user_data.job_hire.paginate(1, 30)
    if request.method == 'POST':
        jobId = request.form['job_id']
        print(jobId)
        Job_hire.query.filter_by(id=jobId).delete()
        db.session.commit()
        return redirect(url_for('user.user_job_hire',data=job_data))
    return render_template('user_job_hire.html',data=job_data)

@user.route('/show_user_profile/<string:id>',methods = ('GET', 'POST'))
@login_required
def show_user_profile(id):
    user_data = User.query.filter_by(id=id).first_or_404()
    posts = user_data.posts.order_by(Post.publish_date.desc()).paginate(1, 20)

    info =User_info.query.filter_by(info_id=id).first()
    job_data = user_data.job_hire.paginate(1, 30)
    return render_template('show_user_profile.html',post_data = posts,userInfo=info,job_data=job_data,user_data=user_data)
