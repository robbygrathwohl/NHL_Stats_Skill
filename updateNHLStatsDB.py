from __future__ import print_function
import urllib 
import httplib
import base64
import string
import json
import boto3

''' Sample dummy data
sample_player = {
  "Abbreviation": "FLO",
  "Age": "44",
  "Assists": "4",
  "BirthCity": "Kladno",
  "BirthCountry": "Czechoslovakia",
  "BirthDate": "1972-02-15",
  "City": "Florida",
  "FaceoffLosses": "3",
  "FaceoffPercent": "33.3",
  "Faceoffs": "5",
  "FaceoffWins": "3",
  "FirstName": "Jaromir",
  "GamesPlayed": "10",
  "GameTyingGoals": "0",
  "GameWinningGoals": "1",
  "Goals": "4",
  "HatTricks": "0",
  "Height": "6'3\"",
  "Hits": "4",
  "IsRookie": "false",
  "JerseyNumber": "68",
  "LastName": "Jagr",
  "Penalties": "0",
  "PenaltyMinutes": "13",
  "playerID": "2",
  "PowerplayAssists": "0",
  "PlusMinus": "0",
  "Points": "8",
  "Position": "RW",
  "PowerplayGoals": "0",
  "ShorthandedAssists": "1",
  "ShorthandedGoals": "0",
  "ShorthandedPoints": "1",
  "ShotPercentage": "11.4",
  "Shots": "0",
  "TeamID": "4",
  "TeamName": "Panthers",
  "Weight": "230"
}

"Stats": {
    "Abbreviation": { "Action": "PUT", "Value":{"S": player["Abbreviation"]}},
    "Age": { "Action": "PUT", "Value":{"S": player["Age"]}},
    "Assists": { "Action": "PUT", "Value":{"S": player["Assists"]}},
    "BirthCity": { "Action": "PUT", "Value":{"S": player["BirthCity"]}},
    "BirthCountry": { "Action": "PUT", "Value":{"S": player["BirthCountry"]}},
    "BirthDate": { "Action": "PUT", "Value":{"S": player["BirthDate"]}},
    "City": { "Action": "PUT", "Value":{"S": player["City"]}},
    "FaceoffLosses": { "Action": "PUT", "Value":{"S": player["FaceoffLosses"]}},
    "FaceoffPercent": { "Action": "PUT", "Value":{"S": player["FaceoffPercent"]}},
    "Faceoffs": { "Action": "PUT", "Value":{"S": player["Faceoffs"]}},
    "FaceoffWins": { "Action": "PUT", "Value":{"S": player["FaceoffWins"]}},
    "FirstName": { "Action": "PUT", "Value":{"S": player["FirstName"]}},
    "GamesPlayed": { "Action": "PUT", "Value":{"S": player["GamesPlayed"]}},
    "GameTyingGoals": { "Action": "PUT", "Value":{"S": player["GameTyingGoals"]}},
    "GameWinningGoals": { "Action": "PUT", "Value":{"S": player["GameWinningGoals"]}},
    "Goals": { "Action": "PUT", "Value":{"S": player["Goals"]}},
    "HatTricks": { "Action": "PUT", "Value":{"S": player["HatTricks"]}},
    "Height": { "Action": "PUT", "Value":{"S": player["Height"]}},
    "Hits": { "Action": "PUT", "Value":{"S": player["Hits"]}},
    "IsRookie": { "Action": "PUT", "Value":{"S": player["IsRookie"]}},
    "JerseyNumber": { "Action": "PUT", "Value":{"S": player["JerseyNumber"]}},
    "LastName": { "Action": "PUT", "Value":{"S": player["LastName"]}},
    "Penalties": { "Action": "PUT", "Value":{"S": player["Penalties"]}},
    "PenaltyMinutes": { "Action": "PUT", "Value":{"S": player["PenaltyMinutes"]}},
    "PowerplayAssists": { "Action": "PUT", "Value":{"S": player["PowerplayAssists"]}},
    "PlusMinus": { "Action": "PUT", "Value":{"S": player["PlusMinus"]}},
    "Points": { "Action": "PUT", "Value":{"S": player["Points"]}},
    "Position": { "Action": "PUT", "Value":{"S": player["Position"]}},
    "PowerplayGoals": { "Action": "PUT", "Value":{"S": player["PowerplayGoals"]}},
    "ShorthandedAssists": { "Action": "PUT", "Value":{"S": player["ShorthandedAssists"]}},
    "ShorthandedGoals": { "Action": "PUT", "Value":{"S": player["ShorthandedGoals"]}},
    "ShorthandedPoints": { "Action": "PUT", "Value":{"S": player["ShorthandedPoints"]}},
    "ShotPercentage": { "Action": "PUT", "Value":{"S": player["ShotPercentage"]}},
    "Shots": { "Action": "PUT", "Value":{"S": player["Shots"]}},
    "TeamID": { "Action": "PUT", "Value":{"S": player["TeamID"]}},
    "TeamName": { "Action": "PUT", "Value":{"S": player["TeamName"]}},
    "Weight": { "Action": "PUT", "Value":{"S": player["Weight"]}}
}

{
    "Abbreviation": { "Action": "PUT", "Value": player["Abbreviation"]},
    "Age": { "Action": "PUT", "Value": player["Age"]},
    "Assists": { "Action": "PUT", "Value": player["Assists"]},
    "BirthCity": { "Action": "PUT", "Value": player["BirthCity"]},
    "BirthCountry": { "Action": "PUT", "Value": player["BirthCountry"]},
    "BirthDate": { "Action": "PUT", "Value": player["BirthDate"]},
    "City": { "Action": "PUT", "Value": player["City"]},
    "FaceoffLosses": { "Action": "PUT", "Value": player["FaceoffLosses"]},
    "FaceoffPercent": { "Action": "PUT", "Value": player["FaceoffPercent"]},
    "Faceoffs": { "Action": "PUT", "Value": player["Faceoffs"]},
    "FaceoffWins": { "Action": "PUT", "Value": player["FaceoffWins"]},
    "FirstName": { "Action": "PUT", "Value": player["FirstName"]},
    "GamesPlayed": { "Action": "PUT", "Value": player["GamesPlayed"]},
    "GameTyingGoals": { "Action": "PUT", "Value": player["GameTyingGoals"]},
    "GameWinningGoals": { "Action": "PUT", "Value": player["GameWinningGoals"]},
    "Goals": { "Action": "PUT", "Value": player["Goals"]},
    "HatTricks": { "Action": "PUT", "Value": player["HatTricks"]},
    "Height": { "Action": "PUT", "Value": player["Height"]},
    "Hits": { "Action": "PUT", "Value": player["Hits"]},
    "IsRookie": { "Action": "PUT", "Value": player["IsRookie"]},
    "JerseyNumber": { "Action": "PUT", "Value": player["JerseyNumber"]},
    "LastName": { "Action": "PUT", "Value": player["LastName"]},
    "Penalties": { "Action": "PUT", "Value": player["Penalties"]},
    "PenaltyMinutes": { "Action": "PUT", "Value": player["PenaltyMinutes"]},
    "PowerplayAssists": { "Action": "PUT", "Value": player["PowerplayAssists"]},
    "PlusMinus": { "Action": "PUT", "Value": player["PlusMinus"]},
    "Points": { "Action": "PUT", "Value": player["Points"]},
    "Position": { "Action": "PUT", "Value": player["Position"]},
    "PowerplayGoals": { "Action": "PUT", "Value": player["PowerplayGoals"]},
    "ShorthandedAssists": { "Action": "PUT", "Value": player["ShorthandedAssists"]},
    "ShorthandedGoals": { "Action": "PUT", "Value": player["ShorthandedGoals"]},
    "ShorthandedPoints": { "Action": "PUT", "Value": player["ShorthandedPoints"]},
    "ShotPercentage": { "Action": "PUT", "Value": player["ShotPercentage"]},
    "Shots": { "Action": "PUT", "Value": player["Shots"]},
    "TeamID": { "Action": "PUT", "Value": player["TeamID"]},
    "TeamName": { "Action": "PUT", "Value": player["TeamName"]},
    "Weight": { "Action": "PUT", "Value": player["Weight"]}
}


'''


