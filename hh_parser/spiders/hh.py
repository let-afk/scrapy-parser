import scrapy
from scrapy.http import HtmlResponse
from hh_parser.items import HhParserItem


class HhSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python&excluded_text=&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20"]

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.xpath("//a[@class='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parser)
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parser(self, response: HtmlResponse):
        title = response.xpath("//h1[@data-qa='vacancy-title']//text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']/span//text()").getall()
        url = response.url
        yield HhParserItem(title=title, salary=salary, url=url)
