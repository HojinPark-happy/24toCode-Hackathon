import pandas as pd
from datetime import datetime
import os
from pathlib import Path
import json
import string
from collections import namedtuple


def add_nozzle_key(row):
    plant = str(row['xml_tag_nm']).split('-')[2]
    machine = str(row['User_Name'])
    product_id = str(row['Product_ID'])
    changer = str(row['location']).split(',')[1]
    hole = str(int(row['location'].split(',')[2]) + 1)

    temp = [plant, machine, product_id, changer, hole]

    nozzle_key = '-'.join(temp)

    return nozzle_key.replace('.upf', '')


def process_data(df):
    df['nozzle_key'] = df.apply(add_nozzle_key, axis=1)

    aggregations = {
        'ulpicks': sum,
        'ulRejects': sum,
        'ulplacements': sum,
        'Date_Time': 'first',
    }

    df = df.groupby(['nozzle_key']).agg(aggregations)

    # n.b. nozzile_key included because of aggregations
    df.columns = ['picks', 'rejects', 'placements', 'date_time']

    df['reject_sum_perc'] = df['rejects'] / (df['placements'] + df['rejects'])
    df['reject_factor'] = df['rejects'] * df['reject_sum_perc']

    return df


def add_messages(jsonmessages):
    messages = []

    for message in jsonmessages:
        messages.append(message)

    return messages


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


# def json2obj(data):
#   return json.loads(data, object_hook=_json_object_hook)
def json2obj(fi):
    return json.load(fi, object_hook=_json_object_hook)


def test_failing(df):
    """
    Test for if nozzle is failing or will fail

    1. pick < placement, failing
    2. reject_factor > 0.2, failing
    3. count(rejects in time order) > 4, failing
    """
    f1 = df[(df.picks > df.placements)]
    print("Failing: picks < placement\n"
          "=========================")
    print(f1, '\n')

    f2 = df[(df.reject_factor > 0.2)]
    print("Failing: reject_factor > 0.2\n"
          "==============================")
    print(f2, '\n')


if __name__ == '__main__':
#    p = Path("/Users/Hojin Park/Desktop/HAck/a")
    p = Path(".")

    f = (p / "101.json").open()
    data1 = json2obj(f)
    df1 = pd.DataFrame(data1)
    # data collection
    filelists = list((p / "raw_splitfiles").iterdir())
    for i in range(3, 12):
        g = filelists[i].open()
        data2 = json2obj(g)
        df2 = pd.DataFrame(data2)
        df1 = df1.append(df2)
    # rawIn = s.read()
    # rawIn = sys.argv[1]  # first arg

    # df1 is the dataframe, you can filter data from it
    # if pick is lower than placement, warning
    # if reject factor is bigger than 0.2, warning
    # if there is more than 5 successive rejects, warning

    p = process_data(df1)

    test_failing(p)

    # draw graph!
    # p.plot.scatter(x='reject_factor', y='rejects')


    # need to print all rows and columns of dataframe
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    # print(p)
#     print(p.to_json(orient='records'))
# return p.to_json(orient='records')

# df = pd.DataFrame(inputFromPipe)
# print('past DF')
# p = process_data(df)

# with open(r'C:\Users\ftedgeuser1\Downloads\OneDrive_2019-12-04\Broken down data\result\103.json', 'r') as f:
#    data = json2obj(f.read())
#    #print(data[0])
# df = pd.DataFrame(data)
# p = process_data(df)

# print(p)
