from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Length, Email, EqualTo, Required
from wtforms import ValidationError
from jobplus.models import db, User

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


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username has already existed')
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
