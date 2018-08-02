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
            password = '123456',
            role = User.ROLE_COMPANY
        )
lt = list(iter_users())

def iter_companies():
    for m in lt:
        for n in all_datas:    
            if n['company-name']==m['username']:
                yield Company(
                    user = m,
                    name = n['company-name'],
                    logo = n['company-logo'],
                    staff_num = n['company_size'],
                    industry = n['industry'],
                    address = n['company_address']
                )

def iter_jobs():
    for company in Company.query:
        for i in all_datas():
            yield Job(
                company = company,
                name =i['post'],
                salary = i['salary'],
                location = i['location'],
                tags = i['about-position'],
                qualifications = i['qualifications']
            )

def run():
    for user in l:
       db.session.add(user)
    
    for company in iter_companies():
        db.session.add(company)
    for job in iter_jobs():
        db.session.add(job)
    
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
