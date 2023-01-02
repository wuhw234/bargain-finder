import scrapy


class CardsSpider(scrapy.Spider):
    name = "cards"
    start_urls = [
        'https://www.amazon.com/s?k=turbotax+2022+deluxe&crid=5IR4UZZPJ0N4&sprefix=%2Caps%2C163&ref=nb_sb_ss_sx-trend-t-all-d_2_0'
    ]

    def parse(self, response):
        for card in response.css('div.s-card-container'):
            yield {
                'image': card.css('img.s-image').attrib['src'],
                'title': card.css('span.a-size-medium::text').get(),
                'stars': card.css('span.a-icon-alt::text').get(),
                'price': card.css('span.a-price-whole::text').get(),
            }

        next_page = response.css('a.s-pagination-next').attrib['href']
        if next_page:
            next_page = response.urljoin(next_page)
            print('asdf', next_page)
            yield scrapy.Request(next_page, callback=self.parse)