# ----------------- Calls to Stats API -----------------


def get_players_stats():

    host = "www.mysportsfeeds.com"
    url = "/api/feed/pull/nhl/current/cumulative_player_stats.json?&force=true"
    f=open("/authentication/account.txt","r")
    lines=f.readlines()
    username=lines[0]
    password=lines[1]
    f.close()
    # base64 encode the username and password
    auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    webservice = httplib.HTTPS(host)
    # write your headers
    webservice.putrequest("GET", url)
    webservice.putheader("Host", host)
    webservice.putheader("User-Agent", "Python http auth")
    webservice.putheader("Content-type", "text/html; charset=\"UTF-8\"")
    # write the Authorization header like: 'Basic base64encode(username + ':' + password)
    webservice.putheader("Authorization", "Basic %s" % auth)
    webservice.endheaders()
    statuscode, statusmessage, header = webservice.getreply()
    print(statusmessage)

    all_players_stats = json.loads(webservice.getfile().read())
    players_stats = []
    for player in all_players_stats['cumulativeplayerstats']['playerstatsentry']:
        players_stats.append(player)

    return players_stats

# ----------------- Formatting Functions -----------------

def package_players_for_dynamodb(players_stats):

    packaged_players_stats = []
    for player in players_stats:
        sample_player = {
            "Abbreviation": " ",
            "Age": " ",
            "Assists": " ",
            "BirthCity": " ",
            "BirthCountry": " ",
            "BirthDate": " ",
            "City": " ",
            "FaceoffLosses": " ",
            "FaceoffPercent": " ",
            "Faceoffs": " ",
            "FaceoffWins": " ",
            "FirstName": " ",
            "GamesPlayed": " ",
            "GameTyingGoals": " ",
            "GameWinningGoals": " ",
            "Goals": " ",
            "HatTricks": " ",
            "Height": " ",
            "Hits": " ",
            "IsRookie": " ",
            "JerseyNumber": " ",
            "LastName": " ",
            "Penalties": " ",
            "PenaltyMinutes": " ",
            "playerID": " ",
            "PowerplayAssists": " ",
            "PlusMinus": " ",
            "Points": " ",
            "Position": " ",
            "PowerplayGoals": " ",
            "ShorthandedAssists": " ",
            "ShorthandedGoals": " ",
            "ShorthandedPoints": " ",
            "ShotPercentage": " ",
            "Shots": " ",
            "TeamID": " ",
            "TeamName": " ",
            "Weight": " "
        }
        #print(player)
        sample_player["Abbreviation"] = player["team"]["Abbreviation"]
        if "Age" in player["player"]:
            sample_player["Age"] = player["player"]["Age"]
        else:
            sample_player["Age"] = "Not Available"
        if "Assists" in player["stats"]["stats"]:
            sample_player["Assists"] = player["stats"]["stats"]["Assists"]["#text"]
        else:
            sample_player["Assists"] = "Not Available"
        if "BirthCity" in player["player"]:
            sample_player["BirthCity"] = player["player"]["BirthCity"]
        else:
            sample_player["BirthCity"] = "Not Available"
        if "BirthCountry" in player["player"]:
            sample_player["BirthCountry"] = player["player"]["BirthCountry"]
        else:
            sample_player["BirthCountry"] = "Not Available"
        if "BirthDate" in player["player"]:
            sample_player["BirthDate"] = player["player"]["BirthDate"]
        else:
            sample_player["BirthDate"] = "Not Available"
        sample_player["City"] = player["team"]["City"]
        if "FaceoffLosses" in player["stats"]["stats"]:
            sample_player["FaceoffLosses"] = player["stats"]["stats"]["FaceoffLosses"]["#text"]
        else:
            sample_player["FaceoffLosses"] = "Not Available"
        if "FaceoffPosses" in player["stats"]["stats"]:
            sample_player["FaceoffPercent"] = player["stats"]["stats"]["FaceoffPercent"]["#text"]
        else:
            sample_player["FaceoffPercent"] = "Not Available"
        if "Faceoffs" in player["stats"]["stats"]:
            sample_player["Faceoffs"] = player["stats"]["stats"]["Faceoffs"]["#text"]
        else:
            sample_player["Faceoffs"] = "Not Available"
        if "FaceoffWins" in player["stats"]["stats"]:
            sample_player["FaceoffWins"] = player["stats"]["stats"]["FaceoffWins"]["#text"]
        else:
            sample_player["FaceoffWins"] = "Not Available"
        sample_player["FirstName"] = player["player"]["FirstName"]
        if "GamesPlayed" in player["stats"]:
            sample_player["GamesPlayed"] = player["stats"]["GamesPlayed"]["#text"]
        else:
            sample_player["GamesPlayed"] = "Not Available"
        if "GameTyingGoals" in player["stats"]["stats"]:
            sample_player["GameTyingGoals"] = player["stats"]["stats"]["GameTyingGoals"]["#text"]
        else:
            sample_player["GameTyingGoals"] = "Not Available"
        if "GameWinningGoals" in player["stats"]["stats"]:
            sample_player["GameWinningGoals"] = player["stats"]["stats"]["GameWinningGoals"]["#text"]
        else:
            sample_player["GameWinningGoals"] = "Not Available"
        if "Goals" in player["stats"]["stats"]:
            sample_player["Goals"] = player["stats"]["stats"]["Goals"]["#text"]
        else:
            sample_player["Goals"] = "Not Available"
        if "HatTricks" in player["stats"]["stats"]:
            sample_player["HatTricks"] = player["stats"]["stats"]["HatTricks"]["#text"]
        else:
            sample_player["HatTricks"] = "Not Available"
        if "Height" in player["player"]:
            sample_player["Height"] = player["player"]["Height"]
        else:
            sample_player["Height"] = "Not Available"
        if "Hits" in player["stats"]["stats"]:
            sample_player["Hits"] = player["stats"]["stats"]["Hits"]["#text"]
        else:
            sample_player["Hits"] = "Not Available"
        if "IsRookie" in player["player"]:
            sample_player["IsRookie"] = player["player"]["IsRookie"]
        else:
            sample_player["IsRookie"] = "Not Available"
        if "JerseyNumber" in player["player"]:
            sample_player["JerseyNumber"] = player["player"]["JerseyNumber"]
        else:
            sample_player["JerseyNumber"] = "Not Available"
        sample_player["LastName"] = player["player"]["LastName"]
        if "Penalties" in player["stats"]["stats"]:
            sample_player["Penalties"] = player["stats"]["stats"]["Penalties"]["#text"]
        else:
            sample_player["Penalties"] = "Not Available"
        if "PenaltyMinutes" in player["stats"]["stats"]:
            sample_player["PenaltyMinutes"] = player["stats"]["stats"]["PenaltyMinutes"]["#text"]
        else:
            sample_player["PenaltyMinutes"] = "Not Available"
        sample_player["playerID"] = player["player"]["ID"]
        if "PowerplayAssists" in player["stats"]["stats"]:
            sample_player["PowerplayAssists"] = player["stats"]["stats"]["PowerplayAssists"]["#text"]
        else:
            sample_player["PowerplayAssists"] = "Not Available"
        if "PlusMinus" in player["stats"]["stats"]:
            sample_player["PlusMinus"] = player["stats"]["stats"]["PlusMinus"]["#text"]
        else:
            sample_player["PlusMinus"] = "Not Available"
        if "Points" in player["stats"]["stats"]:
            sample_player["Points"] = player["stats"]["stats"]["Points"]["#text"]
        else:
            sample_player["Points"] = "Not Available"
        if "Position" in player["player"]:
            sample_player["Position"] = player["player"]["Position"]
        else:
            sample_player["Position"] = "Not Available"
        if "PowerplayGoals" in player["stats"]["stats"]:
            sample_player["PowerplayGoals"] = player["stats"]["stats"]["PowerplayGoals"]["#text"]
        else:
            sample_player["PowerplayGoals"] = "Not Available"
        if "ShorthandedAssists" in player["stats"]["stats"]:
            sample_player["ShorthandedAssists"] = player["stats"]["stats"]["ShorthandedAssists"]["#text"]
        else:
            sample_player["ShorthandedAssists"] = "Not Available"
        if "ShorthandedGoals" in player["stats"]["stats"]:
            sample_player["ShorthandedGoals"] = player["stats"]["stats"]["ShorthandedGoals"]["#text"]
        else:
            sample_player["ShorthandedGoals"] = "Not Available"
        if "ShorthandedPoints" in player["stats"]["stats"]:
            sample_player["ShorthandedPoints"] = player["stats"]["stats"]["ShorthandedPoints"]["#text"]
        else:
            sample_player["ShorthandedPoints"] = "Not Available"
        if "ShotPercentage" in player["stats"]["stats"]:
            sample_player["ShotPercentage"] = player["stats"]["stats"]["ShotPercentage"]["#text"]
        else:
            sample_player["ShotPercentage"] = "Not Available"
        if "Shots" in player["stats"]["stats"]:
            sample_player["Shots"] = player["stats"]["stats"]["Shots"]["#text"]
        else:
            sample_player["Shots"] = "Not Available"
        sample_player["TeamID"] = player["team"]["ID"]
        sample_player["TeamName"] = player["team"]["Name"]
        if "Weight" in player["player"]:
            sample_player["Weight"] = player["player"]["Weight"]
        else:
            sample_player["Weight"] = "Not Available"
        packaged_players_stats.append(sample_player)
    
    return packaged_players_stats

