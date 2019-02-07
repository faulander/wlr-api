import os
import json
import requests
import logging
import uuid
import os
import csv
#import pendulum
from peewee import *
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
import sqlite3 as sql

db = SqliteDatabase('wlr.db')


class linie(object):
    LINIEN_ID = IntegerField()
    BEZEICHNUNG = CharField()
    REIHENFOLGE = IntegerField()
    ECHTZEIT = BooleanField()
    VERKEHRMITTEL = CharField()
    STAND = CharField()

    class Meta:
        database = db


class WlrAPI(object):
    def __init__(self, key):
        self.key = key
        self.__checkforUpdate()

    def monitor(self, *args):
        if len(args) == 0:
            return False
        else:
            urlrbl = "rbl="
            urlti = "&activateTrafficInfo="
            for arg in args:
                if isinstance(arg, int):
                    urlrbl += str(arg) + "&rbl="
            if urlrbl[-1:] == "=":
                urlrbl = urlrbl[:(len(urlrbl)-5)]
            for arg in args:
                if isinstance(arg, str):
                   urlti += arg + "&activateTrafficInfo="
            if urlti[-1:] == "=":
                urlti = urlti[:(len(urlti)-21)]
            url = "https://www.wienerlinien.at/ogd_realtime/monitor?"
            url += urlrbl
            url += urlti
            url += "&sender=" + self.key
            logger.info(url)
            response = requests.get(url)
            return json.loads(response.content)

    def __downloadBaseData(self, filename, url):
        print("Downloading", filename)
        response = requests.get(url, stream=True)
        try:
            handle = open(filename, "wb")
            for chunk in response.iter_content(chunk_size=512):
                if chunk:  # filter out keep-alive new chunks
                    handle.write(chunk)        
        except:
            print("Cannot open %s", filename)

    def __fullUpdate(self):
        print("Doing a full masterdata update")
        self.__downloadBaseData("haltestellen.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-haltestellen.csv")
        self.__downloadBaseData("linien.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-linien.csv")
        self.__downloadBaseData("steige.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-steige.csv")
        self.__updateDB()

    def __updateDB(self):
        # Read the csv and save it to the db
        with open('linien.csv') as linien:
            csv_reader = csv.reader(linien, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'\t{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}')
                    line_count += 1
            print(f'Processed {line_count} lines.')

    def __checkforUpdate(self):
        print("Checking if a full update is necessary")
        if not os.path.isfile('./wlr.db'):
                self.__fullUpdate()
        else:
            print("DB has been found, if necessary to a manual update")


    def Update(self):
        self.__fullUpdate()
        self.__updateDB()
