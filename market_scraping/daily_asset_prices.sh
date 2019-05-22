#!/usr/bin/bash
cat $1 | awk -F',' '{if(NR>1) print$1}' | xargs -I {} scrapy crawl daily_asset_prices -L INFO -a code={}
