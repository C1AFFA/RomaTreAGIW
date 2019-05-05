# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import crawler_utils, json
from mongodb_middleware import mongodb_interface
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from general_utils import text_parser
from bs4 import BeautifulSoup


# Definition of foxlink spider
class ProductFinderSpider(CrawlSpider):

    name = 'foxlink_spider'

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )


    def parse_item(self, response):
        domain = text_parser.extract_domain_from_url(response.url)
        if domain in self.start_urls:
            full_domain = text_parser.add_www_domain(domain)
            body = BeautifulSoup(response.body,'html.parser').body
            relevant_links = crawler_utils.extract_relevant_links(body, text_parser.remove_www_domain(domain), full_domain)
            content = {'url_page': str(response.url),
                       'html_raw_text': str(body),
                       'page_relevant_links': str(list(set(relevant_links))),
                       'depth_level': str(response.meta['depth']),
                       'referring_url': str(response.request.headers.get('Referer',None))}
            content = json.dumps(content)
            mongodb_interface.put(full_domain,content)



# Function for starting the crawler, it takes several parameters for the settings
def start_crawling(start_urls, allowed_domains,depth_limit,download_delay, closespider_pagecount, autothrottle_enable, autothrottle_target_concurrency):

    print '------------------------------------'
    print '--------------URLS------------------'
    print start_urls
    print allowed_domains

    #Check if the donwload delay is at a minimum of 0.3 sec
    if download_delay == None or download_delay<0.3:
        download_delay = 0.3

    custom_settings = get_project_settings()
    custom_settings.update({
        'DEPTH_LIMIT': str(depth_limit),
        'DOWNLOAD_DELAY': str(download_delay),
        'CLOSESPIDER_PAGECOUNT': str(closespider_pagecount),
        'AUTOTHROTTLE_ENABLED': str(autothrottle_enable),
        'AUTOTHROTTLE_TARGET_CONCURRENCY': str(autothrottle_target_concurrency),
        'CONCURRENT_REQUESTS': str(200),
        'REACTOR_THREADPOOL_MAXSIZE': str(20),
        'LOG_LEVEL' : 'INFO',
        'COOKIES_ENABLED':'False',
        'RETRY_ENABLE':'False',
        'DOWNLOAD_TIMEOUT':str(15),
        'REDIRECT_ENABLED':'False',
        'AJAXCRAWL_ENABLED':'True',
        'ROBOTSTXT_OBEY':'True',
        'SCHEDULER': 'domain_scheduler.DomainScheduler',
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0'
    })

    process = CrawlerProcess(custom_settings)
    process.crawl(ProductFinderSpider, start_urls=start_urls, allowed_domains=allowed_domains)
    process.start()
    return None