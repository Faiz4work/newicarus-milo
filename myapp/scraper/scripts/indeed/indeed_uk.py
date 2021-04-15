import scrapy
from scrapy import Request
from datetime import datetime
import requests as r
myheaders = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}
class IndeedUkSpider(scrapy.Spider):
    name = 'indeed_uk'
    days = '1'
    start_urls = ['https://uk.indeed.com/browsejobs']

    custom_settings = {
        'DOWNLOAD_DELAY' : 1,
        'AUTOTHROTTLE_ENABLED' : True,
        'AUTOTHROTTLE_START_DELAY' : 5,
        'AUTOTHROTTLE_MAX_DELAY' : 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY' : 0.5,
    }

    def parse(self, response):
        # There are 4 states in uk
        state_links = response.xpath('//li[@class="state"]/a/@href').getall()
        links = [response.urljoin(i) for i in state_links]

        for link in links:
            yield Request(url=link, callback=self.parse_cities)

    def parse_cities(self, response):
        # Receivig this sample url data: https://uk.indeed.com/browsejobs/in/England
        city_names_links = response.xpath('//p[@class="city"]/a/text()|//p[@class="city"]/a/@href').getall()
        names = city_names_links[1::2]
        links = city_names_links[::2]

        for city,link in zip(names, links):
            link = f"{link}?sort=date&fromage={self.days}"
            city = city.replace('jobs in ', '')
            yield Request(url=response.urljoin(link),
                          callback=self.parse_jobs_page,
                          meta={'city': city},
                          headers=myheaders)

    def parse_jobs_page(self, response):
        city = response.meta['city']
        job_links = response.xpath('//h2/a/@href').getall()
        for link in job_links:
            yield Request(url=response.urljoin(link), callback=self.parse_jobs,
                            meta={'city': city}, headers=myheaders)

        next_page = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page:
            if not '30' in next_page:
                yield Request(url=response.urljoin(next_page), 
                                callback=self.parse_jobs_page,  
                                meta={'city': city}, dont_filter=True,
                                headers=myheaders)


    def parse_jobs(self, response):
        city = response.meta['city']

        title = response.xpath('//h1/text()').get()

        div = response.xpath('//div[@class="icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle"]')
        try:
            location = div.xpath('.//div/text()')[-1].get()
        except:
            location = ''
        company_name = response.xpath('//div[@class="icl-u-textColor--success"]/text()').get()

        job_type = response.xpath('//div[contains(b/text(), "Job Type")]/text()').get()
        if job_type:
            job_type = job_type.replace(': ', '')
        salary = response.xpath('//span[@class="icl-u-xs-mr--xs"]/text()').get()
        
        job_link = response.xpath('//a[contains(text(), "original job")]/@href').get()
        req = r.get(job_link, headers=myheaders)
        job_link = req.url
        company_link = job_link.replace('//', 'ii').split('/')[0].replace('ii', '//')

        yield{
            'Title': title,
            'Company Name': company_name,
            'Company Website': company_link,
            'City': city,
            'Company Location': location,
            'Salary': salary,
            'Job Type': job_type,
            'Company Job link': job_link,
            'Job link': response.url,
        }

