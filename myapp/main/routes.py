from flask import Blueprint, render_template, request
from myapp.models import Jobs
from flask_login import login_required


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

@main.route('/results')
@login_required
def results():
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