def compile_attribute_updates(players_stats):
    compiled_updates = []
    for player in players_stats:
        compiled_attributes = {
            "Key" : { "playerID" : player["playerID"]},
            "TeamName" : { "Action": "PUT", "Value": player["TeamName"]},
            "City" : { "Action": "PUT", "Value": player["City"]},
            "JerseyNumber" : { "Action": "PUT", "Value": player["JerseyNumber"]},
            "FirstName" : { "Action": "PUT", "Value": player["FirstName"]},
            "LastName" : { "Action": "PUT", "Value": player["LastName"]},
            "Goals" : { "Action": "PUT", "Value": player["Goals"]},
            "Points" : { "Action": "PUT", "Value": player["Points"]},
            "Stats": { "Action": "PUT", "Value": {
                "Assists": player["Assists"],
                "FaceoffLosses": player["FaceoffLosses"],
                "FaceoffPercent": player["FaceoffPercent"],
                "Faceoffs": player["Faceoffs"],
                "FaceoffWins": player["FaceoffWins"],
                "GamesPlayed": player["GamesPlayed"],
                "GameTyingGoals": player["GameTyingGoals"],
                "GameWinningGoals": player["GameWinningGoals"],
                "Goals": player["Goals"],
                "HatTricks": player["HatTricks"],
                "Hits": player["Hits"],
                "Penalties": player["Penalties"],
                "PenaltyMinutes": player["PenaltyMinutes"],
                "PowerplayAssists": player["PowerplayAssists"],
                "PlusMinus": player["PlusMinus"],
                "Points": player["Points"],
                "PowerplayGoals": player["PowerplayGoals"],
                "ShorthandedAssists": player["ShorthandedAssists"],
                "ShorthandedGoals": player["ShorthandedGoals"],
                "ShorthandedPoints": player["ShorthandedPoints"],
                "ShotPercentage": player["ShotPercentage"],
                "Shots": player["Shots"]
                }
            },
            "PlayerInfo": {"Action": "PUT", "Value": {
                "Age": player["Age"],
                "BirthCity": player["BirthCity"],
                "BirthCountry": player["BirthCountry"],
                "BirthDate": player["BirthDate"],
                "FirstName": player["FirstName"],
                "Height": player["Height"],
                "IsRookie": player["IsRookie"],
                "JerseyNumber": player["JerseyNumber"],
                "LastName": player["LastName"],
                "Position": player["Position"],
                "Weight": player["Weight"]
                }
            },
            "TeamInfo": { "Action": "PUT", "Value": {
                "City": player["City"],
                "TeamID": player["TeamID"],
                "TeamName": player["TeamName"]
                }
            }
        }
        compiled_updates.append(compiled_attributes)
    
    return compiled_updates

