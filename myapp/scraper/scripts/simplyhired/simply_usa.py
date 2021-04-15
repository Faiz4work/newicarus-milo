from scrapy import Request, Spider

class SimplyUkSpider(Spider):
    name = 'simply_usa'
    start_urls = ['https://www.simplyhired.com/local-jobs']

    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'cache-control': 'max-age=0',
    }

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'AUTOTHROTTLE_ENABLED' : True,
        'AUTOTHROTTLE_START_DELAY' : 5,
        'AUTOTHROTTLE_MAX_DELAY' : 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY' : 0.5,
    }

    def parse(self, response):
        city_links = response.xpath('//a[@class="CategoryTile"]/@href').getall()
        city_links = [response.urljoin(i) for i in city_links]

        for link in city_links:
            city = link.split('/')[-1]
            yield Request(link, callback=self.parse_cities, 
                    cb_kwargs={'city': city},
                    headers=self.header)

    def parse_cities(self, response, city):
        all_jobs = response.xpath('//a[@class="button-jobs-near-me"]/@href').get()
        link = response.urljoin(all_jobs) + '&fdb=1'

        yield Request(link, callback=self.parse_listings,
                        cb_kwargs={'city': city},
                         headers=self.header)

    def parse_listings(self, response, city):
        links = response.xpath('//a[@class="SerpJob-link card-link"]/@href').getall()

        for link in links:
            yield Request(response.urljoin(link), callback=self.parse_jobs,
                            cb_kwargs={'city': city},
                            headers=self.header)

        next_page = response.xpath('//a[@class="Pagination-link next-pagination"]/@href').get()
        if next_page:
            if not 'pn=3' in next_page:
                yield Request(response.urljoin(next_page), callback=self.parse_listings,
                                    cb_kwargs={'city': city},
                                    headers=self.header)

    def parse_jobs(self,response, city):
        title = response.xpath('//div[@class="viewjob-jobTitle h2"]/text()').get()
        section = response.xpath('//div[@class="viewjob-labelWithIcon"]')

        company_name = section[0].xpath('.//text()').get()
        company_location = section[1].xpath('.//text()').get()
        job_type = response.xpath('//span[@class="viewjob-labelWithIcon viewjob-jobType"]/span/text()').get()

        yield{
            'City': city,
            'Title': title,
            'Company Name': company_name,
            'Company Location': company_location,
            'Job Type': job_type,
            'Job Link': response.url,
        }


