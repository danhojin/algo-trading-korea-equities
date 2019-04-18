# -*- coding: utf-8 -*-
import scrapy
from pony import orm
from .db.model import Asset, DailyPrice
import re
from collections import OrderedDict
import logging
from datetime import date
from dateutil.parser import parse as date_parse


# logging.basicConfig(filename='daily_asset_price.log', level=logging.DEBUG)

class DailyAssetPricesSpider(scrapy.Spider):
    name = 'daily_asset_prices'

    @orm.db_session
    def __init__(self, code='066570', *args, **kwargs):
        super().__init__(*args, **kwargs)
        asset = Asset.get(code=code)
        if asset is None:
            logging.critical(f'Asset {code} is not registered yet.')
            raise ValueError(f'Asset {code} is not registered yet.')
        self.code = code
        self.latest_date = orm.max(
            dp.date for dp in DailyPrice if dp.asset.code == code)
        self.latest_date = self.latest_date \
            if self.latest_date else date(1900, 1, 1)

    def start_requests(self):
        self.start_url = ('https://finance.naver.com/item/sise_day.nhn?'
                          'code={}&page={}')
        yield scrapy.Request(
            url=self.start_url.format(self.code, 1),
            callback=self.parse)

    @orm.db_session
    def parse(self, response):
        p = re.compile(r'=(\d+)')
        code = p.search(response.url).group(1)
        assert self.code == code
        on_page = response.css('.on a::text').get()

        els = response.css('tr[onmouseover="mouseOver(this)"]')
        for el in els:
            fields = ['date', 'close', 'change',
                      'open', 'high', 'low', 'volume']
            data = el.css('td span::text').getall()
            data = map(lambda x: x.replace(',', ''), data)   # remove ","
            data = map(lambda x: x.replace('.', '-'), data)  # thousand symbol
            data = map(lambda x: x.strip(), data)
            record = OrderedDict(zip(fields, data))

            del record['change']
            record['date'] = date_parse(record['date']).date()
            record['asset'] = self.code

            if record['date'] <= self.latest_date:
                orm.commit()
                break
            DailyPrice(**record)
            orm.commit()
            yield record
        else:
            if response.css('.pgR'):
                page = int(on_page) + 1
                yield scrapy.Request(
                    url=self.start_url.format(code, page),
                    callback=self.parse)
