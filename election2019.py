#!/usr/bin/env python3

import datetime

import pandas as pd

RESULTS_2017_FILENAME = 'HoC-GE2017-constituency-results.csv'
REFERENDUM_RESULTS_FILENAME = 'estimated-leave-vote-by-constituency.csv'

PARTY_NAMES_2017=['con', 'lab', 'ld', 'ukip', 'green', 'snp', 'pc', 'dup', 'sf', 'sdlp', 'uup', 'alliance', 'other']

def load_data():
    results2017 = pd.read_csv(RESULTS_2017_FILENAME, index_col='ons_id')
    results2017['turnout'] = (results2017.valid_votes + results2017.invalid_votes) / results2017.electorate
    for party in PARTY_NAMES_2017:
        results2017[party + '_percent'] = results2017[party] / results2017.valid_votes
    results2017['majority_percent'] = results2017.majority / results2017.valid_votes

    referendum = pd.read_csv(
        REFERENDUM_RESULTS_FILENAME,
        usecols=['PCON11CD', 'Figure to use'],
        index_col='PCON11CD'
    )
    referendum.columns = ['leave_percent']

    results2017 = results2017.join(referendum)

    return results2017

results2017 = load_data()
