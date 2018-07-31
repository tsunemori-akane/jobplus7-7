import os
import json
from random import randint
from faker import Faker
from jobplus.models import db, User, Company, Job

fake = Faker('zh-cn')

'''
def json_process():
    result = []
    data = json.load(open('scripts/datas/job_company.json'))
    for item in data:
        if not item['company-name'] in result:
            result.append(item)
    return result
'''
with open(os.path.join(os.path.dirname(__file__), 'datas', 'job_company.json')) as f:
    all_datas = json.load(f)

def iter_users():
    for i in all_datas:
        yield User(
            username = i['company-name'],
            email = fake.email(),
            password = fake.password(),
            role = User.ROLE_COMPANY
        )

l = list(iter_users())

def iter_companies():
    for (x, y) in zip(l, list(all_datas)):
        yield Company(
            user = x,
            logo = y['company-logo'],
            staff_num = y['company_size'],
            industry = y['industry'],
            address = y['company_address']
        )

def iter_jobs():
    for n in range(randint(0, 47)):
        i = list(all_datas)[n]
        yield Job(
            name =i['post'],
            salary = i['salary'],
            location = i['location'],
            tags = i['about-position'],
            qualifications = i['qualifications']
        )

def run():
    for user in l:
       db.session.add(user)
    '''
    for company in iter_companies():
        db.session.add(company)
    for job in iter_jobs():
        db.session.add(job)
    '''
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