# ----------------- Writes to Database -----------------

def update_players_stats_db(table_player_stats, compiled_updates_players_stats, counter):
    for update_item in compiled_updates_players_stats:
        counter = counter +1
        response = table_player_stats.update_item( Key = {'playerID' : update_item["Key"]["playerID"] }, AttributeUpdates = {
            "TeamName": update_item["TeamName"], "City": update_item["City"], "JerseyNumber": update_item["JerseyNumber"], "FirstName": update_item["FirstName"], "LastName": update_item["LastName"],
            "Goals": update_item["Goals"], "Points": update_item["Points"], "Stats": update_item["Stats"], "PlayerInfo": update_item["PlayerInfo"], "TeamInfo" : update_item["TeamInfo"]})
    return counter


# ------------------ Helper Functions ------------------



# ------------------ Main handler ---------------------
def lambda_handler(event, context):
    response = ""
    counter = 0
    players_stats = get_players_stats()
    packaged_players_stats = package_players_for_dynamodb(players_stats)
    compiled_updates_players_stats = compile_attribute_updates(packaged_players_stats)
    
    #dynamodb = boto3.client('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    table_player_stats = dynamodb.Table('PlayerStats')
    table_game_schedule = dynamodb.Table('GameSchedule')

    player_count = update_players_stats_db(table_player_stats, compiled_updates_players_stats, counter)
    print(player_count)
    
    return 'Hello from Lambda'