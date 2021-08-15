import scrapy
from lesson5.items import MyJobparserItem

class CatalogSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=st=searchVacancy&text=python']
    pages_count = 2

    def start_requests(self):
        vak = 'ИТ директор'
        for page in range(0, 1 + self.pages_count):
            url = f'https://hh.ru/search/vacancy?area=st=searchVacancy&text={vak}&page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        for href in response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract():
            print(href)
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    # def parse(self, response):
    #     name = response.css('div.vacancy-title h1::text').extract()
    #
    #     salary = response.css('//span[@class='bloko-header-2 bloko-header-2_lite']/text()).extract()
    #
    #     vacancy_link = response.url
    #     site_scraping = self.allowed_domains[0]
    #
    #     yield JobParserItem(
    #         name=name, \
    #         salary=salary, \
    #         vacancy_link=vacancy_link, \
    #         site_scraping=site_scraping
    #     )

    def parse(self, response):
        name = response.xpath("//h1[@class='bloko-header-1']//text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        yield MyJobparserItem(name=name, salary=salary, link=response.url)
