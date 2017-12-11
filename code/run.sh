#!/bin/bash
./setup.sh
python3 stock_crawler.py
python3 tweet_class.py
python3 regressor.py
