# coding=utf-8
# This is a sample Python script.
import xml.etree.ElementTree as ET
import json
import numpy as np
import datetime
from pytz import timezone


def xml_parser(data_path, x, y):
    # 1. Create a python method that takes arguments int X and int Y,
    # and updates DEPART and RETURN fields
    # in test_payload1.xml:
    # - DEPART gets set to X days in the future from the current date
    # (whatever the current date is at the moment of executing the code)
    # - RETURN gets set to Y days in the future from the current date
    # Please write the modified XML to a new file.

    if x < 0 or y < 0:
        return
    tree = ET.parse(data_path)
    root = tree.getroot()

    date_format = '%Y%m%d'
    date = datetime.datetime.now()

    date_depart = date + datetime.timedelta(days=x)
    date_return = date + datetime.timedelta(days=y)

    tree.find(".//DEPART").text = date_depart.strftime(date_format)
    tree.find(".//RETURN").text = date_return.strftime(date_format)

    tree_new = ET.ElementTree(root)
    tree_new.write("data/test_payload2.xml")


def json_parser(data_path, object):
    # 2. Create a python method that takes a json element
    # as an argument, and removes that element from test_payload.json.
    #
    # (try removing "outParams" and "appdate").
    # Please write the modified json to a new file.

    obj = json.load(open(data_path))
    print(type(obj['outParams']))

    for i in range(len(obj['outParams'])):
        if obj['outParams'][i] == object:
            obj['outParams'].pop(i)
            break
    for key in obj['inParams']:
        if key == object:
            obj['inParams'].pop(key)
            break
    for key in obj:
        if key == object:
            obj.pop(key)
            break
    print(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    print(json.dumps(obj))
    open('data/' + object + '_' + "test_payload.json", "w"
         ).write(json.dumps(obj, indent=4, separators=(',', ': ')))

def csv_parser(data_path):
    # 3. Create a python script that parses jmeter log files in CSV format,
    # and in the case if there are any non-successful endpoint responses recorded in the log,
    # prints out the label, response code, response message, failure message,
    # and the time of non-200 response in human-readable format in PST timezone
    # (e.g. 2021-02-09 06:02:55 PST).
    types = ['u8', 'i4', 'U256', 'i4', 'U256', 'U256', 'U256', 'U256', 'U256', 'i4', 'i4', 'i4', 'i4', 'U256', 'i4',
             'i4', 'i4']
    data = np.genfromtxt(data_path, dtype=types, delimiter=',', names=True)

    print('label, response code, response message, failure message,time')
    for x in data:
        if str(x[7]) != 'true' and x[3] != 200:
            timestamp = x[0]
            datetime_sec = datetime.datetime.fromtimestamp(timestamp / 1e3)

            datetime_pacific = timezone('US/Pacific').localize(datetime_sec)
            date_pst = datetime_pacific.strftime("%Y-%m-%d %H:%M:%S %Z")
            print(date_pst + "," + str(x[2]) + "," + str(x[3]) + "," + str(x[4]) + "," + str(x[8]))


if __name__ == '__main__':

    # task 1
    xml_parser('data/test_payload1.xml', 1, 2)

    # task 2
    json_parser('data/test_payload.json', "outParams")
    json_parser('data/test_payload.json', "appdate")
    json_parser('data/test_payload.json', "spreadsheetName")
    json_parser('data/test_payload.json', "sessionId")
    json_parser('data/test_payload.json', "dateeff")
    json_parser('data/test_payload.json', "inParams")

    # task 3
    csv_parser('data/Jmeter_log1.jtl')
    csv_parser('data/Jmeter_log2.jtl')
