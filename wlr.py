import os
import json
import requests
import logging
import uuid
import os
import sys
import csv
#import pendulum
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
import sqlite3 as sql

class WlrAPI(object):
    def __init__(self, key):
        self.key = key
        self.__checkforUpdate()


    """
    -----------------------------------------------------------------------------------
                                  PRIVATE METHODS
    -----------------------------------------------------------------------------------
    """

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
        create_table_linien = """ CREATE TABLE linien (
                                        LINIEN_ID integer PRIMARY KEY,
                                        BEZEICHNUNG text,
                                        REIHENFOLGE integer,
                                        ECHTZEIT integer,
                                        VERKEHRSMITTEL text,
                                        STAND text
                                    ) """
        create_table_haltestellen = """ CREATE TABLE haltestellen (
                                        HALTESTELLEN_ID integer PRIMARY KEY,
                                        TYP text,
                                        DIVA integer,
                                        NAME text,
                                        GEMEINDE text,
                                        GEMEINDE_ID integer,
                                        WGS84_LAT text,
                                        WGS84_LON text, 
                                        STAND text
                                   ) """

        create_table_steige = """ CREATE TABLE steige (
                                        STEIG_ID integer PRIMARY KEY,
                                        FK_LINIEN_ID integer,
                                        FK_HALTESTELLEN_ID integer,
                                        RICHTUNG text,
                                        REIHENFOLGE integer,
                                        RBL_NUMMER integer,
                                        BEREICH integer,
                                        STEIG text,
                                        STEIG_WGS84_LAT text,
                                        STEIG_WGS84_LON text,
                                        STAND text
                                   ) """

        try: 
            con = sql.connect("./wlr.db")
            cur = con.cursor()
        except:
            print("Connecting to the database failed.")
            sys.exit(-1)
        try:
            cur.execute(create_table_linien)
            cur.execute(create_table_haltestellen)
            cur.execute(create_table_steige)
        except:
            print("Creating of tables failed")
            sys.exit(-1)
        # Read the csv and save it to the db
        #TODO WRITE haltestellen.csv
        #TODO WRITE steige.csv
        with open('linien.csv') as linien:
            csv_reader = csv.DictReader(linien, delimiter=';')
            to_db = [(i['LINIEN_ID'], i['BEZEICHNUNG'], i['REIHENFOLGE'], i['ECHTZEIT'], i['VERKEHRSMITTEL'], i['STAND']) for i in csv_reader]
            #print(to_db)
        cur.executemany("INSERT INTO linien (LINIEN_ID, BEZEICHNUNG, REIHENFOLGE, ECHTZEIT, VERKEHRSMITTEL, STAND) VALUES (?, ?, ?, ?, ?, ?)", to_db)
        con.commit()

    def __checkforUpdate(self):
        print("Checking if a full update is necessary")
        if not os.path.isfile('./wlr.db'):
                self.__fullUpdate()
        else:
            print("DB has been found, if necessary to a manual update")

    """
    -----------------------------------------------------------------------------------
                                  PUBLIC METHODS
    -----------------------------------------------------------------------------------
    """

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

    def Update(self):
        self.__fullUpdate()
        self.__updateDB()
