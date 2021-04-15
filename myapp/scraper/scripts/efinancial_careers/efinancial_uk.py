from scrapy import Spider, Request


class efinancialSpider(Spider):
    name = 'efinancial_uk'

    start_urls = ['https://www.efinancialcareers.co.uk/sitemap/html#jobsBySector']

    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
        'AUTOTHROTTLE_ENABLED' : True,
        'AUTOTHROTTLE_START_DELAY' : 5,
        'AUTOTHROTTLE_MAX_DELAY' : 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY' : 1.0,
    }

    def parse(self, response):
        section = response.xpath('//div[@id="jobsByLocation"]')
        links = section.xpath('.//li/a/@href').getall()

        for link in links:
            city = link.split('.')[-2].split('-')[-1]
            yield Request(url=link, callback=self.parse_city, 
                          cb_kwargs={'city': city})

    def parse_city(self, response, city):
        # ol = response.xpath('//ol')
        # titles = ol.xpath('.//li/h2/a/span/text()').getall()
        job_list = response.xpath('//ol/li[@class="jobPreview well"]/h2/a/@href').getall()
        for link in job_list:
            yield Request(url=link, callback=self.parse_job,
                            cb_kwargs={'city': city})


        next_page = response.xpath('//a[@title="Go to next page"]/@href').get()
        if next_page:
            yield Request(url=next_page, callback=self.parse_city,
                            cb_kwargs={'city': city})

    
    def parse_job(self, response, city):
        title = response.xpath('//span[@id="efcJobHeaderTitleFull"]/text()').get()
        job_details = response.xpath('//div[@id="jobDetailStrickyScrollUnderDiv"]')

        location = job_details.xpath('.//div[@class="col"]/text()').getall()[-1]
        location = location.strip().split()
        location.pop(0)
        location = ' '.join(location)

        company_name = job_details.xpath('.//div[@class="col"]/strong/text()').get()

        salary = response.xpath('//*[@id="jobDetailStrickyScrollUnderDiv"]/div/div/div[4]/div/text()').getall()
        salary = salary[-1].strip()

        job_type = job_details.xpath('.//div[2]/div/text()').get()
        description = response.xpath('//div[@class="m-md-4 jobContentFrame"]').getall()

        yield{
            'Title': title,
            'City': city,
            'Location':location,
            'Salary': salary,
            'Job Type': job_type,
            'Description': description,
            'Company Name': company_name,
            'Job Link': response.url,
        }





