from wlr import WlrAPI as wlrAPI

# instantiate the Wiener Linien Remote API
# Get your own API Key here: 
wlr = wlrAPI("Mu3YsSe2HHik42Jg")

# at least once a day run wlr.update()
# it checks if a newer version of the data is available
# The Update command additionally saves the csv in a local sqlite
# database for future reference
#wlr.Update()

# Monitor:
# Current Updates for a given Station.
# Possible values are:
# - List of Stations with their RLP Number
# - List of possible message typs:
#   + 'stoerunglang'
#   + 'stoerungkurz'
# 
# a mix of the values is also possible
#
#wlr.monitor(147, "stoerungkurz")
#wlr.monitor(147, 192, 248, "stoerungkurz", "stoerunglang")

