import json
from pprint import pprint

statsfile = "demofile.json"

with open(statsfile) as datafile:
    statsdata = json.load(datafile)

for event in statsdata["matchData"]["matchEvents"]:
    if not event["event"] == "(null)":
        print(
        event["event"], ",", 
        event["period"], ",",
        event["player1SteamId"], ",",
        event["player2SteamId"], ",", 
        event["second"], ",",
        event["team"],
        "\n", sep='')


#for player in statsdata["matchData"]["players"]:
    #pprint(player["info"]["steamId"])

#print(statsdata["matchData"]["matchInfo"]["periods"])

