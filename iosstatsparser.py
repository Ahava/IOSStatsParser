import json
from pprint import pprint

statsfile = "demofile.json"

with open(statsfile) as datafile:
    statsdata = json.load(datafile)



for player in statsdata["matchData"]["players"]:
    pprint(player["info"]["steamId"])

print(statsdata["matchData"]["matchInfo"]["periods"])

