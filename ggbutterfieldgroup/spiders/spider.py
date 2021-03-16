import scrapy

from scrapy.loader import ItemLoader

from ..items import GgbutterfieldgroupItem
from itemloaders.processors import TakeFirst


class GgbutterfieldgroupSpider(scrapy.Spider):
	name = 'ggbutterfieldgroup'
	start_urls = ['https://www.gg.butterfieldgroup.com/News/Pages/default.aspx?Year=2021']

	def parse(self, response):
		post_links = response.xpath('//tr[@class="default"]')
		for post in post_links:
			url = post.xpath('.//div[@class="item link-item bullet"]/a/@href').get()
			date = post.xpath('.//td[@class="default bottomBorderdot padL7"]/text()').get()
			title = post.xpath('.//div[@class="newDes"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

		next_page = response.xpath('//td[contains(@class, "newsYear")]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response, date, title):
		description = response.xpath(
			'//*[(@id = "WebPartWPQ3")]//text()[normalize-space() and not(ancestor::h1)]|//*[(@id = "WebPartWPQ2")]//td//text()[normalize-space() and not(ancestor::h1)]|//*[contains(concat( " ", @class, " " ), concat( " ", "default", " " ))]//div//text()[normalize-space()]|//*[(@id = "ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField")]//div//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=GgbutterfieldgroupItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
