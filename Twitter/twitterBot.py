import tweepy
import requests
import re
import json 
from datetime import date,datetime,timedelta
from random import randint
from time import sleep
import os.path
from os import path
import flag

#Authenticate to Twitter
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

def apiWorld():
    rCountry = requests.get('https://corona.lmao.ninja/v2/countries')
    jCountry = rCountry.json()
    return jCountry

def apiRequestsIndia():
    r = requests.get('https://api.covid19india.org/data.json')
    j = r.json()
    r = requests.get('https://api.covid19india.org/v2/state_district_wise.json')
    dist_data = r.json()

    return j,dist_data

def apiCountriesyday():
    yCountry = requests.get('https://disease.sh/v2/countries?yesterday=1')
    ydayC = yCountry.json()
    return ydayC

#Send Tweet with Trend chart
def sendTweet(message,media):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    msg = message
    media_send = api.media_upload(media)
    #print(msg)
    try:
        api.verify_credentials()
        print("Authentication OK")
        sleep(randint(10,50))
        api.update_status(msg,media_ids=[media_send.media_id])
    except:
        print("Error during authentication")

def sendTweetM(message):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    msg = message
    #print(msg)
    try:
        api.verify_credentials()
        print("Authentication OK")
        sleep(randint(10,50))
        api.update_status(msg)
    except:
        print("Error during authentication")

class color:
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

jsonContent = apiWorld()
jsonContent1 = apiRequestsIndia()

for each in jsonContent:
    confirmed = str(each["cases"])
    deaths = str(each["deaths"]) 
    recovered = str(each["recovered"])
    populationHere = str(each["population"])
    lastupdatedtime = str(datetime.fromtimestamp((each["updated"])/1000).strftime('%Y-%m-%d %H:%M'))
    countryName = str(each["country"]).replace(" ", "")
    new_case = str(each["todayCases"])
    new_deaths = str(each["todayDeaths"])
    active = str(each["active"])
    code = str(each["countryInfo"]["iso2"])
    testPositivityRate = str(round(((int(each["cases"]))/(int(each["tests"])))*100,2))+"%"
    new_recovered = str(each["todayRecovered"])
    jsonC = apiCountriesyday()
    for each in jsonC:
        if str(each["countryInfo"]["iso2"]) == code:
            confirmed_yday = str(each["cases"])
            new_case_yday = str(each["todayCases"])
            FlagIcon = flag.flag(code)
    message ="Stats for #"+countryName+" "+FlagIcon+"\
        \nActive Cases         : "+active+"\
        \nConfirmed Cases : "+confirmed+"(↑"+new_case+")\
        \nDeath Cases         : "+deaths+"(↑"+new_deaths+")\
        \nRecovered Cases : "+recovered+"(↑"+new_recovered+")\
        \nCases Yesterday  : "+confirmed_yday+"(↑"+new_case_yday+")\
        \nTest Positivity Rate    : "+testPositivityRate+"\
        \nUpdated at        : "+lastupdatedtime
    print(message)
    if code != "None":
        #sendTweetM(message)
        print(code)
        print("Awesome all others")
        media = "/home/ravindra/country/"+code+".png"
        #sendTweet(message,media)
    #elif str(path.isfile("/Users/ravindra/workspace/Covid19WorldStats/country/"+code+".png")):
     #   media = "/home/ravindra/country/"+code+".png"
     #   print("Awesome all others")
        #sendTweet(message,media)
    """ if str(path.isfile("/Users/ravindra/workspace/Covid19WorldStats/country/"+code+".png")):
        media = "/Users/ravindra/workspace/Covid19WorldStats/country/"+code+".png"
        sendTweet(message,media) """
    jsonContent = apiWorld()
    break
    
for each in jsonContent1[0]["statewise"]:
    if str(each["state"]) != "Total":
        confirmed = str(each["confirmed"]) 
        deaths = str(each["deaths"]) 
        recovered = str(each["recovered"])
        deltaconfirmed = str(each["deltaconfirmed"])
        deltarecovered = str(each["deltarecovered"])
        deltadeaths = str(each["deltadeaths"])
        lastupdatedtime = str(each["lastupdatedtime"])
        active = str(each["active"])
        state = str(each["state"]).replace(" ", "")
        message="Stats for Indian state #"+state+" :\
        \n\
        \nActive cases       : "+active+"\
        \nConfirmed cases    : "+confirmed+"(↑"+deltaconfirmed+")\
        \nDeath cases        : "+deaths+"(↑"+deltadeaths+")\
        \nRecovered cases    : "+recovered+"(↑"+deltarecovered+")\
        \nThis data was last updated at : "+lastupdatedtime
        print(message)
        sendTweetM(message)
        jsonContent1 = apiRequestsIndia()