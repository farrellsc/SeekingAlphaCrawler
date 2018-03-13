# -*- coding: utf-8 -*-
import scrapy
import codecs
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArticlelistcrawlerSpider(scrapy.Spider):
    name = 'articleListCrawler'
    allowed_domains = ['seekingalpha.com']
    page_num = 1
    output_base = './data/articleList'
    sector = 'investing-strategy'
    start_urls = [
        #'https://seekingalpha.com/stock-ideas?page=' + str(page_num),
        #'https://seekingalpha.com/dividends?page=' + str(page_num),
        #'https://seekingalpha.com/market-outlook?page=' + str(page_num),
        'https://seekingalpha.com/' + sector + '?page=' + str(page_num)
        #'https://seekingalpha.com/etfs-and-funds?page=' + str(page_num)
    ]
    url_limits = {
        'stock-ideas': 2000,
        'dividends': 858,
        'market-outlook': 2000,
        'investing-strategy': 426,
        'etfs-and-funds': 374
    }

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse(self, response):
        selector = scrapy.Selector(text=response.body, type='html')
        article_urls = selector.xpath("//li/div[contains(@class, 'media-body')]/a/@href").extract()
        url = response.request.url
        current_sector = url.split('?')[0].split('/')[-1]

        with codecs.open(self.output_base + '_' + current_sector, 'a', encoding='utf8') as foutput:
            for article_url in article_urls:
                actual_url = 'https://' + self.allowed_domains[0] + article_url + '\n'
                foutput.write(actual_url)

        self.page_num += 1
        if self.page_num > self.url_limits[current_sector]:
            return
        next_url = url.split('=')[0] + '=' + str(self.page_num)
        yield scrapy.Request(next_url, callback=self.parse)
