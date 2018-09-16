import requests
from urllib.parse import urljoin
import pandas as pd
import os
import json

AMADEUS_URL = "https://test.api.amadeus.com"
ENDPOINT = "/v1/travel/analytics/air-traffic/traveled"
ACCESS_TOKEN = ''
HEADERS = {'Authorization': 'Bearer J4eGqOk3rllgwAZnARExCJAA7zDA'}

params = dict()

airports = {
    'AL': {'BHM'},
    'AK': {'ANC'},
    'AZ': {'PHX'},
    'AR': {'XNA'},
    'CA': {'LAX', 'SAN', 'SFO'},
    'CO': {'DEN'},
    'CT': {'BDL', 'HVN'},
    'DC': {'IAD', 'DCA'},
    'FL': {'FLL', 'MIA', 'MCO'},
    'GA': {'ATL'},
    'HI': {'KOA'},
    'ID': {'BOI'},
    'IL': {'MDW', 'ORD'},
    'IN': {'IND'},
    'IA': {'DSM'},
    'KS': {'ICT'},
    'KY': {'LEX'},
    'LA': {'MSY'},
    'ME': {'AUG', 'BGR'},
    'MD': {'BWI'},
    'MA': {'BOS'},
    'MI': {'DTW'},
    'MN': {'MSP'},
    'MS': {'GPT', 'JAN'},
    'MO': {'MCI', 'STL'},
    'MT': {'BIL'},
    'NE': {'OMA'},
    'NV': {'LAS'},
    'NH': {'MHT'},
    'NJ': {'EWR'},
    'NM': {'ABQ', 'ALM'},
    'NY': {'JFK', 'LGA'},
    'NC': {'CLT'},
    'ND': {'BIS', 'FAR'},
    'OH': {'CLE', 'DAY'},
    'OK': {'OKC', 'TUL'},
    'OR': {'PDX'},
    'PA': {'PHL'},
    'RI': {'PVD'},
    'SC': {'CHS'},
    'SD': {'RAP'},
    'TN': {'MEM', 'BNA'},
    'TX': {'AUS', 'DAL', 'DFW', 'HOU', 'IAH'},
    'UT': {'SLC'},
    'VT': {'BTV'},
    'VA': {'IAD', 'DCA'},
    'WA': {'SEA'},
    'WV': {'CRW'},
    'WI': {'MKE'},
    'WY': {'CPR'}
}

goal_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')
DATA_URL = os.path.abspath(goal_dir)
data_path = os.path.join(DATA_URL, "disasters.csv")
big_dict = dict()

with open(data_path, 'r') as csv_file:
    csv_reader = pd.read_csv(csv_file)

    for index, row in csv_reader.iterrows():
        state = row["state"]
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
            by_year[state] = []
            by_state = by_year[state]

    year = 2017

    # loop over all of the disaster data
    for index, row in csv_reader.iterrows():
        if int(row['fyDeclared']) < year:
            continue

        year = int(row['fyDeclared'])
        state = row['state']
        # loop through each month
        locations = []
        for i in range(1, 13):
            try:
                for airport in airports[state]:
                    params['origin'] = airport
                    if i < 10:
                        params['period'] = str(year) + '-0' + str(i)
                    else:
                        params['period'] = str(year) + '-' + str(i)
                    print(params['period'])
                    r = requests.get(
                        url=urljoin(AMADEUS_URL, ENDPOINT),
                        params=params,
                        headers=HEADERS)

                    data = r.json()
                    print(data)
                    try:
                        data['errors']
                        dir_out = os.path.join(goal_dir, "locations.csv")
                        df = pd.DataFrame(data=big_dict)
                        df.to_csv(dir_out)
                        exit()
                    except KeyError as ex:
                        if data['data']:
                            for obj in data['data']:
                                if obj['destination'] not in locations:
                                    locations.append(obj['destination'])
                            big_dict[int(year)][state].extend(locations)
            except KeyError as ex:
                continue

        dir_out = os.path.join(goal_dir, "locations.csv")
        df = pd.DataFrame(data=big_dict)
        df.to_csv(dir_out)
