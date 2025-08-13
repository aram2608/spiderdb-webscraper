import scrapy

from books.items import BooksItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def start_requests(self):
        """Refactored .start_requests to handle error logging."""
        for url in self.start_urls:
            yield scrapy.Request(
                url, callback=self.parse, errback=self.log_error
            )

    def parse(self, response):
        """
        Parse method provided by scrapy framework.
        Populated with the css selectors for the url, title, and price.
        Selectors found by parsing the target website using the browsers developer tools.

        Spider contract for testing
        @url https://books.toscrape.com
        @returns items 20 20
        @returns request 1 50
        @scrapes url title price
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

        # Handles pagination for web crawler recursively
        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            # Joins attribute to base url
            next_page_url = response.urljoin(next_page)
            # Logging
            self.logger.info(
                f"Navigating to next page with URL {next_page_url}."
            )
            yield scrapy.Request(url=next_page_url, 
                                callback=self.parse,
                                errback=self.log_error,
                                )

    def log_error(self, failure):
        """Helper method for error handling."""
        self.logger.error(repr(failure))