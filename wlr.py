import json
import requests
import logging
import uuid
import os
import csv
import pendulum
import peewee
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import sqlite3 as sql

logger = logging.getLogger("wlr")

class WlrAPI(object):
    def __init__(self, key):
        self.key = key
        #self.Update()

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
                print(urlrbl)
            for arg in args:
                if isinstance(arg, str):
                   urlti += arg + "&activateTrafficInfo="
            url = "https://www.wienerlinien.at/ogd_realtime/monitor?"
            url += urlrbl
            url += urlti
            url += "&sender=" + self.key
            print(url)
            response = requests.get(url)
            return json.loads(response.content)

    def __downloadBaseData(self, filename, url):
        response = requests.get(url, stream=True)
        try:
            handle = open(filename, "wb")
            for chunk in response.iter_content(chunk_size=512):
                if chunk:  # filter out keep-alive new chunks
                    handle.write(chunk)        
        except:
            logger.error("Cannot open %s", filename)

    def __fullUpdate(self):
        self.__downloadBaseData("haltestellen.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-haltestellen.csv")
        self.__downloadBaseData("linien.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-linien.csv")
        self.__downloadBaseData("steige.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-steige.csv")

    def __LastChange(self, option, *args):
        if option == "w":
            with open('last_change.txt', 'w') as file:
                file.write(str(args[0]))
        elif option == "r":
            with open('last_change.txt', 'r') as file:
                lastchange = pendulum.parse(str(file.readline()), tz="Europe/Vienna")
                #lastchange = file.readline()
                return lastchange
        else:
            return False

    def Update(self):
        today = pendulum.now(tz="Europe/Vienna")
        line_count = int()
        self.__downloadBaseData("version.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-version.csv")
        logger.info("Check for latest version")
        with open('version.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
            for row in csv_reader:
                if line_count > 0:
                    gueltig_ab = pendulum.parse(row[0], tz='Europe/Vienna')
                    #erstellt_am = pendulum.parse(row[1], tz='Europe/Vienna')
                line_count += 1
        if gueltig_ab > self.__LastChange("r"):
            self.__fullUpdate()
            # TODO: Import CSV into local database
