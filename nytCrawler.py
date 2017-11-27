# -*- coding: utf-8 -*-
import scrapy
from newspaper import Article
from nyt.items import NytItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class NytcrawlerSpider(CrawlSpider):
    name = 'nytCrawler'
    custom_settings = {'CLOSESPIDER_ITEMCOUNT' : 600}
    allowed_domains = ['www.nytimes.com']
    start_urls = ['https://www.nytimes.com/section/world/europe']
    rules = (Rule(LinkExtractor(allow=[r'https://www.nytimes.com/\d{4}/\d{2}/\d{2}/world/europe/[^/]+']), callback="parse_item", follow=True),)
    #rules = (Rule(LinkExtractor(allow=[r'^((http[s]?|ftp):\/)?(\/)?(www.nytimes.com\/)(\d{4})\/(\d{2})\/(\d{2})\/(world\/europe)\/[^/]+']), callback="parse_item", follow=True),)
    idx = 0

    def parse_item(self,response):
        self.log("scrapping: " + response.url)

        article = Article(response.url)
        article.download()
        article.parse()

        artUrl = article.url
        artAuth = ' , '.join(article.authors)
        artTitle = article.title
        artText = article.text

        item = NytItem()
        item['url'] = artUrl
        item['authors'] = artAuth
        item['title'] = artTitle
        item['text'] = artText

        f = open('%d-{}'.format(artTitle) %(self.idx), 'w', encoding='utf8')
        f.write(artAuth+'\n')
        f.write(artUrl+'\n')
        f.write(artText)
        f.close()
        self.idx+=1
        return item

