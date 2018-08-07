import os
import json
import re
from faker import Faker
from random import randint
from jobplus.models import db, User, Job, Resume, Company


fake = Faker()

path = os.path.join(os.path.dirname(__file__), '..', 'datas', 'job.json')
faker_data = json.load(open(path))


LENGTH = len(faker_data)


def fake_companies():
    for i in range(0, LENGTH):
        company = faker_data[i]

        db_company = User.query.filter_by(username=company['name']).first()

        if db_company:
            continue

        c = User(
            username = company['name'],        
            email = 'shiyanlou_' + str(i) + '@qq.com',
            role = 20
        )

        c.password = '123123'

        try:
            db.session.add(c)
        except:
            db.session.rollback()
            continue

        user = User.query.filter_by(email=c.email).first_or_404()

        welfare = ",".join(company['welfare'])

        d = Company(
            name = company['name'],
            logo = company['logo'],
            address = company['address'].split('：')[1],
            city = company['city'],
            staff_num = company['size'].split('：')[1],
            welfare = welfare, 
            industry = company['industry'],
            user_id = user.id
        )

        db.session.add(d)
        db.session.commit()


def fake_jobs():
    companies = Company.query.all()

    for i in range(len(companies)):


        job = Job(
            name = faker_data[i]['job'], 
            salary = faker_data[i]['salary'], 
            work_year = faker_data[i]['work_year'], 
            degree = faker_data[i]['degree'], 
            company_id = companies[i].id 
        )

        db.session.add(job)
        db.session.commit()


def run():
    fake_companies()
    fake_jobs()
