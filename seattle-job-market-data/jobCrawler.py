import requests
from bs4 import BeautifulSoup


class JobCrawler:
    def __init__(self, root_link, job_link):
        self.job_description = JobDescription(root_link, job_link)

    def getJobDescription(self):
        result = requests.get(self.job_description.root_link + self.job_description.job_link)
        html_soup = BeautifulSoup(result.content, "html.parser")
        self.populate(html_soup)
        html_soup.decompose()
        return self.job_description

    def populate(self, html_parser):
        self.job_description.category = self.job_description.job_link.strip().split('/')[2]

        self.job_description.title = self.get_value(html_parser,
                                                    self.job_description.title,
                                                    '.node-title .field')

        self.job_description.location = self.get_value(html_parser,
                                                       self.job_description.location,
                                                       '.company-address')

        self.job_description.content = self.get_text(html_parser,
                                                     self.job_description.content,
                                                     '.job-description')

        self.job_description.company_name = self.get_value(html_parser,
                                                           self.job_description.company_link,
                                                           '.job-info a')

        self.job_description.company_link = self.get_link(html_parser,
                                                          self.job_description.company_name,
                                                          '.job-info a')

    def get_value(self, html_parser, default_value, class_name):
        return \
            html_parser.select(class_name)[0].string \
                if html_parser.select(class_name) \
                else default_value

    def get_link(self, html_parser, default_value, class_name):
        return \
            html_parser.select(class_name)[0].get('href') \
                if html_parser.select(class_name) \
                else default_value

    def get_text(self, html_parser, default_value, class_name):
        return \
            html_parser.select(class_name)[0].findAll(text=True) \
                if html_parser.select(class_name) \
                else default_value


class JobDescription:
    def __init__(self, root_link, job_link, category="", title="", location="",
                 content="", company_link="", company_name=""):
        self.root_link = root_link
        self.job_link = job_link
        self.category = category
        self.title = title
        self.location = location
        self.content = content
        self.company_link = company_link
        self.company_name = company_name
