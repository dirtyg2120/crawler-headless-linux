from scrapy import Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from stack import items

class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ["http://stackoverflow.com/questions?tab=newest&page=1"]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]')

        for question in questions:
            item = items.StackItem()
            item['title'] = question.xpath('h3/a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath('h3/a[@class="question-hyperlink"]/@href').extract()[0]
            item['author'] = question.xpath('.//div[@class="user-details"]/a/text()').extract()[0]
            yield item
