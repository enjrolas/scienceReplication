BOT_NAME = 'sciencereplication'

SPIDER_MODULES = ['papers.scrapers']
NEWSPIDER_MODULE = 'papers.scrapers'

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.0
COOKIES_ENABLED = False

USER_AGENT = 'ScienceReplication/1.0 (+https://sciencereplication.artiswrong.com)'

LOG_LEVEL = 'INFO'

ITEM_PIPELINES = {
    'papers.scrapers.pipelines.DatasetLinkPipeline': 300,
}
