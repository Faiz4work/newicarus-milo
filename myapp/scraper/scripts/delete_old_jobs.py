from datetime import datetime


def delete_jobs(jb):
    jobs_age = 30
    for job in jb.query.all():
        old_date = job.date_posted
        today = datetime.now()

        days = today - old_date
        print(days)