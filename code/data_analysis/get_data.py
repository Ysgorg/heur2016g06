
def get_main_rows():

    import csv

    rows=[]

    with open('main_results.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader: rows.append(row)

    return rows

def get_val_time_data():

    import json
    with open('value_per_time.json') as json_data: return json.load(json_data)
