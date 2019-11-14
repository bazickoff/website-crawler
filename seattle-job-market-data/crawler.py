# TO-DO: Move each operation to its respective IO file. Add a utils file.

import json

from companyCrawler import CompanyCrawler
from jobMarketCrawler import JobMarketCrawler
from jobCrawler import JobCrawler


class Crawler:

    def __init__(self):
        file_root = 'files/'
        self.json_root_file = file_root + 'web_links_data.json'
        self.json_companies_by_location = file_root + 'companies_by_location.json'
        self.csv_companies_dump = file_root + 'companies_data.json'
        self.csv_jobs_dump = file_root + 'jobs_data.json'

    def start(self):
        # self.scrape_job_market()
        self.scrape_companies_by_location()
        # self.scrape_job_data()

    def scrape_job_market(self):
        job_market_crawler = JobMarketCrawler()

        with open(self.json_root_file) as json_data:
            json_data = json.load(json_data)
            company_links = job_market_crawler.get_companies_by_location(json_data["job-market-data"])

        with open(self.json_companies_by_location, 'w') as json_dump:
            json.dump(company_links, json_dump)

    def scrape_companies_by_location(self):
        with open(self.json_companies_by_location) as json_data:
            json_data = json.load(json_data)
            for companies_by_location in json_data:
                self.scrape_company_data(companies_by_location)

    def scrape_company_data(self, companies_by_location):
        location = companies_by_location['location']
        root_link = companies_by_location['root_link']
        companies = companies_by_location['companies_list']
        companies_data = []
        for company_link in companies:
            company_crawler = CompanyCrawler(location, root_link, company_link)
            companies_data.append(company_crawler.getCompanyData().__dict__)
        self.dump_company_data(companies_data)

    # TO-DO: Write to CSV instead of JSON
    def dump_company_data(self, companies_data):
        with open(self.csv_companies_dump, 'w') as csv_dump:
            json.dump(companies_data, csv_dump)

    def read_companies_data(self):
        companies_data = []
        with open(self.csv_companies_dump) as json_data:
            json_data = json.load(json_data)
            for company in json_data:
                companies_data.append(company)
        return companies_data

    def scrape_job_data(self):
        companies_data = self.read_companies_data()
        job_description_list = []
        for company in companies_data:
            root_link = company['root_link']
            for job_link in company['jobs']:
                if "engineer" in job_link or "data" in job_link:
                    job_crawler = JobCrawler(root_link, job_link)
                    job_description_list.append(job_crawler.getJobDescription().__dict__)
        self.dump_job_data(job_description_list)

    # TO-DO: Write to CSV instead of JSON
    def dump_job_data(self, job_description_list):
        with open(self.csv_jobs_dump, 'w') as csv_dump:
            json.dump(job_description_list, csv_dump)


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
