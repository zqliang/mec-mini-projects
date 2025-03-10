import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.xpath("//div[contains(@class, 'quote')]"):
            yield {
                'text': quote.xpath("span[contains(@class, 'text')]/text()").get(),
                'author': quote.xpath("span/small[contains(@class, 'author')]/text()").get(),
                'tags': quote.xpath("div[contains(@class,'tags')]/a[contains(@class, 'tag')]/text()").getall()
            }