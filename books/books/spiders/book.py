import scrapy

from books.items import BooksItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        """
        Parse method provided by scrapy framework.
        Populated with the css selectors for the url, title, and price.
        Selectors found by parsing the target website using the browsers developer tools.
        """
        # Iterates over every book in url response
        for book in response.css("article.product_pod"):
            # Creates a BooksItem instance for each book and populates fields
            item = BooksItem()
            item["url"] = book.css("h3 > a::attr(href)").get()
            item["title"] = book.css("h3 > a::attr(title)").get()
            item["price"] = book.css(".price_color::text").get()
            # Yield turns parse into a generator and allows for multiple requests as opposed to just return the values
            yield item
