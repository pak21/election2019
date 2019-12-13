#!/usr/bin/env python3

import os
import sys

import contextlib
from lxml import html
import mysql.connector as mysql
import requests

from election2019 import results2017

URL_TEMPLATE = 'https://www.bbc.co.uk/news/politics/constituencies/{}'

conn = mysql.connect(database='election2019', user='philip', password=os.environ['DATABASE_PASSWORD'])

parse = False

for constituency in results2017.index:
    if constituency == 'E14000550':
        parse = True

    if not parse:
        print('Skipping {}'.format(constituency))
        continue

    print('Fetching {} ({})'.format(constituency, results2017.loc[constituency].constituency_name))

    url = URL_TEMPLATE.format(constituency)
    page = requests.get(url)

    print('  Got HTML...')

    tree = html.fromstring(page.content)
    print('  Parsed HTML...')

    results = tree.xpath('//li[contains(@class, "ge2019-constituency-result__item")]')
    print('  Found {} parties'.format(len(results)))

    with contextlib.closing(conn.cursor()) as cursor:
        for result in results:

            party = result.xpath('.//span[@class="ge2019-constituency-result__party-code"]')[0].text
            print('    Party code {}'.format(party))

            details = result.xpath('.//span[@class="ge2019-constituency-result__text-wrapper"]')
            for d in details:
                items = d.xpath('./span')
                if items[0].text == 'Votes:':
                    votes = int(items[1].text.replace(',', ''))
                    print('    Votes {}'.format(votes))
                    cursor.execute('insert into results set ons_id = %s, party_code = %s, votes = %s', (constituency, party, votes))

        conn.commit()
