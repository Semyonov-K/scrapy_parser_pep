import scrapy

from urllib.parse import urljoin

from ..items import PepParseItem

class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('section#numerical-index')
        pep_links = all_peps.css("a::attr(href)").getall()
        for link in pep_links[1:]:
            pep_link = urljoin(self.start_urls[0], link)
            yield response.follow(pep_link, self.parse_pep)

    def parse_pep(self, response):
        number_name = response.css('h1.page-title::text').get()
        number, name = number_name.split(sep=' – ')
        status = response.css('abbr::text').get()
        pep_item = PepParseItem(number=number, name=name, status=status)
        yield pep_item
