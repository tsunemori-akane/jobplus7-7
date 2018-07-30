import os
import json
import re
import random
from faker import Faker
from jobplus.models import db, User, Company, Job

fake = Faker()

path = os.path.join(os.path.dirname(__file__), '..', 'datas', 'liepin.json')
faker_data = json.load(open(path))

LENGTH = len(faker_data)



def fake_companies():
    for i in range(LENGTH):

        company = faker_data[i] 

        c = User(
            username = company['name'],
            email = 'shiyanlou@qq.com',
            role = 20 
        )
        c.password = '123123'

        db.session.add(c)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            continue
        
        d = Company(
            name = company['name'],
            logo = company['logo'],
            user_id = c.id
        )
        db.session.add(d)
        db.session.commit()

def fake_jobs():
    companies = Company.query.all()

    for i in range(LENGTH):
        company = random.choice(companies)

        work_year = re.findall('\d+', faker_data[i]['work_year'])

        job = Job(
            name = faker_data[i]['job'],
            salary = faker_data[i]['salary'],
            work_year = work_year[0], 
            degree = faker_data[i]['degree'], 
            company = company 
        )

        job.company_id = company.id
        db.session.add(job)
        db.session.commit()


def run():
    fake_companies()
    fake_jobs()

