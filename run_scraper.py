import sys
import subprocess
import os
import pandas as pd
from myapp.models import Jobs
from myapp import db, create_app
from datetime import datetime

pythonanywhere = False
jobs_age = 30

# functions
def runSpider(script_path, result_path):
    process = subprocess.Popen(['scrapy', 'runspider', '{}'.format(script_path),
                                '-o', '{}'.format(result_path)])
    process.wait()


# e.g python run_scraper indeed_uk.py
spider_name = sys.argv[1]

if 'delete_old_jobs' == spider_name:
    mapp = create_app()
    mapp.app_context().push()
    for job in Jobs.query.all():
        old_date = job.date_posted
        today = datetime.now()

        time = today - old_date
        if time.days >= jobs_age:
            db.session.delete(job)



if 'simply_uk.py' == spider_name:
    if pythonanywhere:
        spider_path = '/home/newicarus/mysite/myapp/myapp/scraper/scripts/simplyhired/simply_uk.py'
        results_path = '/home/newicarus/mysite/myapp/myapp/scraper/results/simplyhired/simply_uk_results.csv'
    else:
        spider_path = 'myapp\\scraper\\scripts\\simplyhired\\simply_uk.py'
        results_path = 'myapp\\scraper\\results\\simplyhired\\simply_uk_results.csv'
        # spider_exists = os.path.exists(simply_uk_script)

    runSpider(spider_path, results_path)


    # pushing app context
    mapp = create_app()
    mapp.app_context().push()
    # Adding data to database
    data = pd.read_csv(results_path)
    for d in data.index:
        title = data['Title'][d]
        company_name = data['Company Name'][d]
        company_website = 'Not Available'
        city = data['City'][d]
        location = data['Company Location'][d]
        job_type = data['Job Type'][d]
        company_job_link = data['Job Link'][d]
        source = 'simplyhired.co.uk'

        has_old = Jobs.query.filter_by(job_title=title, source=source).first()
        if has_old:
            db.session.delete(has_old)

        job = Jobs(job_title=title, city=city, date_posted=datetime.now(), 
                   company_name=company_name, company_website=company_website,
                   source=source, sector_information='', job_type=job_type,
                   job_location=location, job_url=company_job_link)
        db.session.add(job)
    db.session.commit()

    # removing previous file
    os.remove(results_path)

if 'simply_usa.py' == spider_name:
    if pythonanywhere:
        spider_path = '/home/newicarus/mysite/myapp/myapp/scraper/scripts/simplyhired/simply_usa.py'
        results_path = '/home/newicarus/mysite/myapp/myapp/scraper/results/simplyhired/simply_usa_results.csv'
    else:
        spider_path = 'myapp\\scraper\\scripts\\simplyhired\\simply_usa.py'
        results_path = 'myapp\\scraper\\results\\simplyhired\\simply_usa_results.csv'
        # spider_exists = os.path.exists(simply_uk_script)

    runSpider(spider_path, results_path)


    # pushing app context
    mapp = create_app()
    mapp.app_context().push()
    # Adding data to database
    data = pd.read_csv(results_path)
    for d in data.index:
        title = data['Title'][d]
        company_name = data['Company Name'][d]
        company_website = 'Not Available'
        city = data['City'][d]
        location = data['Company Location'][d]
        job_type = data['Job Type'][d]
        company_job_link = data['Job Link'][d]
        source = 'www.simplyhired.com'

        has_old = Jobs.query.filter_by(job_title=title, source=source).first()
        if has_old:
            db.session.delete(has_old)

        job = Jobs(job_title=title, city=city, date_posted=datetime.now(), 
                   company_name=company_name, company_website=company_website,
                   source=source, sector_information='', job_type=job_type,
                   job_location=location, job_url=company_job_link)
        db.session.add(job)
    db.session.commit()

    # removing previous file
    os.remove(results_path)

if 'efinancial_uk.py' == spider_name:
    if pythonanywhere:
        spider_path = '/home/newicarus/mysite/myapp/myapp/scraper/scripts/efinancial_careers/efinancial_uk.py'
        results_path = '/home/newicarus/mysite/myapp/myapp/scraper/results/efinancial_careers/efinancial_uk_results.csv'
    else:
        spider_path = 'myapp\\scraper\\scripts\\efinancial_careers\\efinancial_uk.py'
        results_path = 'myapp\\scraper\\results\\efinancial_careers\\efinancial_uk_results.csv'

    runSpider(spider_path, results_path)


    # pushing app context
    mapp = create_app()
    mapp.app_context().push()
    # Adding data to database
    data = pd.read_csv(results_path)
    for d in data.index:
        title = data['Title'][d]
        company_name = data['Company Name'][d]
        company_website = 'Not Available'
        city = data['City'][d]
        location = data['Location'][d]
        job_type = data['Job Type'][d]
        company_job_link = data['Job Link'][d]
        salary = data['Salary'][d]
        description = data['Description'][d]
        source = 'efinancialcareers.co.uk'

        has_old = Jobs.query.filter_by(job_title=title, source=source).first()
        if has_old:
            db.session.delete(has_old)


        job = Jobs(job_title=title, city=city, date_posted=datetime.now(), 
                   company_name=company_name, company_website=company_website,
                   source=source, sector_information='', job_type=job_type,
                   job_location=location, job_url=company_job_link,
                   description=description, salary=salary)
        db.session.add(job)
    db.session.commit()

    # removing previous file
    os.remove(results_path)


