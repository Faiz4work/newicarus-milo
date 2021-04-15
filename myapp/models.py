from myapp import db
from datetime import datetime
from myapp import login_manager
from flask_login import UserMixin
    
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

class Users(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String,
                         nullable=False,
                         unique=False)
    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         unique=False,
                         nullable=False)

    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    date_created = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return f"{self.username}"


class Jobs(db.Model):
    __tablename__ = 'Jobs'

    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False, unique=False)
    city = db.Column(db.String(60), nullable=False, unique=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    company_name = db.Column(db.String(50), nullable=True, unique=False)
    company_website = db.Column(db.String(150), nullable=True, unique=False)
    source = db.Column(db.String(30),nullable=True, unique=False)
    sector_information = db.Column(db.String(50),nullable=True, unique=False)
    job_type = db.Column(db.String(30),nullable=True, unique=False)
    job_location = db.Column(db.String(60),nullable=True, unique=False)
    job_url = db.Column(db.String(300),nullable=True, unique=False)
    salary = db.Column(db.String(50), nullable=True, unique=False)
    description = db.Column(db.String(1000), nullable=True, unique=False)

    def __repr__(self):
        return f"{self.job_title}, {self.job_location}"

class ipAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(30), nullable=False, unique=False)
    