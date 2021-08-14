"""
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
"""


from lxml import html
import requests


def lenta_news():
    news = []
    keys = ('title', 'date', 'link')
    link_lenta = 'https://lenta.ru/'
    request = requests.get(link_lenta)
    root = html.fromstring(request.text)
    root.make_links_absolute(link_lenta)
    news_links = root.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 |
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/@href''')

    news_text = root.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 |
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/text()''')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_date = []

    for item in news_links:
        request = requests.get(item)
        root = html.fromstring(request.text)
        date = root.xpath('//time/@title')
        news_date.extend(date)

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):

            news_dict[key] = value
        news_dict['source'] = 'lenta.ru'
        news.append(news_dict)
    return news


print(lenta_news())
