#!/usr/bin/env bash

python3.7 -m venv __venv__
source ./__venv__/bin/activate 2> /dev/null
python -m pip install scrapy bs4

scrapy runspider src/crawler.py -o results/data.json &> results/base.log

deactivate
rm -rf __venv__