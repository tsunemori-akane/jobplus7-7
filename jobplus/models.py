from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()

class Base(db.Model):
    # 不把这个类当作Model类
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY= 20
    ROLE_ADMIN = 30

    # id, username, password, email, role, phone 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    phone = db.Column(db.Integer, unique=True, index=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    company = db.relationship('Company', uselist=False)


    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class Resume():
    __tablename__ = 'resume'

    # id, degree, job, work_year, resume 

    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(32), index=True, nullable=False)
    job = db.Column(db.String(64), index=True, nullable=False)
    work_year = db.Column(db.SmallInteger, index=True, nullable=False)
    resume = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', uselist=False)

    def __repr__(self):
        return '<Resume:{}>'.format(self.id)
        

class Company(Base):
    __tablename__ = 'company'

    # id, name, jobs, address, website, logo, description

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    description = db.Column(db.String(128))
    logo = db.Column(db.String(128))
    website = db.Column(db.String(128), unique=True)
    address = db.Column(db.String(128), nullable=False)
    jobs = db.relationship('Job', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', uselist=False)

    def __repr__(self):
        return '<Company:{}>'.format(self.name)


class Job(Base):
    __tablename__ = 'job'

    #id, name, tags, description

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    description = db.Column(db.String(128))
    degree = db.Column(db.String(32), index=True, nullable=False)
    work_year = db.Column(db.SmallInteger)
    tags = db.Column(db.String(128), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    company = db.relationship('Company', uselist=False)

    def __repr__(self):
        return '<Job:{}>'.format(self.name)
