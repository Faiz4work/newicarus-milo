import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from parsel import Selector
from time import sleep
from datetime import datetime

urls = {'london' : 'https://www.totaljobs.com/jobs/in-london',
            'north east' : 'https://www.totaljobs.com/jobs/in-north-east',
            'west midlands' : 'https://www.totaljobs.com/jobs/in-west-midlands',
            'wales' : 'https://www.totaljobs.com/jobs/in-wales',
            'yorkshire' : 'https://www.totaljobs.com/jobs/in-yorkshire',
            'east midlands' : 'https://www.totaljobs.com/jobs/in-east-midlands',
            'east anglia' : 'https://www.totaljobs.com/jobs/in-east-anglia',
            'ireland' : 'https://www.totaljobs.com/jobs/in-republic-of-ireland',
            'south west' : 'https://www.totaljobs.com/jobs/in-south-west',
            'south east' : 'https://www.totaljobs.com/jobs/in-south-east',
            'north west' : 'https://www.totaljobs.com/jobs/in-north-west',
            'northern ireland' : 'https://www.totaljobs.com/jobs/in-northern-ireland',
            'scotland' : 'https://www.totaljobs.com/jobs/in-scotland',
            }

driver = webdriver.Firefox(executable_path='C:\\driver\\geckodriver.exe')
# driver.delete_all_cookies()

cookie_clicked = False
for city, url in urls.items():
    driver.get(url)            
    resp = Selector(text=driver.page_source)
    listings = resp.xpath('//div[@class="job-title"]/a/@href').getall()
    for link in listings:
        driver.get(link)
        sleep(1)
        # clicking on cookie button
        if not cookie_clicked:
            try:
                sleep(5)
                cookies_notification = driver.find_element_by_id('ccmgt_explicit_accept')
                cookies_notification.click()
                print('clicked on notification')
                cookie_clicked = True
            except:
                pass
        
        resp = Selector(text=driver.page_source)

        title = resp.xpath('//h1/text()').get()
        title = title.strip()
        if 'Access' in title:
            title = ''
        location = resp.xpath('//div[@class="col-xs-12 col-sm-7 travelTime-locationText"]/ul/li/text()').get()
        salary = resp.xpath('//li[@class="salary icon"]/div/text()').get()
        company_name = resp.xpath('//a[@id="companyJobsLink"]/text()').get() 
        job_type = resp.xpath('//li[@class="job-type icon"]/div/text()').get()

        print(title)
        print(location)
        print(salary)
        print(company_name)
        print(job_type)