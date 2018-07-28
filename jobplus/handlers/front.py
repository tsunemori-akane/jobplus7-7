from flask import Blueprint, render_template, url_for, flash, redirect
from jobplus.models import Job, User
from jobplus.forms import LoginForm, RegisterForm
from flask_login import login_user

front = Blueprint('front', __name__) 

@front.route('/')
def index():
    return render_template('index.html')

@front.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route('/user-register', methods=['GET','POST'])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('Register Success', 'success')
        return redirect(url_for('.login'))
    return render_template('user_register.html', form=form)

@front.route('/corp-register')
def corpregister():
    return render_template('corp_register.html')

