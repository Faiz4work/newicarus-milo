from scrapy import Spider, Request

myheaders = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}

class ReedSpider(Spider):
    name = 'reed'

    start_urls = ['https://www.reed.co.uk/jobs/jobs-in-belfast',
                    'https://www.reed.co.uk/jobs/jobs-in-birmingham',
                    'https://www.reed.co.uk/jobs/jobs-in-bradford-west-yorkshire',
                    'https://www.reed.co.uk/jobs/jobs-in-brighton',
                    'https://www.reed.co.uk/jobs/jobs-in-bristol',
                    'https://www.reed.co.uk/jobs/jobs-in-cardiff',
                    'https://www.reed.co.uk/jobs/jobs-in-coventry',
                    'https://www.reed.co.uk/jobs/jobs-in-derby',
                    'https://www.reed.co.uk/jobs/jobs-in-edinburgh',
                    'https://www.reed.co.uk/jobs/jobs-in-glasgow',
                    'https://www.reed.co.uk/jobs/jobs-in-hull',
                    'https://www.reed.co.uk/jobs/jobs-in-leeds',
                    'https://www.reed.co.uk/jobs/jobs-in-leicester',
                    'https://www.reed.co.uk/jobs/jobs-in-liverpool',
                    'https://www.reed.co.uk/jobs/jobs-in-london',
                    'https://www.reed.co.uk/jobs/jobs-in-manchester',
                    'https://www.reed.co.uk/jobs/jobs-in-milton-keynes',
                    'https://www.reed.co.uk/jobs/jobs-in-newcastle-upon-tyne',
                    'https://www.reed.co.uk/jobs/jobs-in-norwich',
                    'https://www.reed.co.uk/jobs/jobs-in-nottingham',
                    'https://www.reed.co.uk/jobs/jobs-in-plymouth',
                    'https://www.reed.co.uk/jobs/jobs-in-reading',
                    'https://www.reed.co.uk/jobs/jobs-in-sheffield',
                    'https://www.reed.co.uk/jobs/jobs-in-southampton',
                    'https://www.reed.co.uk/jobs/jobs-in-swansea',
                    'https://www.reed.co.uk/jobs/jobs-in-swindon']

    custom_settings = {
        'DOWNLOAD_DELAY' : 1,
        'AUTOTHROTTLE_ENABLED' : True,
        'AUTOTHROTTLE_START_DELAY' : 5,
        'AUTOTHROTTLE_MAX_DELAY' : 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY' : 0.5,
    }
    def parse(self, response):
        city = response.url
        city = city.split('/')[-1].replace('jobs-in-', '')
        if '-' in city:
            city = city.replace('-', ' ')
        links = response.xpath('//a[@data-gtm="job_click"]/@href').getall()
        links = [response.urljoin(i) for i in links]

        # current page url = https://www.reed.co.uk/jobs/jobs-in-belfast
        # links example = https://www.reed.co.uk/jobs/otrrba120421/42448318?source=searchResults#/jobs/jobs-in-belfast?sortby=DisplayDate
        for link in links:
            yield Request(url=link, callback=self.parse_jobs,
                            cb_kwargs={'city': city}, headers=myheaders)

        # next_page = response.xpath('//a[@id="nextPage"]/@href').get()
        

    def parse_jobs(self, response, city):
        featured = response.xpath('//span[@class="label label-featured"]/text()').get()
        if featured == 'Featured':
            title = response.xpath('//h1/text()').get()
            salary = response.xpath('//span[@itemprop="baseSalary"]/span/text()').get()
            company_location = response.xpath('//div[@class="job-info--high-level-item"]//span[@itemprop="addressLocality"]/text()|//div[@class="job-info--high-level-item"]//span[@data-qa="localityLbl"]/text()').getall()
            company_location = ', '.join(company_location)
            job_type = response.xpath('//span[@data-qa="jobTypeLbl"]/text()').get()
            company_name = response.xpath('//span[@itemprop="name"]/text()').get()
        
        else:
            title = response.xpath('//h1/text()').get()
            salary = response.xpath('//span[@itemprop="baseSalary"]/span/text()').get()
            job_type = response.xpath('//span[@data-qa="jobTypeLbl"]/text()').get()
            company_location = response.xpath('//span[@data-qa="regionLbl"]/text()').get() + ', ' + response.xpath('//span[@data-qa="localityLbl"]/text()').get()
            company_name = response.xpath('//span[@itemprop="name"]/text()').get()

        yield{
            'Title': title,
            'City': city,
            'Salary': salary,
            'Company Name': company_name,
            'Company Location': company_location,
            'Job Type': job_type,
            'Job Link': response.url,
        }