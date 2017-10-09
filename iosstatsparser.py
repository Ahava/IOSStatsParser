import json
from pprint import pprint

statsfile = "demofile.json"

with open(statsfile) as datafile:
    statsdata = json.load(datafile)


def eventData():
    for event in statsdata["matchData"]["matchEvents"]:
        if not event["event"] == "(null)":
            print(
                event["event"],
                event["period"],
                event["player1SteamId"],
                event["player2SteamId"],
                event["second"],
                event["team"], 
                sep=','
            )
    
    print("\n")

def teamData():
    print(
        "Team Name",
        "Side",
        "Is Mix",
        "Red Cards",
        "Yellow Cards",
        "Fouls",
        "Fouls Suffered",
        "Sliding Tackles",
        "Sliding Tackles Completed",
        "Goals Conceded",
        "Shots",
        "Shots on Goal",
        "Passes Completed",
        "Interceptions",
        "Offsides",
        "Goals",
        "Own Goals",
        "Assists",
        "Passes",
        "Free Kicks",
        "Penalties",
        "Corners",
        "Throw Ins",
        "Keeper Saves",
        "Goal Kicks",
        "Possession",
        "Distance Covered",
        "Keeper Saves Caught",
        sep=","
    )

    for teams in statsdata["matchData"]["teams"]:
        totalstats = ""
        name = str(teams["matchTotal"]["name"])
        side = str(teams["matchTotal"]["side"])
        isMix = str(teams["matchTotal"]["isMix"])

        totalstats = name + "," + side + "," + isMix + ","


        for stat in teams["matchTotal"]["statistics"]:
            statsstring = str(stat)
            statsstring.replace(" ", "")
            totalstats = totalstats + statsstring + ","

        totalstats = totalstats[:-1]
        print(totalstats)

    print("\n")

eventData()
teamData()

#for player in statsdata["matchData"]["players"]:
    #pprint(player["info"]["steamId"])

#print(statsdata["matchData"]["matchInfo"]["periods"])

