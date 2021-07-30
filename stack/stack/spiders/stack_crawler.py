import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from stack import items

class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['http://stackoverflow.com/questions?pagesize=50&sort=newest']

    rules = (
        Rule(LinkExtractor(allow=r'questions\?tab=newest&page=[0-3]'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]')

        for question in questions:
            item = items.StackItem()
            item['title'] = question.xpath('h3/a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath('h3/a[@class="question-hyperlink"]/@href').extract()[0]
            item['author'] = question.xpath('.//div[@class="user-details"]/a/text()').extract()[0]
            yield item