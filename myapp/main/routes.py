from flask import Blueprint, render_template, request, send_from_directory, current_app
from myapp.models import Jobs
from flask_login import login_required
import os
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/main')
def layout():
    return render_template ("layout.html")

@main.route('/')
def home():
    jobs = len(Jobs.query.all())
    return render_template ("main/home.html", jobs=jobs)

@main.route('/job_details/<int:id>')
@login_required
def job_details(id):
    job = Jobs.query.get(id)
    return render_template ("main/job_details.html", job=job)

@main.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    if request.method == 'POST':
        jobs = request.form.getlist('csv_jobs')
        mypath = 'myapp\\static\\myjobs.csv'
        if os.path.exists(mypath): os.remove(mypath)
        myjobs = list(map(lambda _id: Jobs.query.get(_id), jobs))

        results = pd.DataFrame(columns=['Title', 'City', 'Date', 'Company Name',
                                'Salary', 'Company Website', 'Source', 
                                'Job Type', 'Location', 'Job Link'])
        for job in myjobs:
            results = results.append(
                {
                    'Title': job.job_title,
                    'City' : job.city,
                    'Date' : job.date_posted,
                    'Company Name' : job.company_name,
                    'Salary' : job.salary,
                    'Company Website' : job.company_website,
                    'Source' : job.source,
                    'Job Type' : job.job_type,
                    'Location' : job.job_location,
                    'Job Link' : job.job_url,
                }, ignore_index=True)

        results.to_csv(mypath, index=False)
        # return f"Success"
        return send_from_directory(current_app.static_folder, filename='myjobs.csv', as_attachment=True)
    if request.method == 'GET':
        query = request.args.get('query').split()
        location = request.args.get('location')
        results = []
        for q in query:
            search = f"%{q}%"
            que = Jobs.query.filter(Jobs.job_title.like(search)).filter \
                            (Jobs.job_location.like(f"%{location}%")).all()
            for i in que:
                results.append(i)
        keywords = ' '.join(query)
        return render_template("main/results.html", jobs=results,
                                length=len(results), keywords=keywords)

@main.route('/csv', methods=["POST"])
@login_required
def csv_jobs():
    jobs = request.form.getlist('csv_jobs')
    mypath = 'myjobs.csv'
    if os.path.exists(mypath): os.remove(mypath)
    myjobs = list(map(lambda _id: Jobs.query.get(_id), jobs))

    results = pd.DataFrame(columns=['Title', 'City', 'Date', 'Company Name',
                            'Salary', 'Company Website', 'Source', 
                            'Job Type', 'Location', 'Job Link'])
    for job in myjobs:
        results = results.append(
            {
                'Title': job.job_title,
                'City' : job.city,
                'Date' : job.date_posted,
                'Company Name' : job.company_name,
                'Salary' : job.salary,
                'Company Website' : job.company_website,
                'Source' : job.source,
                'Job Type' : job.job_type,
                'Location' : job.job_location,
                'Job Link' : job.job_url,
            }, ignore_index=True)

    results.to_csv(mypath, index=False)
    return send_from_directory('', filename=mypath, as_attachment=True)


    
    