import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    pages_count = 5


    def start_requests(self):
        text = 'Дрель'
        for page in range(1, 1 + self.pages_count):
            url = f'https://leroymerlin.ru/search/?q={text}&page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.xpath("//div[@class='phytpj4_plp largeCard']/a/@href").extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)

        loader.add_value('_id', str(response))
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_xpath('terms', "//dt/text()")
        loader.add_xpath('definitions', "//dd/text()")
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_value('link', str(response))

        yield loader.load_item()
