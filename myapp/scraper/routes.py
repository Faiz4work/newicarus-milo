from flask import Blueprint, url_for, render_template
from myapp import db
import pandas as pd
from datetime import datetime
from myapp.models import Jobs, ipAddress
from subprocess import Popen
import os

scraper = Blueprint('scraper', __name__)

@scraper.route('/test')
def test():
    return render_template('test.html')
# @scraper.route('/scrape_ips')
# def scrape_ip():
#     db.session.query(ipAddress).delete()
#     db.session.commit()
#     if os.path.exists('ip_addresses.csv'):
#         os.remove('ip_addresses.csv')
#     path = os.getcwd() + '\\myapp\\scraper\\utils\\ip_scraper.py'
#     pro = Popen(['scrapy', 'runspider', path, '-o', 'ip_addresses.csv'])
#     pro.wait()
#     data = pd.read_csv('ip_addresses.csv')['ip']
#     for i in data:
#         ipad = ipAddress(ip= 'http://' + i)
#         db.session.add(ipad)
#     db.session.commit()
#     return f"{data}"
