import requests
from bs4 import BeautifulSoup

class TravelBlogCrawler():
    def __init__(self):
        self.root_url = 'https://www.nomadicmatt.com/travel-blog/page/'

    def get_pages_links(self, root_url):
        page_links = []
        for i in range(1,6): # Every page has 6 blogs. Extract 5 pages i.e., 30 blogs
            page_links.append(self.root_url + str(i))
        return page_links

    def get_html_soup(self, url):
        result = requests.get(url)
        html_soup = result.content
        html_soup = BeautifulSoup(html_soup, "html.parser")
        return html_soup

    def get_blog_links(self, page_links):
        blog_links = []
        for url in page_links:
            html_soup = self.get_html_soup(url)
            for link in html_soup.select('.more-link'):
                blog_links.append(link.get('href'))
        return blog_links

    def get_blog_content(self):
        content = ""
        page_links = self.get_pages_links(self.root_url)
        blog_links = self.get_blog_links(page_links)
        for url in blog_links:
            html_soup = self.get_html_soup(url)
            blog_content = html_soup.find("div", { "class" : "entry-content" })
            text = ""
            for string in blog_content.stripped_strings:
                text += repr(string)
            content += text
        return content


crawler = TravelBlogCrawler()
blog_content = crawler.get_blog_content()

with open('output.txt','w') as file:
    file.write(blog_content)



