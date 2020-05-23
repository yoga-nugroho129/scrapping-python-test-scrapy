# 1) import scrapy
import scrapy
# 5.2) import items container class from items.py
from ..items import ScrappingquoteItem

# 2) create class that inherite 'spider' from scrapy
class QuoteSpider(scrapy.Spider):
  # 2.1) SPIDER NAME
  name = 'quotesNoLogin' 
  # 10.1) create pageNumber for url parameter
  pageNumber = 2
  start_urls = [ # 2.2) set the url to be scrape
    'http://quotes.toscrape.com/page/1/'
  ]

  # 3) create 'parse' method 
  # == EXAMPLE ==
  # def parse(self, response): # response is the html of the targeted url
  #   # example to get the title
  #   title = response.css('title::text').extract() # extract data using css selector (.css)
  #   yield {'titleText': title} # 'yield' is a 'return' for scrapy that's return a dictionary (key-value pair)
  #   # 3+) run spider by cd to scrappingQuote & run 'scrapy crawl spiderName'
  # == END OF EXAMPLE ==

  # 4) extract data from the url using the example of step 3
  def parse(self, response):
    # 5.3) Instantiate imported items
    items = ScrappingquoteItem()

    # 4.1) select the main selector
    allQuotes = response.css("div.quote") 

    # 4.2) loop through the allQuotes to get the data inside it
    for quote in allQuotes:
      quoteText = quote.css("span.text::text").extract()
      author = quote.css(".author::text").extract()
      tags = quote.css(".tag::text").extract()
      
      # 5.4) Store data inside the items instance 
      #       => inside [] should be same name with the instance in imported items
      #       => that equal to the variable that get data from url
      items['quote'] = quoteText
      items['author'] = author
      items['tags'] = tags
      # so we can yield it by using this code bellow to replace the step #4.3
      yield items

      # # 4.3) Outputing the result using yield
      # yield {
      #   "quote": quoteText,
      #   "author": author,
      #   "tags": tags
      # }

  # 5) Storing extracted data to temporary container named 'items' ==> move to 'items.py' file # 5.1

  # 6) extract the data with output type of JSON, XML, or CSV we can run the spider with :
  #     JSON format => scrapy crawl quotes -o result.json
  #     CSV format => scrapy crawl quotes -o result.csv
  #     XML format => scrapy crawl quotes -o result.xml

  # 7) before storing data on database/DB need a pipelines => move to 'settings.py' file

    # 9) Scrap next page WITHOUT pagination
    # 9.1) Create nextPage function to select the next page action
    # nextPage = response.css("li.next a::attr(href)").get()

    # # 9.2) check if the next button avaiable or not
    # if nextPage is not None:
    #   # 9.3) yield the to the next page using 'follow' method from scrapy
    #   # after hit the next page, run the callback of 'parse' method again to scrap the data inside the next page (recursive like)
    #   yield response.follow(nextPage, callback = self.parse)
    
    # 10) Scrap next page IF WITH pagination
    # 10.2) Create nextPage function to manipulate the url
    nextPage = "http://quotes.toscrape.com/page/" + str(QuoteSpider.pageNumber) + "/"

    # 10.3) check if the page number is equal to what we want the number of page to scrap
    if QuoteSpider.pageNumber < 10:
      # 10.4) yield the to the next page using 'follow' method from scrapy
      QuoteSpider.pageNumber += 1
      # after hit the next page, run the callback of 'parse' method again to scrap the data inside the next page (recursive like)
      yield response.follow(nextPage, callback = self.parse)