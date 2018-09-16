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
        newlist = []
        if not row['2017']:
            continue
        else:
            try:
                pre_string = row['2017']
                if pre_string != '[]':
                    airports = pre_string[1:len(pre_string) - 1].split("\'")
                    for airport in airports:
                        if len(airport) <= 2:
                            airports.remove(airport)
                        airport.strip()
                for airport in airports:
                    if airport not in newlist:
                        newlist.append(airport)
                print(newlist)
                row['2017'] = newlist
            except TypeError as ex:
                continue
        if not row['2018']:
            continue
        else:
            try:
                pre_string = row['2018']
                if pre_string != '[]':
                    airports = pre_string[1:len(pre_string) - 1].split("\'")
                    for airport in airports:
                        if len(airport) <= 2:
                            airports.remove(airport)
                        airport.strip()
                for airport in airports:
                    if airport not in newlist:
                        newlist.append(airport)
                print(newlist)
                row['2018'] = newlist
            except TypeError as ex:
                continue

    df = pd.DataFrame(csv_reader)
    dir_out = os.path.join(goal_dir, "loc_dedup.csv")
    df.to_csv(dir_out)
