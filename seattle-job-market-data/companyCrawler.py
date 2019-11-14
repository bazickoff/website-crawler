import requests
from bs4 import BeautifulSoup


class CompanyCrawler:

    def __init__(self, location, root_link, company_link):
        self.company = Company(location, root_link, company_link)

    def getCompanyData(self):
        result = requests.get(self.company.root_link + self.company.company_link)
        html_soup = BeautifulSoup(result.content, "html.parser")
        self.populate(html_soup)
        html_soup.decompose()
        return self.company

    def populate(self, html_parser):
        self.company.industry = self.get_value(html_parser,
                                               self.company.industry,
                                              '.col-industry .item')
        self.company.funding = self.get_value(html_parser,
                                              self.company.funding,
                                             '.field_year_founded .item')
        self.company.local_employees = self.get_value(html_parser,
                                                      self.company.local_employees,
                                                     '.field_local_employees .item')
        self.company.total_employees = self.get_value(html_parser,
                                                      self.company.total_employees,
                                                     '.field_total_employees .item')
        self.company.overview = self.get_value(html_parser,
                                               self.company.overview,
                                              '.first-child .description')
        self.company.why_work = self.get_value(html_parser,
                                               self.company.why_work,
                                              '.last-child .description')
        self.company.address = self.get_value(html_parser,
                                              self.company.address,
                                             '.company_description')
        self.company.google_maps_location = self.get_link_from_iframe(html_parser,
                                                         self.company.google_maps_location,
                                                         '#gmap_location_widget_map',
                                                         '.google-maps-link')
        self.company.jobs = self.get_links(html_parser,
                                           self.company.jobs,
                                          '.job-opportunities-default .view-content .link')
        self.company.tech_stack = self.get_tech_stack(html_parser,
                                                      self.company.tech_stack,
                                                    '.accordion-tabs .full-stack-item')
        self.company.media_links = self.get_links(html_parser,
                                                  self.company.media_links,
                                                 '.view-company-news .views-row')

        print(self.company)

    def get_value(self, html_parser, default_value, class_name):
        return \
            html_parser.select(class_name)[0].string \
                if html_parser.select(class_name) \
                else default_value

    def get_links(self, html_parser, default_value, class_name):
        links = default_value
        if html_parser.select(class_name):
            for elem in html_parser.select(class_name):
                links.append(elem.select('a')[0].get('href'))
        return links

    def get_link_from_iframe(self, html_parser, default_value, iframe_id, class_name):
        if html_parser.select(iframe_id):
            iframe_response = requests.get(html_parser.select(iframe_id)[0].attrs['src'])
            iframe_parser = BeautifulSoup(iframe_response.content, "html.parser")
            link = iframe_parser.select(class_name)[0].get('href')
            print(link)
            iframe_parser.decompose()

    def get_tech_stack(self, html_parser, default_value, class_name):
        tech_stack = default_value
        if html_parser.select(class_name):
            for elem in html_parser.select(class_name):
                tech_stack.append(elem.string)
        return tech_stack


class Company:
    def __init__(self, location, root_link, company_link, industry="", funding="", local_employees=None,
                 total_employees=None, overview="", why_work="", address="", google_maps_location="",
                 jobs=None, tech_stack=None, media_links=None):
        self.location = location
        self.root_link = root_link
        self.company_link = company_link
        self.industry = industry
        self.funding = funding
        self.local_employees = local_employees
        self.total_employees = total_employees
        self.overview = overview
        self.why_work = why_work
        self.address = address
        self.google_maps_location = google_maps_location
        self.jobs = jobs if jobs else []
        self.tech_stack = tech_stack if tech_stack else []
        self.media_links = media_links if media_links else []
