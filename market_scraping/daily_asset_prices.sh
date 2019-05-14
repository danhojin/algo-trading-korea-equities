#!/usr/bin/bash
cat < list_kospi200.csv | awk -F',' '{if(NR>1) print$1}' | xargs -I {} scrapy crawl daily_asset_prices -L INFO -a code={}
