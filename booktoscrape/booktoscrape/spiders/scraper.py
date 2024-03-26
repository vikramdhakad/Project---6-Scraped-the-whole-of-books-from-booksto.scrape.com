import scrapy


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        for books in response.xpath("//h3/a"):
            url = books.xpath('@href').get()
            ab_link = response.urljoin(url)
            yield response.follow(url=ab_link,callback=self.books_data)
            
        for page in range(1,50):
            nxt = response.xpath("//li[@class='next']/a/@href").get()
            yield response.follow(url=nxt,callback=self.parse)
            
    def books_data(self,response):
        yield{
            'Image':response.xpath("//img/@src").get(),
            'Book Name':response.xpath("//h1/text()").get(),
            'Price':response.xpath("//p[@class='price_color']/text()").get(),
            'Description':response.xpath("(//p/text())[11]").get()
        }
