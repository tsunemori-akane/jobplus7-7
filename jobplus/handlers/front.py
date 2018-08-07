from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from jobplus.models import Job, User, Company
from jobplus.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required

front = Blueprint('front', __name__) 

@front.route('/')
def index():
    '''
    page = request.args.get('page', default=1, type=int)
    jobs = Job.query.paginate(
            page=page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False
            )
    companies = Company.query.paginate(
            page=page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False
            )
    return render_template('index.html', jobs=jobs, companies=companies, active='index')
    '''
    jobs = Job.query.filter_by(is_disable=False).limit(9).all()
    return render_template('index.html', jobs=jobs)

@front.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        if user.role == User.ROLE_COMPANY:
            return redirect(url_for('company.profile'))
        elif user.role == User.ROLE_ADMIN:
            return redirect(url_for('admin.users'))
        else:
            return redirect(url_for('user.profile'))
    return render_template('login.html', form=form)

@front.route('/user-register', methods=['GET','POST'])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('Register Success', 'success')
        return redirect(url_for('.login'))
    return render_template('user_register.html', form=form)

@front.route('/corp-register', methods=['GET','POST'])
def corpregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('Register Success', 'success')
        return redirect(url_for('.login'))
    return render_template('corp_register.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('log off', 'success')
    return redirect(url_for('.index'))

