# for the csv wrangling
import sys
import os
import pandas as pd

goal_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')
DATA_URL = os.path.abspath(goal_dir)
data_path = os.path.join(DATA_URL, "DisasterDeclarationsSummaries.csv")

states = []

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
            by_state[disaster_type] = 1

    # big_cols is a dict of all the columns we're interested in
    big_cols = dict()
    big_cols['state'] = []
    big_cols['fyDeclared'] = []

    # fill big_cols with columns by disaster type
    for year, states in big_dict.items():
        for state, disasters in states.items():
            if state not in states:
                states.append[state]
            for disaster, freq in disasters.items():
                if disaster not in big_cols.keys():
                    big_cols[disaster] = []

    # big_dict is a dict of all the years we're interested in
    for k, v in big_dict.items():
        dir_out = os.path.join(goal_dir, str(k) + "disasters.csv")

        cols = dict()
        cols['state'] = []
        cols['fyDeclared'] = []

        # fill cols with columns by disaster type
        for year, states in big_dict.items():
            for state, disasters in states.items():
                for disaster, value in disasters.items():
                    if disaster not in cols.keys():
                        cols[disaster] = []

        # build columns by appending each state's data
        for state, disasters in v.items():
            cols['state'].append(state)
            cols['fyDeclared'].append(int(k))
            for disaster in cols:
                if disaster == 'state' or disaster == 'fyDeclared':
                    continue
                if disaster in disasters.keys():
                    cols[disaster].append(int(disasters[disaster]))
                else:
                    cols[disaster].append(0)
        for state in states:
            if state not in cols['state']:
                for disaster in cols:
                    if disaster == 'state':
                        cols['state'].append(state)
                    elif disaster == 'fyDeclared':
                        cols['fyDeclared'].append(int(k))
                    else:
                        cols[disaster].append(0)

        for c, l in big_cols.items():
            l.extend(cols[c])

        df = pd.DataFrame(data=cols)
        df.to_csv(dir_out)

    dir_out = os.path.join(goal_dir, "disasters.csv")
    df = pd.DataFrame(data=big_cols)
    df.to_csv(dir_out)
