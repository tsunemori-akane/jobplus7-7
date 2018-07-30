import scrapy

class LiePinScrapy(scrapy.Spider):
    name = 'liepin'

    start_urls = ['https://www.liepin.com/it/']

    def parse(self, response):
        for rep in response.css('div.hotjob-listwrap li'):
            yield {
                'job': rep.xpath('.//p[@class="job-title"]/a/text()').extract_first(),
                'salary': rep.xpath('.//span[@class="text-warning"]/text()').extract_first(),
                'city': rep.xpath('.//span[@class="area"]/text()').extract_first(),
                'degree': rep.xpath('.//span[@class="edu"]/text()').extract_first(),
                'work_year': rep.xpath('.//p[@class="condition clearfix"]/span[4]/text()').extract_first(),
                'name': rep.xpath('.//a[@class="job-img"]/@title').extract_first(),
                'logo': rep.xpath('.//a[@class="job-img"]/img/@src').extract_first()
            }
