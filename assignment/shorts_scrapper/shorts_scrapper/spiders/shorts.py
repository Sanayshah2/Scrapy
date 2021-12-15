from urllib import parse
import scrapy
# from ..items import ShortsScrapperItem

class Shorts(scrapy.Spider):
    name = 'shorts'
    main_url = 'https://in.seamsfriendly.com'
    start_urls = ['https://in.seamsfriendly.com/collections/shorts?page=1']
    counter = 2
    # item = ShortsScrapperItem()

    def parse(self, response):
        for product in response.css('div.Grid__Cell'):
            # multiple_colors = product.css('div.swatch-navigable')
            # if multiple_colors != []:
            #     for x in multiple_colors:
            #         yield response.follow(self.main_url+x.css(), callback = self.parseProduct)
            # else:
            yield response.follow(self.main_url+product.css('a.ProductItem__ImageWrapper--withAlternateImage').attrib['href'], callback = self.parseProduct)
        if self.counter <=3:
            next_page = 'https://in.seamsfriendly.com/collections/shorts?page='+str(self.counter)
            self.counter+=1
            yield response.follow(next_page, callback = self.parse)
        

    def parseProduct(self, response):
        yield {
            'title':response.css('h1.u-h2::text').get().replace('\n', '').strip(),
            'description':response.css('div.ProductMeta__Description div.Rte ul li::text').getall(),
            'image_links':['https:'+x for x in response.css('a.Product__SlideshowNavImage img::attr(src)').getall()],
            'price':response.css('span.ProductMeta__Price::text').get()[1:].replace(',', '')
        }
        