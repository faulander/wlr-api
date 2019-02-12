# WLR-API

Python wrapper for the Wiener Linien API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Install

First get a developer api key here: https://go.gv.at/l9ogdechtzeitdatenwienerlinienkeyanforderung
The wrapper will work in python >3.5, not tested in <3.5.
```

git clone https://github.com/faulander/wlr-api.git
cd wlr-api
pip install -r requirements.txt
```

### Examples

## Monitor:
Current Updates for a given Station.
Possible values are:
  - List of Stations with their RLP Number
  - List of possible message types:
    + 'stoerunglang'
    + 'stoerungkurz'
 
  a mix of the values is also possible

      wlr.Monitor(147, "stoerungkurz")
      wlr.Monitor(250, 271, "stoerungkurz", "stoerunglang")

  This function will not parse the JSON Object.
  If you need specific Data like departure times only,
  pleasse call getDepartures().

## SearchStation:

  Returns a JSON Object of Stations with the given searchterm
  the number represents the matching quality:
  0 would be completely different
  100 would be an exact match
  >50 will deliver searchresults, even with typos
  >80 will narrow down the searchresult to a few result
 
      wlr.SearchStation("zentralfriedhof", 85)
      wlr.SearchStation("alpertgasse", 90)
 
## GetRBL:

  Returns a JSON Object with RBL-Number and Line-Name:
      wlr.GetRBL("Albertgasse")
 
## GetDepartures:

  Returns a JSON Object with the next departure times
  for the given station:

      wlr.GetDepartures(250)
