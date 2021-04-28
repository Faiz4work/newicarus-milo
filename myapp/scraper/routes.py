from flask import Blueprint, url_for, render_template, request
from numpy import source
from myapp import db
from myapp.models import Jobs


scraper = Blueprint('scraper', __name__)

@scraper.route('/company')
def company():
    source = set([i.source for i in Jobs.query.all()])
    return render_template('scraper/companies.html', source=source)

@scraper.route('/company_jobs')
def company_jobs():
    source = request.args.get('source')
    results = Jobs.query.filter_by(source=source).all()
    return render_template("main/results.html", jobs=results,
                            length=len(results), keywords=source)