from flask_wtf import FlaskForm
from flask_login import login_required, current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Length, Email, EqualTo, Required
from jobplus.models import db, User, Resume, Company

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('REMEMBER ME')
    submit = SubmitField('LOGIN TO THE SITE')
    
    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('The email is not registered')
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('Incorrect Password')


class RegisterForm(FlaskForm):
    name = StringField('Nickname', validators=[Required(), Length(3, 24)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6,24)])
    confirm_password = PasswordField('Confirm Password', validators=[Required(), EqualTo('password')])
    submit = SubmitField('SEND')


    def validate_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The name has already existed')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email has already existed')
    def create_user(self):
        user = User()
        user.username = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def create_company(self):
        user = User()
        user.username = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.role = User.ROLE_COMPANY 
        db.session.add(user)
        db.session.commit()
        return user
    

class UserProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Required(), Length(2, 24)])
    phone = StringField('电话')
    work_year = StringField('工作年限') 
    degree = StringField('学历') 
    resume_url = StringField('简历') 
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ['13', '15', '18'] or len(phone) != 11:
            raise ValidationError('请输入有效的手机号码')

    def update_resume(self, user):
        if user.resume:
            resume = user.resume
        else:
            resume = Resume()
            resume.user_id = user.id

        self.populate_obj(resume)
        db.session.add(resume)
        db.session.commit()


class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称', validators=[Required(), Length(2, 24)])
    phone = StringField('电话')
    description = StringField('一句话描述') 
    logo = StringField('Logo') 
    website = StringField('网站') 
    city = StringField('城市') 
    address = StringField('公司地址') 
    submit = SubmitField('提交')


    def validate_phone(self, field):
        if field.data:
            phone = field.data
            if phone[:2] not in ['13', '15', '18'] or len(phone) != 11:
                raise ValidationError('请输入有效的手机号码')
    def validate_name(self, f):
        c = Company.query.filter_by(name=f.data).first()
        if c and c != current_user.company:
            raise ValidationError('该公司名已经存在')

    def update_company(self, user):
        if user.company:
            company = user.company
        else:
            company = Company()
            company.user_id = user.id 

        self.populate_obj(company)
        db.session.add(company)
        db.session.commit()
