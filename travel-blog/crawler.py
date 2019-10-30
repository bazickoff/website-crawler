import requests
import json
from bs4 import BeautifulSoup

class TravelBlogCrawler():
    def __init__(self, travel_blog):
        self.travel_blog = travel_blog

    def get_page_links(self):
        page_links = []
        for i in range(1, self.travel_blog.num_of_pages + 1):
            page_links.append(self.travel_blog.root_url + str(i) + "/")
        return page_links

    def get_html_soup(self, url):
        result = requests.get(url)
        html_soup = result.content
        html_soup = BeautifulSoup(html_soup, "html.parser")
        return html_soup

    def get_blog_links(self, page_links):
        blog_links = []
        for url in page_links:
            print(url)
            html_soup = self.get_html_soup(url)
            for link in html_soup.select("." + self.travel_blog.link_classname):
                blog_links.append(link.get('href'))
        return blog_links

    def cleanup(self, html_soup):
        if html_soup.find('aside'):
                html_soup.find('aside').decompose()

        for script in html_soup.find_all('script'):
            script.decompose()

        for style in html_soup.find_all('style'):
            style.decompose()

        # thepoortraveler
        for ad_item in html_soup.find_all('div', {"class": "ad-box-item"}):
            ad_item.decompose()

    def get_blog_content(self):
        content = ""
        page_links = self.get_page_links() 
        blog_links = self.get_blog_links(page_links)
        for url in blog_links:
            print(url)            
            html_soup = self.get_html_soup(url)
            self.cleanup(html_soup) 
            search_elem = { "class" : self.travel_blog.content_classname }           
            blog_content = html_soup.find("div", **search_elem)
            text = ""

            if blog_content:
                for string in blog_content.stripped_strings:
                    text += repr(string)
                content += text

        return content



class TravelBlog():
    def __init__(self, url, link_classname, content_classname, num_of_pages):
        self.root_url = url
        self.link_classname = link_classname
        self.content_classname = content_classname
        self.num_of_pages = num_of_pages



class BlogsCrawl():
    def __init__(self):
        self.text_filename = 'blog.txt'
        self.json_filename = 'blogs_info.json'

    def get_travel_blogs(self):
        blogs = []
        with open(self.json_filename) as json_data:
            d = json.load(json_data)
            for travel_blog in d["travel-blogs"]:                
                page_url = travel_blog['link']
                link_classname = travel_blog['read-more-class-name']
                content_classname = travel_blog['content-class-name']
                num_of_pages = travel_blog['num-of-pages']
                blogs.append(TravelBlog(page_url, link_classname, content_classname, num_of_pages))
        
        return blogs
                
    def start(self):
        travel_blogs = self.get_travel_blogs()

        for blog in travel_blogs:
            crawler = TravelBlogCrawler(blog)
            blog_content = crawler.get_blog_content()

            with open(self.text_filename, 'a') as file:
                file.write(blog_content)
                file.write("\n")


blogs_crawl = BlogsCrawl()
blogs_crawl.start()