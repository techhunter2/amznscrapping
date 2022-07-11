import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
import re
# from ..items import AmznbotItem
queries = ['laptop']   
API = 'fde7f47431dfc12570fbbcf3f2476082'                   ##Used API From https://www.scraperapi.com/signup


def get_url(url):                 
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url
    # proxies are used for not getting blocked by Amazon


class SpidernmSpider(scrapy.Spider):
    name = 'spidernm'
    def start_requests(self):
        for query in queries:
            url = 'https://www.amazon.com/s?' + urlencode({'k': query})
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        
        products = response.xpath('//*[@data-asin]')

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.com/dp/{asin}"
            yield scrapy.Request(url=get_url(product_url), callback=self.parse_product_page, meta={'asin': asin})
            
        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urljoin("https://www.amazon.com",next_page)
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)

    def parse_product_page(self, response):
        # items  = AmznbotItem()
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        image = re.search('"large":"(.*?)"',response.text).groups()[0]
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
        number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        price = response.xpath('//span[@class="a-price-whole"]/text()').extract_first()
        details = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        manufacturer = response.xpath('//*[@id="prodDetails"]//td/text()')[1].extract()
        color = response.xpath('//*[@id="prodDetails"]//td/text()')[3].extract()

        # items['Asin'] = asin
        # items['Title'] = title
        # items['MainImage'] = image
        # items['Rating'] = rating
        # items['NumberOfReviews'] = number_of_reviews
        # items['Price($'] = price
        # items['Details'] = details
        # items['Manufacture'] = manufacturer
        # items['Color'] = color
        # yield items
        
        yield {'asin': asin, 'Title': title, 'MainImage': image, 'Rating': rating, 'NumberOfReviews': number_of_reviews,
               'Price($)':price, 'details':details,'Manufacture':manufacturer,'Color':color}
