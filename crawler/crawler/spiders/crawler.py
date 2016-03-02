#! /usr/bin/env python

import scrapy
import json
import sys
import time

class Spider(scrapy.Spider):
	name = "cashbackmonitor"
	start_urls = [
		"http://www.cashbackmonitor.com/",
	]

	store_title_path = '//div[@style="width:100%;text-align:center;"]/h1/span[@class="font2 s22"]/text()'
	front_page_store_path = '//div[@class="fl c"]/table/tr'
	stores = {}
	
	all_stores = []
	def parse(self, response):
		for sel in response.xpath(self.front_page_store_path):
			rate = ''
			name = ''
			url = ''
			for td in sel.xpath('td'):
				class_name = str(td.xpath('@class').extract()[0])
				if 'c' == class_name:
					text = td.xpath('text()').extract()
					if text == []:
						rate = str(td.xpath('a/text()').extract()[0])
						self.stores[name] = {'name': name, 'url': url, 'best_rate': rate}
				elif 'l tl' == class_name:
					href = str(td.xpath('a/@href').extract()[0])
					url = response.urljoin(href)
					name = str(td.xpath('a/text()').extract()[0])


		for store in self.stores.values():
			yield scrapy.Request(store['url'], callback = self.parse_each_website)
		


	def parse_each_website(self, response):
		store_detail = {}
		store_detail['name'] = str(response.xpath(self.store_title_path).extract()[0])
		store_detail['websites'] = []
		for sel in response.xpath('//td[@class="sp half"]/div[@class="half fl"]/table/tr'):
			url = ''
			name = ''
			rate = ''
			website = []
			for td in sel.xpath('td'):
				class_name = str(td.xpath('@class').extract()[0])
				if 'l lo' == class_name:
					href = str(td.xpath('a/@href').extract()[0])
					url = response.urljoin(href)
					name = str(td.xpath('a/text()').extract()[0])
				elif 'l' == class_name:
					rate = td.xpath('a/text()').extract()
					if rate == []:
						rate = str(td.xpath('text()').extract()[0])
						rate = rate.replace(' ', '')
						rate = rate.replace("\r", '')
						rate = rate.replace("\n", '')
						rate = rate.replace("\t", '')
					else:
						rate = str(rate[0])
					website.append({'name': name, 'url':url, 'rate': rate})
			store_detail['websites'].extend(website)
		# print store_detail['name']
		# print store_detail['websites']
		# self.all_stores.append(store_detail)
		store_detail['best_rate'] = self.stores[store_detail['name']]['best_rate']
		yield store_detail

