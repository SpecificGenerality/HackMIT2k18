from urllib.parse import urljoin
import pandas as pd
import os
import csv

goal_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')
DATA_URL = os.path.abspath(goal_dir)
data_path = os.path.join(DATA_URL, "locations.csv")

with open(data_path, 'r') as csv_file:
    csv_reader = pd.read_csv(
        data_path, usecols=['state', str(2017), str(2018)])
    for index, row in csv_reader.iterrows():
        state = row['state']
        if not row['2017']:
            continue
        else:
            newlist = []
            try:
                for i in row['2017']:
                    if i not in newlist:
                        print(i)
                        newlist.append(i)
                row['2017'] = newlist
                newlist = []
            except TypeError as ex:
                continue
        if not row['2018']:
            continue
        else:
            try:
                for i in row['2018']:
                    if i not in newlist:
                        newlist.append(i)
                row['2018'] = newlist
            except TypeError as ex:
                continue

    df = pd.DataFrame(csv_reader)
    dir_out = os.path.join(goal_dir, "loc_dedup.csv")
    df.to_csv(dir_out)
