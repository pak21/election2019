#!/usr/bin/env python3

import os

import contextlib
import mysql.connector as mysql
import pandas as pd

from election2019 import results2017

def get_votes(by_policy, policy):
    try:
        return by_policy.loc[policy].votes
    except KeyError:
        return 0

SQL = '''
select results.party_code, brexit_policy.policy, results.votes
from results
join brexit_policy on results.party_code = brexit_policy.party_code
where results.ons_id = %s
order by results.votes desc
'''

conn = mysql.connect(database='election2019', user='philip', password=os.environ['DATABASE_PASSWORD'])

print('ONS ID,Constituency,Leave,Remain,Other,Actual winner,Coalition winner,Unsure,Changed')
with contextlib.closing(conn.cursor()) as cursor:
    for constituency in results2017.index:
        cursor.execute(SQL, (constituency,))
        votes = pd.DataFrame(cursor.fetchall(), columns=['party_code', 'brexit_policy', 'votes'])

        actual_winner_policy = votes.iloc[0].brexit_policy

        by_policy = votes.groupby('brexit_policy').sum()

        coalition_winner_policy = by_policy.votes.idxmax()
        coalition_winner_votes = by_policy.loc[coalition_winner_policy].votes

        total_votes = sum(votes.votes)

        result_unsure = 2 * coalition_winner_votes <= total_votes
        result_changed = coalition_winner_policy != actual_winner_policy

        if result_unsure or result_changed:
            leave, remain, other = [get_votes(by_policy, policy) for policy in ['Leave', 'Remain', 'Other']]
            print('{},"{}",{},{},{},{},{},{},{}'.format(
                constituency,
                results2017.loc[constituency].constituency_name,
                leave, remain, other,
                actual_winner_policy,
                coalition_winner_policy,
                result_unsure,
                result_changed))