# if 'indeed_uk.py' == spider_name:
    # if pythonanywhere:
    #     spider_path = '/home/newicarus/mysite/myapp/myapp/scraper/scripts/indeed/indeed_uk.py'
    #     results_path = '/home/newicarus/mysite/myapp/myapp/scraper/results/indeed/indeed_uk_results.csv'
    # else:
    #     spider_path = 'myapp\\scraper\\scripts\\indeed\\indeed_uk.py'
    #     results_path = 'myapp\\scraper\\results\\indeed\\indeed_uk_results.csv'

    # runSpider(spider_path, results_path)

    # # pushing app context
    # mapp = create_app()
    # mapp.app_context().push()
    # # Adding data to database
    # data = pd.read_csv(results_path)
    # for d in data.index:
    #     title = data['Title'][d]
    #     company_name = data['Company Name'][d]
    #     company_website = data['Company Job link'][d]
    #     city = data['City'][d]
    #     location = data['Company Location'][d]
    #     job_type = data['Job Type'][d]
    #     company_job_link = data['Job link'][d]
    #     salary = data['Salary'][d]
    #     description = ''


    #     job = Jobs(job_title=title, city=city, date_posted=datetime.now(), 
    #                company_name=company_name, company_website=company_website,
    #                source='uk.indeed.com', sector_information='', job_type=job_type,
    #                job_location=location, job_url=company_job_link,
    #                description=description, salary=salary)
    #     db.session.add(job)
    # db.session.commit()

    # # removing previous file
    # os.remove(results_path)


if 'reed.py' == spider_name:
    if pythonanywhere:
        spider_path = '/home/newicarus/mysite/myapp/myapp/scraper/scripts/reed/reed.py'
        results_path = '/home/newicarus/mysite/myapp/myapp/scraper/results/reed/reed_results.csv'
    else:
        spider_path = 'myapp\\scraper\\scripts\\reed\\reed.py'
        results_path = 'myapp\\scraper\\results\\reed\\reed_results.csv'

    runSpider(spider_path, results_path)

    # pushing app context
    mapp = create_app()
    mapp.app_context().push()
    # Adding data to database
    data = pd.read_csv(results_path)
    for d in data.index:
        title = data['Title'][d]
        company_name = data['Company Name'][d]
        city = data['City'][d]
        location = data['Company Location'][d]
        job_type = data['Job Type'][d]
        company_job_link = data['Job Link'][d]
        salary = data['Salary'][d]
        description = ''
        source='reed.co.uk'

        has_old = Jobs.query.filter_by(job_title=title, source=source).first()
        if has_old:
            db.session.delete(has_old)

        job = Jobs(job_title=title, city=city, date_posted=datetime.now(), 
                   company_name=company_name, company_website='',
                   source=source, sector_information='', job_type=job_type,
                   job_location=location, job_url=company_job_link,
                   description=description, salary=salary)
        db.session.add(job)
    db.session.commit()

    # removing previous file
    os.remove(results_path)

if 'totaljobs.py' == spider_name:
    if pythonanywhere:
        spider_path = '/home/newicarus/mysite/myapp/myapp/scraper/scripts/totaljobs/totaljobs2.py'
        results_path = '/home/newicarus/mysite/myapp/myapp/scraper/results/totaljobs/totaljobs_results.csv'
    else:
        spider_path = 'myapp\\scraper\\scripts\\totaljobs\\totaljobs2.py'
        results_path = 'myapp\\scraper\\results\\totaljobs\\totaljobs_results.csv'

    # runSpider(spider_path, results_path)
    python spider_path

    # pushing app context
    mapp = create_app()
    mapp.app_context().push()
    # Adding data to database
    data = pd.read_csv(results_path)
    for d in data.index:
        title = data['Title'][d]
        company_name = data['Company Name'][d]
        city = data['City'][d]
        location = data['Company Location'][d]
        job_type = data['Job Type'][d]
        company_job_link = data['Job Link'][d]
        salary = data['Salary'][d]
        description = ''
        source='totaljobs.com'

        has_old = Jobs.query.filter_by(job_title=title, source=source).first()
        if has_old:
            db.session.delete(has_old)

        job = Jobs(job_title=title, city=city, date_posted=datetime.now(), 
                   company_name=company_name, company_website='',
                   source=source, sector_information='', job_type=job_type,
                   job_location=location, job_url=company_job_link,
                   description=description, salary=salary)
        db.session.add(job)
    db.session.commit()

    # removing previous file
    os.remove(results_path)
