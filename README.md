# WLR-API

Python wrapper for the Wiener Linien API.

## Install

First get a developer api key here: https://go.gv.at/l9ogdechtzeitdatenwienerlinienkeyanforderung. 
The wrapper will work in python >3.5, not tested in <3.5.

```
git clone https://github.com/faulander/wlr-api.git
cd wlr-api
pip install -r requirements.txt
```
For example usage please check 'examples.py'.

## Examples

### Update:
At least once a day the update command should be run. It checks the Wiener Linien API for new data and fills the local database with them. On the first run it doesn't need to be called extra, it's being done automatically.

```
wlr.Update()
```

### Monitor:
Current Updates for a given Station.
Possible values are:
  - List of Stations with their RLP Number
  - List of possible message types:
    + 'stoerunglang'
    + 'stoerungkurz'
 
  a mix of the values is also possible

```
      wlr.Monitor(147, "stoerungkurz")
      wlr.Monitor(250, 271, "stoerungkurz", "stoerunglang")
```
  This function will not parse the JSON Object.
  If you need specific Data like departure times only,
  pleasse call getDepartures().

### SearchStation:

  Returns a JSON Object of Stations with the given searchterm
  the number represents the matching quality:
  0 would be completely different
  100 would be an exact match

 ```
      wlr.SearchStation("zentralfriedhof", 85)
      wlr.SearchStation("alpertgasse", 90)
 ```
### GetRBL:

  Returns a JSON Object with RBL-Number and Line-Name:

```
      wlr.GetRBL("Albertgasse")
 ```
### GetDepartures:

  Returns a JSON Object with the next departure times
  for the given station:

```
      wlr.GetDepartures(250)
```
### GetTrafficInfoList:
  Returns a JSON Object with traffic Information for the given lines.
  If no line is provided, all traffic info is delivered.

```
     wlr.GetTrafficInfoList("relatedLine=2", "relatedLine=U6")
     wlr.GetTrafficInfoList()
```

## TODO:
+ If Realtime data is available, deliver it. Otherwise deliver planned data.
+ New method to deliver all data around a given location
+ Method "trafficinfolist"
+ Method "newlist"
