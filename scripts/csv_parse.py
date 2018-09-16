# for the csv wrangling
import csv
import sys
import os
from urllib.parse import urljoin

goal_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')
DATA_URL = os.path.abspath(goal_dir)
data_path = os.path.join(DATA_URL, "DisasterDeclarationsSummaries.csv")

# parse the CSV into a dict
with open(data_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    big_dict = dict()
    for row in csv_reader:
        state = row["state"]
        disaster_type = row["incidentType"]
        year = int(row["declarationDate"].split("-")[0])

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
        file_name = os.path.join(DATA_URL, str(k) + ("disasters.csv"))
        with open(file_name, 'w+', newline='') as csv_file:
            csv_writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL)
            for qee, walue in v.items():
                for key, value in walue.items():
                    csv_writer.writerow([qee] + [key] + [str(value)])