"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib 
import httplib
import base64
import string
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import operator
import time


all_players_stats = {}



# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the N H L Stats skill. " \
                    "Please tell me how I can help you. "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me how I can help you."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))






# ----------------- Calls to Stats DB -----------------

def retrieve_player_stats(requested_player_number, name_in_use, name_type):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    table = dynamodb.Table('PlayerStats')
    
    if name_type == "city":
        name_in_use = name_in_use.title()
        name_in_use = name_in_use.replace("Saint", "St.")
        print(name_in_use)
        response = table.scan(FilterExpression=Attr('City').eq(name_in_use) & Attr('JerseyNumber').eq(requested_player_number))
    elif name_type == "team":
        name_in_use = name_in_use
        response = table.scan(FilterExpression=Attr('TeamName').eq(name_in_use) & Attr('JerseyNumber').eq(requested_player_number))
    player_stats = response["Items"]
    print(player_stats)

    return player_stats

def retrieve_todays_games(todays_date):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    table = dynamodb.Table('GameSchedule')
    print(todays_date)
    response = table.scan(FilterExpression=Attr('date').eq(todays_date))
    todays_games = response["Items"]
    print(todays_games)

    return todays_games

def retrieve_future_games(name_in_use, name_type):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    table = dynamodb.Table('GameSchedule')
    if name_type == "city":
        name_in_use = name_in_use.title()
        name_in_use = name_in_use.replace("Saint", "St.")
        response = table.scan(FilterExpression=Attr('awayCity').eq(name_in_use) | Attr('homeCity').eq(name_in_use))
    elif name_type == "team":
        name_in_use = name_in_use.title()
        response = table.scan(FilterExpression=Attr('awayName').eq(name_in_use) | Attr('homeName').eq(name_in_use))
    print(response)
    future_games = response["Items"]
    return future_games
    
# ----------------- Speech Output Functions -----------------

def write_intro_player_stats(speech_output, player_stats):
    FirstName = player_stats["PlayerInfo"]["FirstName"]
    LastName = player_stats["PlayerInfo"]["LastName"]

    speech_output = speech_output + "Here are the stats for " + FirstName + ' ' + LastName + " this season. "
    return speech_output
    

def write_basic_player_stats(speech_output, player_stats):
    Goals = player_stats["Stats"]["Goals"]
    Assists = player_stats["Stats"]["Assists"]
    Points = player_stats["Stats"]["Points"]
    GamesPlayed = player_stats["Stats"]["GamesPlayed"]
    PlusMinus = player_stats["Stats"]["PlusMinus"]
    PenaltyMinutes = player_stats["Stats"]["PenaltyMinutes"]
    FirstName = player_stats["PlayerInfo"]["FirstName"]
    LastName = player_stats["PlayerInfo"]["LastName"]
    
    speech_output = (speech_output + FirstName + ' ' + LastName + " has " + GamesPlayed + " games played. " +
    "He has " + Goals + " goals, and " + Assists + " assists, for a total of " + Points + " points. " +
    "His plus minus is " + PlusMinus + ", and has " + PenaltyMinutes + " penalty minutes. " +
    "Is there anything else I can help you with?")

    return speech_output

def write_todays_games(speech_output, todays_games):
    todays_games.sort(key=lambda x:time.mktime(time.strptime(x['time'], '%H:%M%p')))
    #todays_games.sort(key=operator.itemgetter("time"))
    speech_output = speech_output + "Here are todays games. . "
    for game in todays_games:
        speech_output = (speech_output + "At " + game["time"] + " Eastern Time, the " + game["awayCity"] + ' ' + game["awayName"] + " are playing the " +
            game["homeCity"] + ' ' + game["homeName"] + " at the " + game["location"] + " in " + game["homeCity"] + " . . ")
    speech_output = speech_output + "Is there anything else I can help you with?"

    return speech_output

def write_next_team_game(speech_output, next_game, where):
    full_time = db_time_to_date_object(next_game["date"], next_game["time"])

    if where == "away":
        speech_output = speech_output + " The next game for the " + next_game["awayCity"] + ' ' + next_game["awayName"] + ' '
        other_team = next_game["homeName"]
        other_city = next_game["homeCity"]
    if where == "home":
        speech_output = speech_output + " The next game for the " + next_game["homeCity"] + ' ' + next_game["homeName"] + ' '
        other_team = next_game["awayName"]
        other_city = next_game["awayCity"]

    speech_output = (speech_output + "is on " + full_time.strftime("%A, %B %d") + ',  at ' + next_game["time"] + ' versus the ' + other_city + ' ' + other_team + ' in ' + next_game["homeCity"] +
        ". . . Is there anything else I can help you with?")
    return speech_output



