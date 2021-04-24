from scrapy import Request, Spider
import json
from time import sleep

myheader = {'content-type': 'application/json;charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
            'Accept': '*/*',
            'accept-encoding':'gzip, deflate, br',
}


class MonsterSpider(Spider):
    name = 'monster'

    url = 'https://services.monster.io/jobs-svx-service/v2/monster/jobs-search/samsearch/en-gb'
    cities = {
        'newport': 'l-newport,-wales',
        'scarborough yorkshire': 'l-scarborough,-yorkshire',
        'manchester north-west': 'l-manchester,-north-west',
        'ayr scotland': 'l-ayr,-scotland',
        'lowestoft anglia': 'l-lowestoft,-anglia',
        'shrewsbury midlands': 'l-shrewsbury,-midlands',
        'bristol south-west': 'l-bristol,-south-west',
        'swansea wales': 'l-swansea,-wales',
        'dundee scotland': 'l-dundee,-scotland',
        'leeds yorkshire': 'l-leeds,-yorkshire',
        'scotland': 'l-scotland',
        'plymouth south-west': 'l-plymouth,-south-west',
        'aberdeen scotland': 'l-aberdeen,-scotland',
        'edinburgh scotland': 'l-edinburgh,-scotland',
        'wrexham wales': 'l-wrexham,-wales',
        'norwich anglia': 'l-norwich,-anglia',
        'carlisle north-west': 'l-carlisle,-north-west',
        'glasgow scotland': 'l-glasgow,-scotland',
        'birmingham midlands': 'l-birmingham,-midlands',
    }
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'AUTOTHROTTLE_ENABLED' : True,
        'AUTOTHROTTLE_START_DELAY' : 5,
        'AUTOTHROTTLE_MAX_DELAY' : 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY' : 0.5,
    }

    def start_requests(self):
        for city, symbol in self.cities.items():
            for i in range(1,11):
                body = '{"jobQuery":{"locations":[{"address":"","country":"gb"}],"excludeJobs":[],"companyDisplayNames":[],"query":"' + f"{symbol}" + '"},"offset":' + f"{i}" + ',"pageSize":10,"searchId":"5ee4be24-f55e-44a3-9591-68f59a36c665","jobAdsRequest":{"position":[1,2,3,4,5,6,7,8,9,10],"placement":{"component":"JSR_SPLIT_VIEW","appName":"monster"}}}'
                yield Request(url=self.url, method='POST', dont_filter=True,
                                headers=myheader, body=body, 
                                    cb_kwargs={"city" : city})

    def parse(self, response, city):
        jdata = json.loads(response.body)
        data = jdata['jobResults']
        for i in data:
            title = i['enrichments']['normalizedTitles'][0]['title']

            # company_job_url = i['apply']['applyUrl']
            try:
                company_email = i['apply']['onsiteApplyEmail']
            except:
                company_email = ''
            try:
                job_type = i['enrichments']['employmentTypes'][0]['name']
            except:
                job_type = ''
            try:
                job_url = i['enrichments']['localizedMonsterUrls'][0]['url']
            except:
                job_url = ''
            try:
                job_location = i['enrichments']['normalizedJobLocations'][0]['postalAddress']['address']['addressLocality']
            except:
                job_location = ''
            
            try:
                currency = i['jobPosting']['baseSalary']['currency']
                min_salary = i['jobPosting']['baseSalary']['value']['minValue']
                max_salary = i['jobPosting']['baseSalary']['value']['maxValue']
                unit_text = i['jobPosting']['baseSalary']['value']['unitText']

                salary = f"{currency} {min_salary} - {max_salary} {unit_text}"
            except:
                salary = ''

            try:
                company_name = i['jobPosting']['hiringOrganization']['name']
            except:
                company_name = ''
            

            yield{
                'Title': title,
                # 'Company Job Url': company_job_url,
                'City': city,
                'Company Email': company_email,
                'Job Type': job_type,
                'Job Link': job_url,
                'Company Location': job_location,
                'Salary': salary,
                'Company Name': company_name,
            }