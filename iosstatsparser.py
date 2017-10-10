import json
import steamapi
import configparser

# Read config file
config = configparser.ConfigParser()
config.read("config.ini")

# Set variables and read them from config file
statsfile = "2017.10.08_19h.58m.01s_nextgen-vs-natural.talent_10-0.json"
steamapikey = config["Steam"]['ApiKey']
convertsteamid = config["Steam"].getboolean('ConvertSteamId')

# Load json file
with open(statsfile, 'r', encoding='utf-8') as datafile:
    statsdata = json.load(datafile)

# Open csv for writing
csvfile = open('stats.csv', 'w', newline='', encoding='utf-8')

# Print seperator so office automatically opens the file correctly
print("sep=,", file=csvfile)

# Taken from https://stackoverflow.com/questions/36463687/how-can-i-get-a-steamid-64-from-a-steamid-in-python
# Converts a normal steamid to it's 64bit version
def steamid_to_64bit(steamid):
    steam64id = 76561197960265728 # I honestly don't know where
                                    # this came from, but it works...
    id_split = steamid.split(":")
    steam64id += int(id_split[2]) * 2 # again, not sure why multiplying by 2...
    if id_split[1] == "1":
        steam64id += 1
    return steam64id

# Queries the Steam API to get a players name from the 64bit steamid
def steamid_to_name(steamid64):
    # Authenticate with the Steamapi
    steamapi.core.APIConnection(api_key=steamapikey, validate_key=True)
    # Return players name
    return steamapi.user.SteamUser(steamid64).name

def eventData():
    # Print header row 
    print(
        "Event",
        "Second",
        "Period",
        "Player 1 Steamid",
        "Player 1 Name",
        "Player 2 Steamid",
        "Player 2 Name",
        "Team",
        sep=',',
        file=csvfile
    )

    # Loop through all of the events
    for event in statsdata["matchData"]["matchEvents"]:
        # Sort out (null) events
        if not event["event"] == "(null)":

            # Create 2 empty strings for players name so print doesn't error
            player1Name = ""
            player2Name = ""

            # Convert the Steamid to strings
            player1SteamId = str(event["player1SteamId"])
            player2SteamId = str(event["player2SteamId"])

            # Convert the steamapi to the username if set to true in config
            if convertsteamid:
                if player1SteamId:
                    player1Name = steamid_to_name(steamid_to_64bit(player1SteamId))
                if player2SteamId:
                    player2Name = steamid_to_name(steamid_to_64bit(player2SteamId))

            # Print the event stats
            print(
                event["event"],
                event["second"],
                event["period"],
                player1SteamId,
                player1Name,
                player2SteamId,
                player2Name,
                event["team"], 
                sep=',',
                file=csvfile
            )
    
    # Print a newline to seperate different statistic sets
    print("\n", file=csvfile)

def teamData():
    # Print header row 
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
        sep=",",
        file=csvfile
    )

    # Iterate through overall team results in stats object
    for teams in statsdata["matchData"]["teams"]:
        # Create empty new string totalstats in which the stats are being written into
        totalstats = ""
        # Get variables from object and convert them to string
        name = str(teams["matchTotal"]["name"])
        side = str(teams["matchTotal"]["side"])
        isMix = str(teams["matchTotal"]["isMix"])

        # Assemble first set of totalstats
        totalstats = name + "," + side + "," + isMix + ","

        # Iterate through all the statistics
        for stat in teams["matchTotal"]["statistics"]:
            # Convert the statistic to a string
            statsstring = str(stat)
            # Replace spaces for formatting
            statsstring.replace(" ", "")
            # Add the statistic to totalstring
            totalstats = totalstats + statsstring + ","

        #Remove trailing comma from totalstats
        totalstats = totalstats[:-1]
        print(totalstats, file=csvfile)

    # Print a newline to seperate different statistic sets
    print("\n", file=csvfile)

def playerData():
    # Print header row 
    print(
        "Player Name",
        "Steam ID",
        "Position",
        "Team",
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
        sep=",",
        file=csvfile
    )

    # Iterate through all player stats in stats object
    for player in statsdata["matchData"]["players"]:
        # Set name and Steam ID
        name = str(player["info"]["name"])
        steamId = str(player["info"]["steamId"])
        
        # Set empty variables to be set later
        position = ""
        team = ""
        totalstats = ""
        statistics = []

        # Iterate through the different match periods
        for period in player["matchPeriodData"]:
            # Get position and team
            position = period["info"]["position"]
            team = period["info"]["team"]
            
            # Assign the first statistics array to the statistics variable if it is empty
            if not statistics:
                statistics = period["statistics"]
            else:
                # If it is not empty, combine the two arrays into one
                statistics = [x + y for x, y in zip(statistics, period["statistics"])]

        # Assign first batch of statistics to totalstats variable
        totalstats = name + "," + steamId + "," + position + "," + team + ","

        # Iterate through all the statistics
        for stat in statistics:
            # Convert the statistic to a string
            statsstring = str(stat)
            # Replace spaces for formatting
            statsstring.replace(" ", "")
            # Add the statistic to totalstats
            totalstats = totalstats + statsstring + ","


        #Remove trailing comma from totalstats
        totalstats = totalstats[:-1]
        print(totalstats, file=csvfile)
    
    print("\n", file=csvfile)

playerData()
eventData()
teamData()
