from wlr import WlrAPI as wlrAPI
import pprint

# instantiate the Wiener Linien Remote API
# Get your own API Key here: 
wlr = wlrAPI("Mu3YsSe2HHik42Jg")
#
# at least once a day run wlr.update()
# it checks if a newer version of the data is available
# The Update command additionally saves the csv in a local sqlite
# database for future reference
#     wlr.Update()
#
# -----------------------------------------------------------------------------------
# Monitor:
# -----------------------------------------------------------------------------------
# Current Updates for a given Station.
# Possible values are:
# - List of Stations with their RLP Number
# - List of possible message types:
#   + 'stoerunglang'
#   + 'stoerungkurz'
# 
# a mix of the values is also possible
#
#     wlr.Monitor(147, "stoerungkurz")
#     wlr.Monitor(250, 271, "stoerungkurz", "stoerunglang")
#
# This function will not parse the JSON Object.
# If you need specific Data like departure times only,
# pleasse call getDepartures().
#
# -----------------------------------------------------------------------------------
# SearchStation:
# -----------------------------------------------------------------------------------
# Returns a JSON Object of Stations with the given searchterm
# the number represents the matching quality:
# 0 would be completely different
# 100 would be an exact match
# >50 will deliver searchresults, even with typos
# >80 will narrow down the searchresult to a few result
#
#     wlr.SearchStation("zentralfriedhof", 85)
#     wlr.SearchStation("alpertgasse", 90)
#
# -----------------------------------------------------------------------------------
# GetRBL:
# -----------------------------------------------------------------------------------
# Returns a JSON Object with RBL-Number and Line-Name:
#     wlr.GetRBL("Albertgasse")
#
# -----------------------------------------------------------------------------------
# GetDepartures:
# -----------------------------------------------------------------------------------
# Returns a JSON Object with the next departure times
# for the given station:
#
#     wlr.GetDepartures(250)

pprint.pprint(wlr.monitor(250, 271, "stoerungkurz"), indent=1)
