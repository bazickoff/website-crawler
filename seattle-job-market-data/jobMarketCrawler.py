import requests
from bs4 import BeautifulSoup

class JobMarketCrawler:

    def __init__(self):
        pass

    def get_companies_by_location(self, job_market_data):
        companies_data = []
        for companies_by_location in job_market_data:
            job_market = JobMarket(companies_by_location)
            companies_list = list(self.fetch_company_links(job_market))
            companies_data.append(self.build_companies_dict(companies_list, job_market))
        return companies_data

    # TO-DO: cleanup html_soup. It gets very slow after a point.
    def fetch_company_links(self, job_market):
        company_links = []
        root_link = self.build_root_link(job_market, job_market.all)
        for page_number in range(0, job_market.number_of_pages):
            result = requests.get(root_link + str(page_number))
            html_soup = BeautifulSoup(result.content, "html.parser")
            company_links.extend(self.get_all_links(html_soup,
                                                    job_market.class_name))
            html_soup.decompose()

        root_link = self.build_root_link(job_market, job_market.hiring_now)
        for page_number in range(0, job_market.number_of_pages):
            result = requests.get(root_link + str(page_number))
            html_soup = BeautifulSoup(result.content, "html.parser")
            company_links.extend(self.get_all_links(html_soup,
                                                    job_market.class_name))
            html_soup.decompose()

        return set(company_links)


    def get_all_links(self, html_parser, class_name):
        links = []
        for link in html_parser.select("." + class_name):
            links.append(link.get('href'))
        return links

    def build_root_link(self, job_market, type):
        return job_market.root_link + job_market.companies_page + type + job_market.pagination_query_string


    def build_companies_dict(self, companies_list, job_market):
        return {'location': job_market.location,
                'root_link': job_market.root_link,
                'companies_list': companies_list}


class JobMarket:
    def __init__(self, data):
        self.__dict__ = data
