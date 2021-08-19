BOT_NAME = 'leroyparser'

SPIDER_MODULES = ['leroyparser.spiders']
NEWSPIDER_MODULE = 'leroyparser.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'

LOG_ENABLE = True
LOG_LEVEL = 'DEBUG'

IMAGES_STORE = 'images'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'leroyparser.pipelines.LeroyparserPipeline': 300,
    'leroyparser.pipelines.LeroyImagesPipeline': 200,
}

