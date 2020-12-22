#!/bin/bash

if [ -f "pts.html" ]; then 
	echo "Found pts.html in the current folder, skip getting html process."
else
    echo "producing pts.html..."
    python get_pts_urls.py
fi


if [ -f "pts_taigi_news.json" ]; then 
	echo "Found pts_taigi_news.json in the current folder, skip crawling process."
else
    echo "producing pts_taigi_news.json..."
    scrapy crawl pts_taigi_news -o pts_taigi_news.json
fi


python gen_pts_one_article_per_line.py