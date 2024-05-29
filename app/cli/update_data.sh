#!/bin/bash

export PYTHONPATH=$(pwd)
python app/cli/admin.py bulk-upload-tickers --provider Yahoo --file-path assets/YahooTickerSymbols-September2017.xlsx