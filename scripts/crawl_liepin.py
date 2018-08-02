import scrapy

class LiePinS(scrapy.Spider):
    name = 'paliepin'
    start_urls = ['https://www.liepin.com/']

    def parse(self, response):
        for i in response.css('li.clearfix'):    
        
            url = i.css('p.job-title a::attr(href)').extract_first()
            
            request = scrapy.Request('https:'+url, callback=self.parse_detail)
            yield request
            
    
    def parse_detail(self, response):
            yield{
                'qualifications':response.css('div.job-qualifications span::text').extract(), 
                'about-position':response.css('div.tag-list span::text').extract(),
                'industry':response.css('ul.new-compintro a::text').extract_first().strip(),
                'company_size':response.css('ul.new-compintro li::text').extract()[2].strip(),
                'company_address':response.css('ul.new-compintro li::text').extract()[3].strip(),
                'company-logo':response.css('div.company-logo img::attr(src)').extract_first(),
                'post':response.css('div.title-info h1::text').extract_first(),
                'salary':response.css('div.job-title-left p::text').extract_first().strip(),
                'company-name':response.css('div.title-info a::attr(title)').extract_first(),
                'location':response.css('p.basic-infor a::text').extract_first()
            }
