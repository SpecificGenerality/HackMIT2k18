# for the csv wrangling
import sys
import os
import pandas as pd
from urllib.parse import urljoin

goal_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')
DATA_URL = os.path.abspath(goal_dir)
data_path = os.path.join(DATA_URL, "DisasterDeclarationsSummaries.csv")

# parse the CSV into a dict
with open(data_path, mode='r') as csv_file:
    csv_reader = pd.read_csv(
        data_path, usecols=['state', 'incidentType', 'fyDeclared'])
    line_count = 0
    big_dict = dict()
    for index, row in csv_reader.iterrows():
        state = row["state"]
        disaster_type = row["incidentType"]
        year = int(row["fyDeclared"])

        # read all of the data into big_dict
        # example: big_dict = {1953: {'GA':{'Flood' : 10, 'Hurricane': 1}}}
        try:
            by_year = big_dict[year]
        except KeyError as ex:
            big_dict[year] = dict()
            by_year = big_dict[year]

        try:
            by_state = by_year[state]
        except KeyError as ex:
            by_year[state] = dict()
            by_state = by_year[state]

        try:
            by_state[disaster_type] = by_state[disaster_type] + 1
        except KeyError as ex:
            by_state[disaster_type] = 0
            by_state[disaster_type] = by_state[disaster_type] + 1

    for k, v in big_dict.items():
        dir_out = os.path.join(goal_dir, str(k) + "disasters.csv")

        cols = dict()
        cols['state'] = []
        for k, v in big_dict.items():
            for key, value in v.items():
                for qee, walue in value.items():
                    if qee not in cols.keys():
                        cols[qee] = []

        for key, value in v.items():
            cols['state'].append(key)
            for disaster in cols:
                if disaster == 'state':
                    continue
                if disaster in value.keys():
                    cols[disaster].append(int(value[disaster]))
                else:
                    cols[disaster].append(0)

        df = pd.DataFrame(data=cols)
        df.to_csv(dir_out)
