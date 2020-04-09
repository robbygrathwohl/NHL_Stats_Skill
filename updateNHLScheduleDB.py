from __future__ import print_function
import urllib 
import httplib
import base64
import string
import json
import boto3

'''
sample_game = {
    "id": "37705",
    "date": "2016-04-03",
    "time": "1:30PM",
    "awayTeam": {
        ID: "133",
        City: "St. Louis",
        Name: "Cardinals"
        Abbreviation: "STL"
    },
    "homeTeam": {
        "ID": "132",
        "City": "Pittsburgh",
        "Name": "Pirates",
        "Abbreviation": "PIT"
    },
    "location": "PNC Park"
}

sample_game = {
    "id": "37705",
    "date": "2016-04-03",
    "time": "1:30PM",
    "awayName" : "Blues",
    "awayCity" : "St. Louis",
    "homeName" : "Flyers",
    "homeCity" : "Philidelphia",
    "location": "PNC Park"
}
https://www.mysportsfeeds.com/api/feed/pull/nhl/2017-playoff/full_game_schedule.json
'''


# ----------------- Calls to Stats API -----------------


def get_game_schedule():

    host = "www.mysportsfeeds.com"
    url = "/api/feed/pull/nhl/2017-playoff/full_game_schedule.json"
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

    all_game_schedule = json.loads(webservice.getfile().read())
    game_schedule = []
    for game in all_game_schedule['fullgameschedule']['gameentry']:
        game_schedule.append(game)

    return game_schedule

# ----------------- Formatting Functions -----------------

def package_game_schedule_for_dynamodb(game_schedule):

    packaged_game_schedule = []
    for game in game_schedule:
        sample_game = {
            "gameID": "37705",
            "date": "2016-04-03",
            "time": "1:30PM",
            "awayName" : "Blues",
            "awayCity" : "St. Louis",
            "homeName" : "Flyers",
            "homeCity" : "Philidelphia",
            "location": "PNC Park"
        }
        if "id" in game:
            sample_game["gameID"] = game["id"]
        else:
            sample_game["gameID"] = "Not Available"
        if "date" in game:
            sample_game["date"] = game["date"]
        else:
            sample_game["date"] = "Not Available"
        if "time" in game:
            sample_game["time"] = game["time"]
        else:
            sample_game["time"] = "Not Available"
        if "Name" in game["awayTeam"]:
            sample_game["awayName"] = game["awayTeam"]["Name"]
        else:
            sample_game["awayName"] = "Not Available"
        if "City" in game["awayTeam"]:
            sample_game["awayCity"] = game["awayTeam"]["City"]
        else:
            sample_game["awayCity"] = "Not Available"
        if "Name" in game["homeTeam"]:
            sample_game["homeName"] = game["homeTeam"]["Name"]
        else:
            sample_game["homeName"] = "Not Available"
        if "City" in game["homeTeam"]:
            sample_game["homeCity"] = game["homeTeam"]["City"]
        else:
            sample_game["homeCity"] = "Not Available"
        if "location" in game:
            sample_game["location"] = game["location"]
        else:
            sample_game["location"] = "Not Available"
            
        packaged_game_schedule.append(sample_game)
        
    return packaged_game_schedule

def compile_attribute_updates(game_schedule):
    compiled_updates = []
    for game in game_schedule:
        compiled_attributes = {
            "Key" : { "gameID" : game["gameID"]},
            "awayName" : { "Action": "PUT", "Value": game["awayName"]},
            "awayCity" : { "Action": "PUT", "Value": game["awayCity"]},
            "homeName" : { "Action": "PUT", "Value": game["homeName"]},
            "homeCity" : { "Action": "PUT", "Value": game["homeCity"]},
            "time" : { "Action": "PUT", "Value": game["time"]},
            "date" : { "Action": "PUT", "Value": game["date"]},
            "location" : { "Action": "PUT", "Value": game["location"]},
        }
        compiled_updates.append(compiled_attributes)
    
    return compiled_updates

# ----------------- Writes to Database -----------------

def update_game_schedule_db(table_game_schedule, compiled_updates_game_schedule, counter):
    for update_item in compiled_updates_game_schedule:
        counter = counter +1
        response = table_game_schedule.update_item( Key = {'gameID' : update_item["Key"]["gameID"] }, AttributeUpdates = {
            "awayName": update_item["awayName"], "awayCity": update_item["awayCity"], "homeName": update_item["homeName"],
            "homeCity": update_item["homeCity"],"date": update_item["date"], "time": update_item["time"], "location": update_item["location"]})
    return counter


# ------------------ Helper Functions ------------------



# ------------------ Main handler ---------------------
def lambda_handler(event, context):
    response = ""
    counter = 0
    game_schedule = get_game_schedule()
    packaged_game_schedule = package_game_schedule_for_dynamodb(game_schedule)
    compiled_updates_game_schedule = compile_attribute_updates(packaged_game_schedule)
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    table_game_schedule = dynamodb.Table('GameSchedule')

    game_count = update_game_schedule_db(table_game_schedule, compiled_updates_game_schedule, counter)
    print(game_count)
    
    return 'Hello from Lambda'