def player_not_found_speech_output(speech_output, requested_player_number, name_in_use):
    speech_output = ("I'm sorry, but I could not find stats for a player with the number " + str(requested_player_number) + " for the team " + name_in_use +
        ". Please try again.")
    return speech_output

def todays_games_not_found_speech_output(speech_output):
    speech_output = ("I could not find any NHL games that are scheduled for today" +
    ". Please try again later.")
    return speech_output

def next_game_not_found_speech_output(speech_output, requested_team, name_type):
    if name_type == "city":
        speech_output = ("I could not find the next game scheduled for " + requested_team + ". Please try again later."
            ". Please try again later.")
    if name_type=="team":
        speech_output = ("I could not find the next game scheduled for the " + requested_team + ". Please try again later.")
    return speech_output

# ----------------- Helper Functions -----------------

def format_date_for_db(requested_date):
    return "%s-%s-%s" % (requested_date.strftime('%Y'), requested_date.strftime('%m'), requested_date.strftime('%d'))

def db_time_to_date_object(requested_date, time):
    return datetime.datetime.strptime(requested_date + ' '+ time , "%Y-%m-%d %I:%M%p").date()

#def date_object_to_text(requested_date):

# ----------------- Intent Functions -----------------

def close_out(intent, session):
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    card_title = intent['name']
    
    speech_output = "Thank you for using the N H L stats skill. Goodbye"
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def get_simple_player_stats(intent, session):
    session_attributes = {}
    should_end_session = False
    card_title = intent['name']
    reprompt_text = None
    speech_output = ""
    found = 0
    requested_player_number = intent['slots']['Number']['value']
    player_stats = {}
    if "Detail" in intent['slots']:
        detail = intent['slots']['Detail']['value']
    else:
        detail = "basic"
    if "City" in intent['slots']:
        name_in_use = intent['slots']['City']['value']
        player_stats = retrieve_player_stats(requested_player_number, name_in_use, "city")
    elif "TeamName" in intent['slots']:
        name_in_use = intent['slots']['TeamName']['value']
        player_stats = retrieve_player_stats(requested_player_number, name_in_use, "team")

    if player_stats == []:
        found = 1
    else:
        player_stats = player_stats[0]
    if found == 0:
        speech_output = write_intro_player_stats(speech_output, player_stats)
        if detail == "basic":
            speech_output = write_basic_player_stats(speech_output, player_stats)
    elif found == 1:
        speech_output = player_not_found_speech_output(speech_output, requested_player_number, name_in_use)
    
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_todays_game_schedule(intent, session):
    session_attributes = {}
    should_end_session = False
    card_title = intent['name']
    reprompt_text = None
    speech_output = ""
    found = 0
    todays_date = format_date_for_db(datetime.datetime.now())
    todays_games = retrieve_todays_games(todays_date)
    if todays_games == []:
        speech_output = todays_games_not_found_speech_output(speech_output)
    else:
        speech_output = write_todays_games(speech_output, todays_games)

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def get_next_team_game(intent, session):
    session_attributes = {}
    should_end_session = False
    card_title = intent['name']
    reprompt_text = None
    speech_output = ""
    found = 0
    where = ""
    if "City" in intent['slots']:
        name_in_use = intent['slots']['City']['value'].title()
        name_type = "city"
    elif "TeamName" in intent['slots']:
        name_in_use = intent['slots']['TeamName']['value'].title()
        name_type = "team"

    future_games = retrieve_future_games(name_in_use, name_type)
    if future_games == []:
        speech_output = next_game_not_found_speech_output(speech_output, name_in_use, name_type)
    else:
        next_game = future_games[0]
        print(name_in_use)
        if (name_in_use == next_game["awayName"] or name_in_use == next_game["awayCity"]):
            where = "away"
            #print("away - " + name_in_use)
        else:
            where = "home"
            #print("home - " + name_in_use)
        speech_output = write_next_team_game(speech_output, next_game, where)

    return build_response({}, build_speechlet_response(
    card_title, speech_output, None, should_end_session))

# --------------------- Events -----------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want"""
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WhatsPlayerStats":
        return get_player_stats(intent, session)
    elif intent_name == "WhatsSimplePlayerCityStats":
        return get_simple_player_stats(intent, session)
    elif intent_name == "WhatsSimplePlayerTeamStats":
        return get_simple_player_stats(intent, session)
    elif intent_name == "WhatsTodaysGameSchedule":
        return get_todays_game_schedule(intent, session)
    elif intent_name == "WhensNextCityGame":
        return get_next_team_game(intent, session)
    elif intent_name == "WhensNextTeamGame":
        return get_next_team_game(intent, session)
    elif intent_name == "CloseOut":
        return close_out(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    print(event['request']['type'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
