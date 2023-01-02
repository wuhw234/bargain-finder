import scrapy


class AmazonSpider(scrapy.Spider):
    name = "amazon"

    def __init__(self, search_phrase):
        filtered = search_phrase.replace('+', '%2B')
        words = filtered.split(' ')
        search_string = '+'.join(words)
        self.start_url = f'https://www.amazon.com/s?k={search_string}'
        print('start url', self.start_url)

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        for card in response.css('div.s-card-container.puis'):
            yield {
                'image': card.css('img.s-image').attrib['src'],
                'link': 'https://www.amazon.com' + card.css('a.a-text-normal').attrib['href'],
                'title': card.css('span.a-size-medium::text').get(),
                'stars': card.css('span.a-icon-alt::text').get(),
                'price': card.css('span.a-price-whole::text').get(),
            }

        next_page = response.css('a.s-pagination-next').attrib['href']
        if next_page:
            next_page = response.urljoin(next_page)
            print('asdf', next_page)
            yield scrapy.Request(next_page, callback=self.parse)