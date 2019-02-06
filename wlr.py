import json
import requests
import logging
import uuid
import os

logger = logging.getLogger("wlr")

# Key used for developing
key = "Mu3YsSe2HHik42Jg"
# Key used for production
# key = "8pKLaGwCurSyZrxe"

class WlrAPI(object):
    def __init__(self, key):
        self.key = key
        self.__checkUpdate()

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
        handle = open(filename, "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)        
    # TODO:  
    def update(self):
        self.__downloadBaseData("haltestellen.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-haltestellen.csv")
        self.__downloadBaseData("linien.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-linien.csv")
        self.__downloadBaseData("steige.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-steige.csv")
        self.__downloadBaseData("version.csv", "https://data.wien.gv.at/csv/wienerlinien-ogd-version.csv")

    # TODO: Download Version CSV and check if an update is necessary
    def __checkUpdate(self):
        pass