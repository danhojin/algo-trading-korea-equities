# -*- coding: utf-8 -*-
import scrapy
from tinydb import TinyDB


class ListKospi200Spider(scrapy.Spider):
    name = 'list_kospi200'

    def __init__(self):
        super().__init__()
        self.db = TinyDB('db_list_kospi200.json')

    def start_requests(self):
        self.start_urls = ('https://finance.naver.com/sise/'
                           'entryJongmok.nhn?'
                           'order=itemname&isRightDirection=true')
        page = 1
        yield scrapy.Request(
            url=self.start_urls + f'&page={page}',
            callback=self.parse)

    def parse(self, response):
        on_page = response.css('.on a::text').get()

        for el in response.css('.ctg'):
            item = {
                'code': el.css('a::attr(href)').get().split('=')[-1],
                'name': el.css('a::text').get(),
            }
            self.db.insert(item)
            yield item

        if response.css('.pgR'):
            page = int(on_page) + 1
            yield scrapy.Request(
                url=self.start_urls + f'&page={page}',
                callback=self.parse)
