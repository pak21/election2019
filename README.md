# Election 2019

Data and tools to hopefully make some interesting visualizations on (UK)
General Election night 2019.

## Download

Run `download.sh` to get the source data:

* 2017 GE results

The estimated leave vote shares by constituency are from [this Google Sheet
by Dr Chris Hanretty of UEA](https://docs.google.com/spreadsheets/d/1b71SDKPFbk-ktmUTXmDpUP5PT299qq24orEA0_TOpmw/edit#gid=579044181).
TODO: download the data rather than checking it in. (This file is _not_ covered
by the MIT license).

## Reality

In reality, I didn't get a chance to do anything on election night. That said...

## Grand coalition analysis

Two scripts here to support a [blog post I've written](https://jorallan.dreamwidth.org/6644.html):

* `bbc-scraper.py`: scrape the 2019 results from the BBC website and stick them
in an SQL database.
* `coalitions.py`: what would have happened had there been "leave" and "remain"
grand coalitions?

If you want the scraped data, it's in `election2019.sql.xz`.
