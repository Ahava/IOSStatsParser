import json
from pprint import pprint
import steamapi
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

statsfile = "demofile.json"
steamapikey = config["Steam"]['ApiKey']
convertsteamid = config["Steam"]['ConvertSteamId']

with open(statsfile) as datafile:
    statsdata = json.load(datafile)

# Taken from https://stackoverflow.com/questions/36463687/how-can-i-get-a-steamid-64-from-a-steamid-in-python
def steamid_to_64bit(steamid):
    steam64id = 76561197960265728 # I honestly don't know where
                                    # this came from, but it works...
    id_split = steamid.split(":")
    steam64id += int(id_split[2]) * 2 # again, not sure why multiplying by 2...
    if id_split[1] == "1":
        steam64id += 1
    return steam64id

def steamid_to_name(steamid64):
    steamapi.core.APIConnection(api_key=steamapikey, validate_key=True)
    return steamapi.user.SteamUser(steamid64).name

def eventData():
    print(
        "Event",
        "Period",
        "Player 1 Steamid",
        "Player 1 Name",
        "Player 2 Steamid",
        "Player 2 Name",
        "Second",
        "Team",
        sep=','
    )

    for event in statsdata["matchData"]["matchEvents"]:
        if not event["event"] == "(null)":

            player1Name = ""
            player2Name = ""

            if convertsteamid == True:
                player1SteamId = str(event["player1SteamId"])
                player2SteamId = str(event["player2SteamId"])

                if player1SteamId:
                    player1Name = steamid_to_name(steamid_to_64bit(player1SteamId))
                if player2SteamId:
                    player2Name = steamid_to_name(steamid_to_64bit(player2SteamId))

            print(
                event["event"],
                event["period"],
                event["player1SteamId"],
                player1Name,
                event["player2SteamId"],
                player2Name,
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

