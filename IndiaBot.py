from telegram.ext import (Updater, InlineQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters)
import telegram
import requests
import re
import json 
from datetime import date,datetime,timedelta
import logging
from functools import wraps
import numbers
import geocoder
import pyshorteners
from russia import region
from spain import regionES
from indianDistricts import districtIN
import pandas as pd
from franceRegion import regionFRA
from italy import regionIT
from usaStateCode import usaStateCode
from mexico import stateMX
from malaysiaState import state_malaysia
from pyshorteners import Shorteners
import random
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt 
import wget
import os
import xlrd
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import flag
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)
#today = date.today()
regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

def dateToday():
    today = date.today()
    return today

def apiRequestsIndia():
    r = requests.get('https://api.covid19india.org/data.json')
    j = r.json()
    r = requests.get('https://api.covid19india.org/v2/state_district_wise.json')
    dist_data = r.json()

    return j,dist_data

def apiZoneIndia():
    r= requests.get('https://api.covid19india.org/zones.json')
    zone = r.json()
    return zone

def apiTestedIndia():
    tr= requests.get('https://api.covid19india.org/state_test_data.json')
    test_data = tr.json()
    return test_data

def apiWorld():
    rCountry1 = requests.get('https://disease.sh/v2/countries')
    jCountry1 = rCountry1.json()
    return jCountry1

def apiCountriesyday():
    yCountry = requests.get('https://disease.sh/v2/countries?yesterday=1')
    ydayC = yCountry.json()
    return ydayC

def apiRequestUSA():
    rUS = requests.get('https://covidtracking.com/api/states/info')
    jstates = rUS.json()

    rUS_states = requests.get('https://covidtracking.com/api/states')
    states_us = rUS_states.json()

    us_county = requests.get('https://disease.sh/v2/jhucsse/counties')
    county_us = us_county.json()

    return jstates,states_us,county_us

def apiUSAStates(stateName):
    usaState = requests.get("https://disease.sh/v2/states/"+stateName)
    states_us_new = usaState.json()
    return states_us_new

def apiUSAStatesYday(stateName):
    usaState_y = requests.get("https://disease.sh/v2/states/"+stateName+"?yesterday=true")
    states_us_new_yday = usaState_y.json()
    return states_us_new_yday

def apiRequestGermany():
    germany = requests.get("https://rki-covid-api.now.sh/api/states")
    statejson = germany.json()
    return statejson

def apiWorldNew():
    world = requests.get("https://disease.sh/v2/all").json()
    return world

def apiRequestJapan():
    japan = requests.get("https://data.covid19japan.com/summary/latest.json")
    japanProvince = japan.json()
    return japanProvince

def apiRequestUK():
    uk = requests.get("https://c19downloads.azureedge.net/downloads/json/coronavirus-cases_latest.json")
    uk_ltla = uk.json()
    return uk_ltla

def apiRequestNL():
    nl = requests.get("https://opendata.arcgis.com/datasets/620c2ab925f64ed5979d251ba7753b7f_0.geojson")
    nl_city = nl.json()
    return nl_city

def apiRequestRU(code):
    ru = requests.get("https://xn--80aesfpebagmfblc0a.xn--p1ai/covid_data.json?do=region_stats&code="+code)
    ru_state = ru.json()
    return ru_state

def apiRequestAUS():
    aus = requests.get("https://interactive.guim.co.uk/docsdata/1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE.json")
    aus_state = aus.json()
    return aus_state

def apiRequestCAN():
    can = requests.get("https://opendata.arcgis.com/datasets/3afa9ce11b8842cb889714611e6f3076_0.geojson")
    can_province = can.json()
    return can_province

def apiRequestBrazil():
    bra = requests.get("https://covid19-brazil-api.now.sh/api/report/v1")
    bra_states = bra.json()
    return bra_states

def apiRequestES(dateToday):
    spain = requests.get("https://api.covid19tracking.narrativa.com/api/"+dateToday+"/country/spain/region/all")
    es_province = spain.json()
    return es_province

def apiRequestFR(code):
    fr = requests.get("https://coronavirusapi-france.now.sh/LiveDataByDepartement?Departement="+code)
    fr_state = fr.json()
    return fr_state

def apiRequestItaly():
    ita = requests.get("https://disease.sh/v2/gov/Italy")
    ita_states = ita.json()
    return ita_states

def apiRequestMexStates():
    mex = requests.get("https://api.apify.com/v2/key-value-stores/vpfkeiYLXPIDIea2T/records/LATEST?disableRedirect=true")
    mex_states = mex.json()
    return mex_states

def apiTravelAlert():
    travel = requests.get("http://api.coronatracker.com/v1/travel-alert")
    travel_country = travel.json()
    return travel_country

APIKey_LQ = ""
API_key_M = ""
NewsAPIKey = ""

WORLD_MAP="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/COVID-19_Outbreak_World_Map_per_Capita.svg/1200px-COVID-19_Outbreak_World_Map_per_Capita.svg.png"

def _add_timestamp(url):
    timestamp = datetime.utcnow().strftime("%Y%m%d%H")
    return "{}?t={}".format(url, timestamp)

def cases_world_map():
    return _add_timestamp(WORLD_MAP)

def get_count_world():
    jsonContent = apiWorldNew()
    TotalConfirmed = str(jsonContent["cases"])
    NewConfirmed = str(jsonContent["todayCases"])
    NewDeaths = str(jsonContent["todayDeaths"])
    TotalDeaths = str(jsonContent["deaths"])
    TotalRecovered = str(jsonContent["recovered"])
    active = str(jsonContent["active"])
    casesPerOneMillion = str(jsonContent["casesPerOneMillion"])
    deathsPerOneMillion = str(jsonContent["deathsPerOneMillion"])
    tests = str(jsonContent["tests"])
    testsPerOneMillion = str(jsonContent["testsPerOneMillion"])
    activePerOneMillion = str(jsonContent["activePerOneMillion"])
    recoveredPerOneMillion = str(jsonContent["recoveredPerOneMillion"])
    affectedCountries = str(jsonContent["affectedCountries"])
    return TotalConfirmed,NewConfirmed,NewDeaths,TotalDeaths,TotalRecovered,affectedCountries,active,casesPerOneMillion,deathsPerOneMillion,tests,testsPerOneMillion,activePerOneMillion,recoveredPerOneMillion

def world(update, context):
    content = get_count_world()
    print (content)
    if content[0] == "0":
        context.bot.send_message(chat_id=update.message.chat_id, text="The API is giving incorrect data")
    else:
        updatedTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        chat_id = update.message.chat_id
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=chat_id, text="Below are the stats for World, \
        \n\
        \nActive cases          : *"+content[6]+"*\
        \nConfirmed cases   : *"+content[0]+"* *(↑"+content[1]+")*\
        \nDeath cases           : *"+content[3]+"* *(↑"+content[2]+")*\
        \nRecovered cases   : *"+content[4]+"*\
        \nAffected countries : *"+content[5]+"*\
        \nCases per million   : *"+content[7]+"*\
        \nDeaths per million  : *"+content[8]+"*\
        \nTotal Tests              : *"+content[9]+"*\
        \nTests per million     : *"+content[10]+"*\
        \nActive per million    : *"+content[11]+"*\
        \nRecovered per million : *"+content[12]+"*\
        \nThis data was last updated at *"+str(updatedTime)+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=cases_world_map(),parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked world :"+update.message.from_user.first_name)
    logger.info("World handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def zones(update, context, districtIndia):
    jsonContent = apiZoneIndia()
    for each in jsonContent["zones"]:
        if str(each["district"]) == districtIndia:
            zone = str(each["zone"])
            if zone == "Green":
                zone = "GREEN ✅"
            if zone == "Red":
                zone = "RED 🔴"
            if zone == "Orange":
                zone = "ORANGE 🔶"
    return zone

def testRate(stateName):
    jsonContent = apiTestedIndia()
    today = datetime.today()
    tday = today.strftime('%d.%m.%Y')
    yesterday = today - timedelta(days = 1)
    yday = yesterday.strftime('%d/%m/%Y')
    for each in jsonContent["states_tested_data"]:
        if str(each["state"]) == stateName:
            print(stateName)
            print(str(each["updatedon"]))
            print(str(yday))
            if str(each["updatedon"])==str(yday):
                testpositivityrate = str(each["testpositivityrate"])
                totaltested = int(each["totaltested"])
                if testpositivityrate == "":
                    totaltested = int(each["totaltested"])
                    print(totaltested)
                    positive = int(each["positive"])
                    testpositivityrate = str(round((positive/totaltested)*100,2))+"%"
                lastUpdated = str(each["updatedon"])
    return testpositivityrate,str(totaltested),lastUpdated

def testRateIndia(cases):
    print(cases)
    jsonContent = apiRequestsIndia()
    today = datetime.today()
    tday = today.strftime('%d/%m/%Y')
    yesterday = today - timedelta(days = 1)
    yday = yesterday.strftime('%d/%m/%Y')
    for each in jsonContent[0]["tested"]:
        d = str(each["updatetimestamp"]).split(" ")
        print(d[0])
        print(str(tday))
        print(str(yday))
        if(d[0]==str(tday)):
            print(d[0])
            testpositivityrate = str(each["testpositivityrate"])
            totalsamplestested = int(each["totalsamplestested"])
            if testpositivityrate == "":
                totalsamplestested = int(each["totalsamplestested"])
                positive = int(cases)
                testpositivityrate = str(round((positive/totalsamplestested)*100,2))+"%"
        elif(d[0]==str(yday)):
            print(d[0])
            testpositivityrate = str(each["testpositivityrate"])
            totalsamplestested = int(each["totalsamplestested"])
            if testpositivityrate == "":
                totalsamplestested = int(each["totalsamplestested"])
                positive = int(cases)
                testpositivityrate = str(round((positive/totalsamplestested)*100,2))+"%"
    return testpositivityrate,str(totalsamplestested)

def new_count_India():
    jsonContent = apiRequestsIndia()
    for each in jsonContent[0]["statewise"]:
        if str(each["state"]) == "Total":
           confirmed = str(each["confirmed"]) 
           deaths = str(each["deaths"]) 
           recovered = str(each["recovered"])
           deltaconfirmed = str(each["deltaconfirmed"])
           deltarecovered = str(each["deltarecovered"])
           deltadeaths = str(each["deltadeaths"])
           lastupdatedtime = str(each["lastupdatedtime"])
           active = str(each["active"])
    for each in jsonContent[0]["cases_time_series"]:
        today = datetime.today()
        yesterday = today - timedelta(days = 1)
        yday = yesterday.strftime('%d %B')
        print(yday)
        if str(each["date"]).strip() == str(yday):
            totalconfirmedyday = str(each["totalconfirmed"])
            dailyconfirmedyday = str(each["dailyconfirmed"])
            totaldeathyday = str(each["totaldeceased"])
    return confirmed,deaths,recovered,deltaconfirmed,lastupdatedtime,deltarecovered,deltadeaths,active,totalconfirmedyday,dailyconfirmedyday,totaldeathyday

def india(update, context):
    content = new_count_India()
    tr = testRateIndia(content[0])
    FlagIcon = flag.flag("IN")
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="Below are the stats for *India* "+FlagIcon+":\
    \n\
    \nActive cases           : *"+content[7]+"*\
    \nConfirmed cases    : *"+content[0]+"* *(↑"+content[3]+")*\
    \nDeath cases            : *"+content[1]+"* *(↑"+content[6]+")*\
    \nRecovered cases    : *"+content[2]+"* *(↑"+content[5]+")*\
    \nCases Yesterday    : *"+content[8]+"* *(↑"+content[9]+")*\
    \nTest Positivity Rate : *"+tr[0]+"*\
    \nTotal samples tested : *"+tr[1]+"*\
    \nThis data was last updated at : *"+content[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked India: "+update.message.from_user.first_name)
    logger.info("India handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)
    return content[8],content[10]

def state_new_count_India(var):
    jsonContent = apiRequestsIndia()
    for each in jsonContent[0]["statewise"]:
        if str(each["statecode"]) == var:
           confirmed = str(each["confirmed"]) 
           deaths = str(each["deaths"]) 
           recovered = str(each["recovered"])
           deltaconfirmed = str(each["deltaconfirmed"])
           lastupdatedtime = str(each["lastupdatedtime"])
           stateName = str(each["state"])
           active = str(each["active"])
           deltarecovered = str(each["deltarecovered"])
           deltadeaths = str(each["deltadeaths"])
    
    return confirmed,deaths,recovered,deltaconfirmed,lastupdatedtime,stateName,deltarecovered,deltadeaths,active

def indianstate(update, context):
    state_code = ' '.join(context.args).upper()
    print(state_code)
    if (state_code.isdigit()):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a statecode, Ex: '/state KA'",parse_mode=telegram.ParseMode.MARKDOWN)
    elif state_code == "":
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a statecode, Ex: '/state KA'",parse_mode=telegram.ParseMode.MARKDOWN)
    elif(regex.search(state_code)) == None:
        content_k = state_new_count_India(state_code)
        testR = testRate(content_k[5])
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Below are the stats for *"+content_k[5]+"* \
        \n\
        \nActive cases           : *"+content_k[8]+"*\
        \nConfirmed cases    : *"+content_k[0]+"* *(↑"+content_k[3]+")*\
        \nDeath cases            : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered cases    : *"+content_k[2]+"* *(↑"+content_k[6]+")*\
        \nTest Positivity Rate : *"+testR[0]+"*\
        \nTotal samples tested : *"+testR[1]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a statecode correctly , Ex: '/state KA",parse_mode=telegram.ParseMode.MARKDOWN)   
    logger.info("State handler used ", update.message.chat.id, update.message.from_user.first_name)
    print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)

def indian_state_code(update, context):
    jsonContent = apiRequestsIndia()
    state = []
    code = []
    for each in jsonContent[0]['statewise']:    
        state.append(each["state"])
        code.append(each["statecode"])
    
    StateName_StateCode = ' \n'.join(["For "+ str(a) +" use code "+ b for a,b in zip(state,code)])
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="*"+StateName_StateCode+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    logger.info("State code handler used ", update.message.chat.id, update.message.from_user.first_name)   

def country_code(update, context):
    var = ' '.join(context.args)
    print(var)
    if var == "":
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a Letter to list the countries , Ex: '/countrycode N'",parse_mode=telegram.ParseMode.MARKDOWN)
    elif (var.isdigit()):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a Letter to list the countries , Ex: '/countrycode N'",parse_mode=telegram.ParseMode.MARKDOWN)
    elif(regex.search(var)) == None:
        letter = var.capitalize()
        print(letter)
        jsonContent = apiWorld()
        country = []
        country_code = []
        for each in jsonContent:
            countryName = str(each["country"])
            if countryName.startswith(letter):
                country.append(each["country"])
                country_code.append(each["countryInfo"]["iso2"])

        countryName_countryCode = ' \n'.join([str(a) +" use code : "+ b for a,b in zip(country,country_code)])
        chat_id = update.message.chat_id
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=chat_id, text="List of Countries starting with letter *"+letter+"* :\n*"+countryName_countryCode+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a Letter to list the countries , Ex: '/countrycode N",parse_mode=telegram.ParseMode.MARKDOWN)
    logger.info("Country code handler used ", update.message.chat.id, update.message.from_user.first_name)

def countryWiseStatsCollect(var):
    print(str(var).upper())
    jsonContent = apiWorld()
    jsonC = apiCountriesyday()
    for each in jsonContent:
        if str(each["countryInfo"]["iso2"]) == str(var).upper():
            confirmed = str(each["cases"])
            deaths = str(each["deaths"]) 
            recovered = str(each["recovered"])
            populationHere = str(each["population"]).strip()
            lastupdatedtime = str(datetime.fromtimestamp((each["updated"])/1000).replace(microsecond=0))
            countryName = str(each["country"])
            new_case = str(each["todayCases"])
            new_deaths = str(each["todayDeaths"])
            casesPerOneMillion = str(each["casesPerOneMillion"])
            deathsPerOneMillion = str(each["deathsPerOneMillion"])
            activePerOneMillion = str(each["activePerOneMillion"])
            recoveredPerOneMillion = str(each["recoveredPerOneMillion"])
            testsPerOneMillion = str(each["testsPerOneMillion"])
            active = str((each["cases"])-(each["deaths"])-(each["recovered"]))
            testPositivityRate = str(round(((int(each["cases"]))/(int(each["tests"])))*100,2))+"%"
    for each in jsonC:
        if str(each["countryInfo"]["iso2"]) == str(var).upper():
            confirmed_yday = str(each["cases"])
            new_case_yday = str(each["todayCases"])
            deaths_yday = str(each["deaths"])
    return confirmed,deaths,recovered,populationHere,lastupdatedtime,countryName,new_case,new_deaths,casesPerOneMillion,deathsPerOneMillion,activePerOneMillion,recoveredPerOneMillion,testsPerOneMillion,confirmed_yday,new_case_yday,deaths_yday,active,testPositivityRate

def countryWiseData(update, context):
    country_code = ' '.join(context.args)
    letter = country_code.capitalize()
    print(country_code)
    if (country_code.isdigit()):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a country code, Ex:'/country NL'",parse_mode=telegram.ParseMode.MARKDOWN)
    elif country_code == "":
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a country code, Ex:'/country NL'",parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        content_k = countryWiseStatsCollect(letter)
        FlagIcon = flag.flag(letter)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The stats for country *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases           : *"+content_k[16]+"*\
        \nConfirmed Cases    : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases            : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases    : *"+content_k[2]+"*\
        \nCases Yesterday     : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nCases per million    : *"+content_k[8]+"*\
        \nDeath per million    : *"+content_k[9]+"*\
        \nActive per million    : *"+content_k[10]+"*\
        \nRecovered per million : *"+content_k[11]+"*\
        \nTests per million    : *"+content_k[12]+"*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        #context.bot.send_photo(chat_id=update.message.chat_id, photo=photo_file,parse_mode=telegram.ParseMode.MARKDOWN)
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
        logger.info("Country handler used ", update.message.chat.id, update.message.from_user.first_name)
        captureID(update)

def topC(update, context):
    var = ' '.join(context.args)
    #res = isinstance(var, str)
    country = []
    country_code = []
    deaths = []
    confirmed =[]
    countryN = []
    confirmedcountry = []
    confirmedN = []
    if var == "":
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a number after the handler to get the results, Ex: '/topC 10",parse_mode=telegram.ParseMode.MARKDOWN)
    elif ((var>='a' and var<= 'z') or (var>='A' and var<='Z')):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a number after the handler to get results, Ex: '/topC 10",parse_mode=telegram.ParseMode.MARKDOWN)
    elif ((var >= '50')):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a number below 50 with the handler to get results, Ex: '/topD 10",parse_mode=telegram.ParseMode.MARKDOWN)
    elif(regex.search(var)) == None:
        jsonContent = apiWorld()
        for each in jsonContent:
            confirmed.append(each["cases"])
            country.append(str(each["country"]))
            country_code.append(str(each["countryInfo"]["iso2"]))
            deaths.append(str(each["deaths"]))
        #print(confirmed)
        confirmed.sort(reverse = True)
        top = confirmed[0:int(var)]
        #print("This is sorted:",confirmed)
        #print(top)
        j=0
        for i in top:
            for each in jsonContent:
                confirmedN = each["cases"]
                if (i == confirmedN):
                    confirmedcountry.append(str(each["cases"]))
                    countryN.append("No:"+str(j+1)+">> "+str(each["country"]))
                    j += 1
                    
        countryName_confirmed = ' \n'.join(["*"+str(a)+"*"+" has *"+ b +"* confirmed cases" for a,b in zip(countryN,confirmedcountry)])
    else:
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a number below 50 with the handler to get results, Ex: '/topD 10",parse_mode=telegram.ParseMode.MARKDOWN)  
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="The *Top "+var+"* countries with max confirmed cases of Covid-19 are : \
    \n\
    \n"+countryName_confirmed+"",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked TopC: "+update.message.from_user.first_name)
    logger.info("TopC handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def topD(update, context):
    var = ' '.join(context.args)
    #res = isinstance(var, str)
    country = []
    deaths = []
    countryN = []
    deathCountry = []
    jsonContent = apiWorld()
    if var == "":
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a number after the handler to get the results, Ex: '/topD 10",parse_mode=telegram.ParseMode.MARKDOWN)
    elif ((var>='a' and var<= 'z') or (var>='A' and var<='Z')):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a number after the handler to get results, Ex: '/topD 10",parse_mode=telegram.ParseMode.MARKDOWN)
    elif ((var >= '50')):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a number below 50 with the handler to get results, Ex: '/topD 10",parse_mode=telegram.ParseMode.MARKDOWN)
    elif(regex.search(var)) == None:
        for each in jsonContent:
            country.append(str(each["country"]))
            deaths.append(each["deaths"])
        #print(confirmed)
        deaths.sort(reverse = True)
        top = deaths[0:int(var)]
        #print("This is sorted:",confirmed)
        #print(top)
        j=0
        for i in top:
            for each in jsonContent:
                deathN = each["deaths"]
                if (i == deathN):
                    deathCountry.append(str(each["deaths"]))
                    countryN.append("No:"+str(j+1)+">> "+str(each["country"]))
                    j += 1

        countryName_death = ' \n'.join(["*"+str(a)+"*"+" has *"+ b +"* deaths from Covid-19" for a,b in zip(countryN,deathCountry)])
    else:
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a number below 50 with the handler to get results, Ex: '/topD 10",parse_mode=telegram.ParseMode.MARKDOWN)
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="The *Top "+var+"* countries with max death cases from Covid-19 are : \
    \n\
    \n"+countryName_death+"",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked TopD: "+update.message.from_user.first_name)
    logger.info("TopD handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def commands(update,context):
    logger.info("help handler used ", update.message.chat.id, update.message.from_user.first_name)
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text= "\
    \n<b><u>Commands:</u></b> \n \
    \n<b>/india</b> - Fetch stats of India \n\
    \n<b>/statecode</b> - Fetch statewise code \n\
    \n<b>/state</b> statecode - Fetch stats per state,\
    \nNow for karnataka use <b>'/state KA'</b> without the single quotes\n \
    \n<b>/districtwise</b> - Fetch stats district wise of a particular state using the state code \n\
    \n<b>/world</b> - Fetch stats for the entire world \n\
    \n<b>/countrycode</b> - Fetch country codes ,\
    \nTo show all country names with starting letter I and thier resp. code use <b>'/countrycode I'</b> without the single quotes\n \
    \n<b>/country</b> countrycode - Fetch country wise stats,\
    \nNow for showing stats of Netherlands use <b>'/country NL'</b> without the single quotes\n\
    \n<b>/topC</b> number - Fetch top countries with highest confirmed covid-19 cases,\
    \nNow to show Top 10 countries use <b>'/topC 10'</b> \n\
    \n<b>/topD</b> number - Fetch top countries with highest death due to covid-19,\
    \nNow to show Top 10 countries use <b>'/topD 10'</b> without the single quotes\
    \n\
    \n<b>/ListUSAStates</b> \
    \nTo show all state names with starting letter N and thier respective code use <b>'/ListUSAStates N'</b> \n \
    \n<b>/USAState</b> statecode - Fetch stats per state,\
    \nNow for NewYork use <b>'/USAState NY'</b> without the single quotes \n \
    \n<b>/asia</b> - Fetch stats of Asia \
    \n<b>/africa</b> - Fetch stats of Africa \
    \n<b>/europe</b> - Fetch stats of Europe \
    \n<b>/australia</b> - Fetch stats of Australia \
    \n<b>/northamerica</b> - Fetch stats of North America \
    \n<b>/southamerica</b> - Fetch stats of South America \
    \n<b>/official_TC</b> to see official Telegram channels of other countries \
    \n<b>/news</b> - Fetch random top news from worldwide related to Covid-19 \
    \n<b>/travelAdvice</b> - Fetch travel alerts set by each countries due to Covid-19, \
    \nNow for Netherlands use <b>'/travelAdvice NL'</b> without the single quotes \
    ",parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
    print(update.message.from_user.username)
    captureID(update)

def help(update,context):
    logger.info("help handler used ", update.message.chat.id, update.message.from_user.first_name)
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text= "\
    \n \
    \nYou can now <b>Share any location</b> and get the stats of any country,\
    \nBelow are few countries where you get more detailed stats \
    \n\
    \nIf you share any location which inside \
    \n\
    \n<b>1)India</b> get statewise and district-wise stats,\
    \n<b>2)USA</b> get statewise and county wise stats,\
    \n<b>3)Germany</b> get statewise stats,\
    \n<b>4)Netherlands</b> get statewise and Gementee wise stats,\
    \n<b>5)Japan</b> get statewise stats,\
    \n<b>6)Russia</b> get statewise stats,\
    \n<b>7)UK</b> get statewise stats,\
    \n<b>8)Spain</b> get statewise stats,\
    \n<b>9)Australia</b> get statewise stats,\
    \n<b>10)Canada</b> get statewise stats,\
    \n<b>11)Brazil</b> get statewise stats,\
    \n<b>12)France</b> get Département stats,\
    \n<b>13)Italy</b> get statewise stats,\
    \n<b>14)Mexico</b> get statewise stats,\
    \n<b>15)Malaysia</b> get statewise stats,\
    \nAll other countries get just country wise stats,\n\
    \n<b>Just point the pin on the map and share it</b> \n \
    \n /commands for listing all the available commands",parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
    print(update.message.from_user.username)
    captureID(update)

def start(update,context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat.id, text="<b>Welcome to The Covid-19 Tracker Bot! 🦠</b> \
    \n \
    \n<b><u>You can use these Commands:</u></b> \n \
    \n<b>/help</b> \
    \n<b>/commands</b> \
    \n<b>/official_TC</b> \
    \n \
    \nStay Home, Stay Safe! 🏡 <b>"+ update.message.from_user.first_name+"</b>\
    \n\
    \nAbout: Bot created by https://twitter.com/ravindraten",parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
    print(update.message.from_user.username)
    print(update.message.from_user.first_name)
    print(update.message.chat.id)
    captureID(update)
    logger.info("Start handler used ", update.message.chat.id, update.message.from_user.first_name)

def captureID(update):
    f= open("userID.txt","w+")
    f= open("guru99.txt", "a+")
    f.write("\nUser is %d\r" % (update.message.chat.id)+": "+(update.message.from_user.first_name)+": "+str(dateToday()))

def officialTelegramChannels(update,context):
    logger.info("officialTelegramChannels handler used ", update.message.chat.id, update.message.from_user.first_name)
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text= """\
    If you're looking for official news about the Novel Coronavirus and COVID-19, here are some examples of verified Telegram channels from health ministries around the world.\

    🇨🇺 <a href="https://t.me/MINSAPCuba">Cuba</a>
    🇬🇪 <a href="https://t.me/StopCoVge">Georgia</a>
    🇩🇪 <a href="https://t.me/Corona_Infokanal_BMG">Germany</a>
    🇭🇰 <a href="http://t.me/HKFIGHTCOVID19">Hong Kong</a>
    🇮🇳 <a href="https://t.me/MyGovCoronaNewsdesk">India</a>
    🇮🇹 <a href="https://t.me/MinisteroSalute">Italy</a>
    🇮🇱 <a href="https://t.me/MOHreport">Israel</a>
    🇰🇿 <a href="https://t.me/coronavirus2020_kz">Kazakhstan</a>
    🇰🇬 <a href="https://t.me/RshKRCOV">Kyrgyzstan</a>
    🇲🇾 <a href="https://t.me/cprckkm">Malaysia</a>
    🇳🇬 <a href="http://t.me/ncdcgov">Nigeria</a>
    🇷🇺 <a href="https://t.me/stopcoronavirusrussia">Russia</a>
    🇸🇦 <a href="https://t.me/LiveWellMOH">Saudi Arabia</a>
    🇸🇬 <a href="https://t.me/govsg">Singapore</a>
    🇪🇸 <a href="https://t.me/sanidadgob">Spain</a>
    🇹🇬 <a href="http://t.me/GouvTG">Togo</a>
    🇺🇦 <a href="https://t.me/COVID19_Ukraine">Ukraine</a>
    🇺🇿 <a href="https://t.me/koronavirusinfouz">Uzbekistan</a>
    """,parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
    print(update.message.from_user.username)
    logger.info("officialTelegramChannels handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocation(update,context):
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    current_lat = str(message.location.latitude)
    current_lon = str(message.location.longitude)
    print(current_lat)
    print(current_lon)
    jsonContent = apiRequestsIndia()
    contents = requests.get("https://locationiq.com/v1/reverse.php?key="+APIKey_LQ+"&lat="+current_lat+"&lon="+current_lon+"&format=json").json()
    countryName = contents["address"]["country"]
    country = contents["address"]["country_code"]
    FlagIcon = flag.flag(country)
    #print(contents)
    if country == "in":
        contentIN = india(update,context)
        countryTrend(update,context,country,contentIN[0],contentIN[1],countryName)
        try:
            state = contents["address"]["state"]
            testR = testRate(state)
        except:
            state_district = contents["address"]["state_district"]
            if state_district == "North Goa":
                state = "Goa"
            if state_district == "South Goa":
                state = "Goa"

        for each in jsonContent[0]["statewise"]:
            if str(each["state"]) == state:
                confirmed = str(each["confirmed"]) 
                deaths = str(each["deaths"]) 
                recovered = str(each["recovered"])
                deltaconfirmed = str(each["deltaconfirmed"])
                deltarecovered = str(each["deltarecovered"])
                deltadeaths = str(each["deltadeaths"])
                lastupdatedtime = str(each["lastupdatedtime"])
                active = str(each["active"])
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+state+"* \
        \n\
        \nActive cases       : *"+active+"*\
        \nConfirmed cases : *"+confirmed+"* *(↑"+deltaconfirmed+")*\
        \nDeath cases         : *"+deaths+"* *(↑"+deltadeaths+")*\
        \nRecovered cases : *"+recovered+"* *(↑"+deltarecovered+")*\
        \nTest Positivity Rate : *"+testR[0]+"*\
        \nTest samples tested : *"+testR[1]+"*\
        \nThis data was last updated at : *"+lastupdatedtime+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        getLocation1(update,context,current_lat,current_lon,lastupdatedtime)
        
        #links(context,update,current_lat,current_lon)
    elif country == "us":
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are currently located in or the Map location shared is in *"+content_k[5]+"* "+FlagIcon+" \
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases         : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases  : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        state = contents["address"]["state"]
        print(state)
        jsonContentUS = apiUSAStates(state)
        jsonContentUS_yday = apiUSAStatesYday(state)
        #for each in jsonContentUS:
        active = str(jsonContentUS["active"])
        cases = str(jsonContentUS["cases"])
        todayCases = str(jsonContentUS["todayCases"])
        deaths = str(jsonContentUS["deaths"])
        todayDeaths = str(jsonContentUS["todayDeaths"])
        recovered = ((int(cases)) - (int(active)))
        CasesYday = str(jsonContentUS_yday["cases"])
        NewCasesYday = str(jsonContentUS_yday["todayCases"])
        updated = str(datetime.fromtimestamp((jsonContentUS["updated"])/1000).replace(microsecond=0))
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+state+"*\
        \n\
        \nConfirmed Cases   : *"+cases+"**(↑"+todayCases+")*\
        \nDeath Cases         : *"+deaths+"**(↑"+todayDeaths+")*\
        \nActive Cases        : *"+active+"*\
        \nRecovered Cases   : *"+str(recovered)+"*\
        \nCases yesterday  : *"+CasesYday+"**(↑"+NewCasesYday+")*\
        \nThis data was last updated at : *"+updated+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        getLocation2(update,context,current_lat,current_lon)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "de":
        #state = contents["address"]["state"]
        #print(state)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        getLocation3(update,context,current_lat,current_lon)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "jp":
        state_jp = contents["address"]["state"]
        prefecture = str((state_jp.replace("Prefecture","")).strip())
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases          : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        getLocationJP(update,context,prefecture)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "gb":
        regionUK = contents["address"]["state_district"]
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        getLocationUK(update,context,regionUK)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "nl":
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        #links(context,update,current_lat,current_lon)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        
        try:
            cityNL = contents["address"]["city"]
        except:
            cityNL = contents["address"]["town"]
        getLocationNL(update,context,cityNL)
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
        captureID(update)
    elif country == "ru":
        stateRU = contents["address"]["state"]
        print(stateRU)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        print(stateRU)
        getLocationRU(update,context,stateRU)
        print("This User checked this"+ content_k[5] +":"+update.message.from_user.first_name)
        captureID(update)
    elif country == "au":
        stateAUS = str((contents["address"]["state"]).strip())
        print(stateAUS)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        getLocationAUS(update,context,stateAUS)
        print("This User checked this"+ content_k[5] +":"+update.message.from_user.first_name)
        captureID(update)
    elif country == "ca":
        provinceCA = str(contents["address"]["state"]).upper()
        print(provinceCA)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        #links(context,update,current_lat,current_lon)
        getLocationCA(update,context,provinceCA)
        print("This User checked Now"+ content_k[5] +":"+update.message.from_user.first_name)
        captureID(update)
    elif country == "es":
        provinceCA = str(contents["address"]["state"])
        print(provinceCA)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nTests per million    : *"+content_k[12]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        #links(context,update,current_lat,current_lon)
        getLocationES(update,context,provinceCA)
        print("This User checked Now"+ content_k[5] +":"+update.message.from_user.first_name)
        captureID(update)
    elif country == "br":
        state_br = contents["address"]["state"]
        print(state_br)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases          : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        getLocationBR(update,context,state_br)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "fr":#country = url['country_code']
        county = contents["address"]["county"]
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        #links(context,update,current_lat,current_lon)
        print(county)
        getLocationFR(update,context,county)
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
    elif country == "it" :#country = url['country_code']
        contentsBDC = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client?latitude="+current_lat+"&longitude="+current_lon+"&localityLanguage=en").json()
        stateIT = contentsBDC["principalSubdivision"]
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        #links(context,update,current_lat,current_lon)
        getLocationIT(update,context,stateIT)
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
    elif country == "cl" :#country = url['country_code']
        content_k = countryWiseStatsCollect(country)
        today = datetime.today()
        tday = today.strftime('%d.%m.%Y')
        yesterday = today - timedelta(days = 1)
        yday = yesterday.strftime('%d.%m.%Y')
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*\
        \nBelow is the pdf from Minsal from yesterday",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        try:
            context.bot.send_document(chat_id=update.effective_chat.id,document="https://cdn.digital.gob.cl/public_files/Campa%C3%B1as/Corona-Virus/Reportes/"+tday+"_Reporte_Covid19.pdf")
        except:
            context.bot.send_document(chat_id=update.effective_chat.id,document="https://cdn.digital.gob.cl/public_files/Campa%C3%B1as/Corona-Virus/Reportes/"+yday+"_Reporte_Covid19.pdf")
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
    elif country == "mx" :#country = url['country_code']
        content_k = countryWiseStatsCollect(country)
        state_mx = contents["address"]["state"]
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases    : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases            : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases    : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        getLocationMX(update,context,state_mx)
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
    elif country == "my" :#country = url['country_code']
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases    : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases            : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases    : *"+content_k[2]+"*\
        \nCases Yesterday : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        contentsBDC = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client?latitude="+current_lat+"&longitude="+current_lon+"&localityLanguage=en").json()
        stateMY = contentsBDC["principalSubdivision"]
        getLocationMY(update,context,stateMY)
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
    else :#country = url['country_code']
        print(contents)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* "+FlagIcon+"\
        \n\
        \nActive Cases        : *"+content_k[16]+"*\
        \nConfirmed Cases   : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases           : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCases Yesterday    : *"+content_k[13]+"* *(↑"+content_k[14]+")*\
        \nTest Positivity Rate    : *"+content_k[17]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        countryTrend(update,context,country,content_k[13],content_k[15],countryName)
        #links(context,update,current_lat,current_lon)
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
    logger.info("Location handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)
    #context.bot.send_message(chat_id=update.message.chat_id, text="Would you mind sharing your location and contact with me?",reply_markup=reply_markup)

def links(context,update,current_lat,current_lon):
    s = pyshorteners.Shortener(Shorteners.TINYURL)
    response = s.short("https://www.google.com/maps/search/food+shelters/@"+current_lat+","+current_lon+",13z")
    context.bot.send_message(chat_id=update.effective_chat.id, text="*Below you can find the food shelters in this area*\n"+response,parse_mode=telegram.ParseMode.MARKDOWN)
    s = pyshorteners.Shortener(Shorteners.TINYURL)
    response1 = s.short("https://www.google.com/maps/search/night+shelters/@"+current_lat+","+current_lon+",12z")
    context.bot.send_message(chat_id=update.effective_chat.id, text="*Below you can find the Night shelters in this area*\n"+response1,parse_mode=telegram.ParseMode.MARKDOWN)

def ask_state_for_districtwise_msg():
    return 'Which state\'s district count do you want?'

def get_district_msg(state_name):
    
    jsonContent = apiRequestsIndia()
    state_data = []
    for s in jsonContent[1]:
        if s['statecode'].lower() == state_name.lower().strip():
            state_name = s['state']
            state_data = s['districtData']
            break
    districtwise_msg = "No data found for State {state_name}".format(state_name=state_name)
    if state_data != []:
        state_data = sorted(state_data, key = lambda i: i['confirmed'],reverse=True)
        districtwise_msg = "District-wise Covid-19 stats till now in <b>{state_name}</b>\n".format(state_name=state_name)
        for district in state_data:
            formatted_district_data = "\n<b>{district_name}</b>\nActive:{active}\nConfirmed:{confirmed:4}{delta_confirmed}\nRecovered:{recovered}{delta_recovered}\nDeaths:{death}{delta_death}\n".format(confirmed=district['confirmed'], delta_confirmed=get_delta_msg(district), district_name= district['district'], recovered=get_msg_r(district),delta_recovered=get_delta_r(district), death=get_msg_d(district),delta_death=get_delta_d(district),active=get_msg_a(district))
            districtwise_msg += formatted_district_data
        districtwise_msg += "\nData last updated at " + get_lastupdated_msg()
    return districtwise_msg

def get_delta_msg(district):
    delta_msg = ""
    if district['delta']['confirmed'] != 0:
        delta_msg += "(↑{delta_count})".format(delta_count=district['delta']['confirmed'])
    elif district['delta']['confirmed'] == 0:
        delta_msg += "(0)"
    return delta_msg

def get_msg_a(district):
    msg_a = ""
    if district['active'] != 0:
        msg_a += "{count}".format(count=district['active'])
    elif district['active'] == 0:
        msg_a += "0"
    return msg_a

def get_msg_r(district):
    msg_r = ""
    if district['recovered'] != 0:
        msg_r += "{count}".format(count=district['recovered'])
    elif district['recovered'] == 0:
        msg_r += "0"
    return msg_r

def get_delta_r(district):
    delta_msg_r = ""
    if district['delta']['recovered'] != 0:
        delta_msg_r += "(↑{delta_count})".format(delta_count=district['delta']['recovered'])
    elif district['delta']['recovered'] == 0:
        delta_msg_r += "(0)"
    return delta_msg_r

def get_msg_d(district):
    msg_d = ""
    if district['deceased'] != 0:
        msg_d += "{count}".format(count=district['deceased'])
    elif district['deceased'] == 0:
        msg_d += "0"
    return msg_d

def get_delta_d(district):
    delta_msg_d = ""
    if district['delta']['deceased'] != 0:
        delta_msg_d += "(↑{delta_count})".format(delta_count=district['delta']['deceased'])
    elif district['delta']['deceased'] == 0:
        delta_msg_d += "(0)"
    return delta_msg_d

def get_lastupdated_msg():
    jsonContent = apiRequestsIndia()
    msg_lastupdated = jsonContent[0]['statewise'][0]['lastupdatedtime']
    print (msg_lastupdated)
    return msg_lastupdated

def districtwise(update: telegram.Update, context: CallbackContext):
    message = ask_state_for_districtwise_msg()
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=telegram.ForceReply(),
    )
    logger.info("Districtwise handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def handle_message(update: telegram.Update, context: CallbackContext):
    if update.message.reply_to_message:
        if (update.message.reply_to_message.text== ask_state_for_districtwise_msg()):
            message = get_district_msg(update.message.text)
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML
    )    

def getLocation1(update, context, var, var1, time_u):
    
    current_lat = var
    current_lon = var1
    last_updated_time = time_u
    
    contents = requests.get("http://apis.mapmyindia.com/advancedmaps/v1/"+API_key_M+"/rev_geocode?lat="+current_lat+"&lng="+current_lon+"&format=json").json()
    #print(contents)
    for each in contents['results']:
        stateName = str(each["state"])
        district = str(each["district"])
    dist = str((district.replace("District","")).strip())
    
    rd = requests.get('https://api.covid19india.org/state_district_wise.json')
    rdj = rd.json()
    state = rdj[stateName]
    dist = districtIN(dist)
    zoneD = zones(update, context, dist)
    try:
        active = str(state["districtData"][dist]["active"])
        confirmed_d = str(state["districtData"][dist]["confirmed"])
        new_case = str(state["districtData"][dist]["delta"]["confirmed"])
        death = str(state["districtData"][dist]["deceased"])
        delta_death = str(state["districtData"][dist]["delta"]["deceased"])
        recovered = str(state["districtData"][dist]["recovered"])
        delta_recovered = str(state["districtData"][dist]["delta"]["recovered"])
        print(recovered)
        testR = testRate(stateName)
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in *"+dist+"*\
        \n\
        \nActive Cases        : *"+active+"*\
        \nConfirmed Cases : *"+confirmed_d+"* *(↑"+new_case+")*\
        \nDeath Cases         : *"+death+"* *(↑"+delta_death+")*\
        \nRecovered Cases : *"+recovered+"* *(↑"+delta_recovered+")*\
        \nZone                      : *"+zoneD+"*\
        \nThis data was last updated at *"+last_updated_time+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You requested for *"+dist+"* district for which there are no stats at the moment")

    logger.info("location for district handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def us_statewise(update, context):
    var = ' '.join(context.args)
    print(var)
    jsonContent = apiRequestUSA()
    if var == "":
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a Letter to list the US state names , Ex: '/ListUSAStates N",parse_mode=telegram.ParseMode.MARKDOWN)
    elif (var.isdigit()):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a Letter to list the US state names , Ex: '/ListUSAStates N",parse_mode=telegram.ParseMode.MARKDOWN)
    elif(regex.search(var)) == None:
        letter = var.capitalize()
        print(letter)
        state_us = []
        code_us = []
        stateCount = str(len(jsonContent[0]))
        for each in jsonContent[0]:   
            US_state_name = str(each["name"]) 
            if US_state_name.startswith(letter):
                state_us.append(each["name"])
                code_us.append(each["state"])

        StateName_StateCode = ' \n'.join(["For "+ str(a) +" use code "+ b for a,b in zip(state_us,code_us)])
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="There are *"+stateCount+"* States in USA. Below are the names starting with letter *"+letter+"* and their codes\n\n\n*"+StateName_StateCode+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a Letter to list the US state names , Ex: '/ListUSAStates N",parse_mode=telegram.ParseMode.MARKDOWN)
    logger.info("US State code handler used ", update.message.chat.id, update.message.from_user.first_name)   
    captureID(update)

def us_statewise_stats(var):
    jsonContent = apiRequestUSA()
    for each in jsonContent[1]:
        if str(each["state"]) == var:
           confirmed = str(each["positive"]) 
           deaths = str(each["death"]) 
           recovered = str(each["recovered"])
           lastupdatedtime = str(each["lastUpdateEt"])
    return confirmed,deaths,recovered,lastupdatedtime

def getUS_stateName(var):
    jsonContent = apiRequestUSA()
    for each in jsonContent[0]:
        if str(each["state"]) == var:   
            state_name1 = str(each["name"])
    return state_name1

def usa_state(update, context):
    us_state_code = ' '.join(context.args).upper()
    print(us_state_code)
    if (us_state_code.isdigit()):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a statecode, Ex: '/USAState AK'",parse_mode=telegram.ParseMode.MARKDOWN)
    elif us_state_code == "":
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a statecode, Ex: '/USAState AK'",parse_mode=telegram.ParseMode.MARKDOWN)
    elif(regex.search(us_state_code)) == None:
        state_it = usaStateCode(us_state_code)
        sN = getUS_stateName(us_state_code)
        jsonContentUS = apiUSAStates(state_it)
        jsonContentUS_yday = apiUSAStatesYday(state_it)
        #for each in jsonContentUS:
        active = str(jsonContentUS["active"])
        cases = str(jsonContentUS["cases"])
        todayCases = str(jsonContentUS["todayCases"])
        deaths = str(jsonContentUS["deaths"])
        todayDeaths = str(jsonContentUS["todayDeaths"])
        recovered = ((int(cases)) - (int(active)))
        CasesYday = str(jsonContentUS_yday["cases"])
        NewCasesYday = str(jsonContentUS_yday["todayCases"])
        updated = str(datetime.fromtimestamp((jsonContentUS["updated"])/1000).replace(microsecond=0))
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The stats for *"+sN+"*\
        \n\
        \nConfirmed Cases  : *"+cases+"**(↑"+todayCases+")*\
        \nDeath Cases         : *"+deaths+"**(↑"+todayDeaths+")*\
        \nActive Cases        : *"+active+"*\
        \nRecovered Cases  : *"+str(recovered)+"*\
        \nCases yesterday  : *"+CasesYday+"**(↑"+NewCasesYday+")*\
        \nThis data was last updated at : *"+updated+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        
        """ content_k = us_statewise_stats(us_state_code)
        sN = getUS_stateName(us_state_code)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The stats for *"+sN+"* are:\
        \n\
        \nConfirmed Cases  : *"+content_k[0]+"*\
        \nDeath Cases       : *"+content_k[1]+"*\
        \nRecovered Cases  : *"+content_k[2]+"*\
        \nThis data was last updated at : *2020/"+content_k[3]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
     """
    else:
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a statecode correctly , Ex: '/USAState AK",parse_mode=telegram.ParseMode.MARKDOWN)   
    logger.info("State handler used ", update.message.chat.id, update.message.from_user.first_name)
    print("This User checked "+sN+":"+update.message.from_user.first_name)
    captureID(update)

def getLocation2(update, context, var, var1):
    current_lat = var
    current_lon = var1
    jsonContent = apiRequestUSA()
    contents = requests.get("https://locationiq.com/v1/reverse.php?key="+APIKey_LQ+"&lat="+current_lat+"&lon="+current_lon+"&format=json").json()
    county = contents["address"]["county"]
    #countyName = county.split(' ',1)[0]
    countyName = str((county.replace("County","")).strip())
    for each in jsonContent[2]:
        if str(each["county"]) == countyName:
            confirmed = str(each["stats"]["confirmed"]) 
            deaths = str(each["stats"]["deaths"]) 
            recovered = str(each["stats"]["recovered"])
            updatedAt = str(each["updatedAt"])
    print(countyName)
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in county *"+countyName+"*\
        \n\
        \nConfirmed Cases : *"+confirmed+"*\
        \nDeath cases     : *"+deaths+"*\
        \nRecovered cases : *"+recovered+"*\
        \nThis data was last updated at *"+updatedAt+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for county *"+countyName+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def continent_count(var):
    continent = requests.get('https://corona.lmao.ninja/v2/continents?yesterday=true&sort')
    continent_v = continent.json()
    for each in continent_v:
        if str(each["continent"]) == var:
           confirmed = str(each["cases"]) 
           deaths = str(each["deaths"]) 
           recovered = str(each["recovered"])
           deltaconfirmed = str(each["todayCases"])
           deltadeaths = str(each["todayDeaths"])
           lastUpdatedTime = str(datetime.fromtimestamp((each["updated"])/1000).replace(microsecond=0))
    return confirmed,deaths,recovered,deltaconfirmed,deltadeaths,lastUpdatedTime

def asia(update, context):
    continentCount = continent_count("Asia")
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="The numbers for *Asia* are as below\
    \n\
    \nConfirmed Cases : *"+continentCount[0]+"* *(↑"+continentCount[3]+")*\
    \nDeath Cases        : *"+continentCount[1]+"* *(↑"+continentCount[4]+")*\
    \nRecovered Cases : *"+continentCount[2]+"*\
    \nThis data was last updated at of : *"+continentCount[5]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked Asia: "+update.message.from_user.first_name)
    logger.info("Asia handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def africa(update, context):
    continentCount = continent_count("Africa")
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="The numbers for *Africa* are as below\
    \n\
    \nConfirmed Cases : *"+continentCount[0]+"* *(↑"+continentCount[3]+")*\
    \nDeath Cases        : *"+continentCount[1]+"* *(↑"+continentCount[4]+")*\
    \nRecovered Cases : *"+continentCount[2]+"*\
    \nThis data was last updated at of : *"+continentCount[5]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked Asia: "+update.message.from_user.first_name)
    logger.info("Africa handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def northamerica(update, context):
    continentCount = continent_count("North America")
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="The numbers for *North America* are as below\
    \n\
    \nConfirmed Cases : *"+continentCount[0]+"* *(↑"+continentCount[3]+")*\
    \nDeath Cases        : *"+continentCount[1]+"* *(↑"+continentCount[4]+")*\
    \nRecovered Cases : *"+continentCount[2]+"*\
    \nThis data was last updated at of : *"+continentCount[5]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked Asia: "+update.message.from_user.first_name)
    logger.info("North America handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def europe(update, context):
    continentCount = continent_count("Europe")
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="The numbers for *Europe* are as below\
    \n\
    \nConfirmed Cases : *"+continentCount[0]+"* *(↑"+continentCount[3]+")*\
    \nDeath Cases        : *"+continentCount[1]+"* *(↑"+continentCount[4]+")*\
    \nRecovered Cases : *"+continentCount[2]+"*\
    \nThis data was last updated at of : *"+continentCount[5]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked Asia: "+update.message.from_user.first_name)
    logger.info("Europe handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def southamerica(update, context):
    continentCount = continent_count("South America")
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="The numbers for *South America* are as below\
    \n\
    \nConfirmed Cases : *"+continentCount[0]+"* *(↑"+continentCount[3]+")*\
    \nDeath Cases        : *"+continentCount[1]+"* *(↑"+continentCount[4]+")*\
    \nRecovered Cases : *"+continentCount[2]+"*\
    \nThis data was last updated at of : *"+continentCount[5]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked Asia: "+update.message.from_user.first_name)
    logger.info("South America handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def australia(update, context):
    continentCount = continent_count("Oceania")
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="The numbers for *Australia* are as below\
    \n\
    \nConfirmed Cases : *"+continentCount[0]+"* *(↑"+continentCount[3]+")*\
    \nDeath Cases         : *"+continentCount[1]+"* *(↑"+continentCount[4]+")*\
    \nRecovered Cases : *"+continentCount[2]+"*\
    \nThis data was last updated at of : *"+continentCount[5]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked Asia: "+update.message.from_user.first_name)
    logger.info("Australia handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocation3(update, context, var, var1):
    current_lat = var
    current_lon = var1
    G_stateName = germanToEnglish(update, context, current_lat, current_lon)
    jsonContent = apiRequestGermany()
    for each in jsonContent['states']:    
        if str(each["name"]) == G_stateName:
            confirmed = str(each["count"]) 
            deaths = str(each["deaths"]) 
            newcases = str(each["difference"])
    print(G_stateName)
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in state *"+G_stateName+"*\
        \n\
        \nConfirmed Cases : *"+confirmed+"* *(↑"+newcases+")*\
        \nDeath Cases        : *"+deaths+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for state *"+G_stateName+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationJP(update, context, prefecture):
    state_japan = prefecture
    jsonContent = apiRequestJapan()
    updatedTime = jsonContent["updated"]
    uT = updatedTime.replace("T"," ")
    UT = uT.replace("+09:00","")
    #d1 = datetime.strptime(updatedTime,"%Y-%m-%dT%H:%M:%S%z:%z")
    #uT = d1.strftime("%Y-%m-%d %H:%M:%S")
    for each in jsonContent['prefectures']:    
        if str(each["name"]) == state_japan:
            confirmed = str(each["confirmed"]) 
            deaths = str(each["deceased"]) 
            newcases = str(each["newlyConfirmed"])
            recovered = str(each["recovered"])
            new_death = str(each["newlyDeceased"])
    print(state_japan)
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in prefecture *"+state_japan+"*\
        \n\
        \nConfirmed Cases  : *"+confirmed+"* *(↑"+newcases+")*\
        \nDeath Cases         : *"+deaths+"* *(↑"+new_death+")*\
        \nRecovered Cases  : *"+recovered+"*\
        \nThis data was last updated at *"+UT+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for state *"+state_japan+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler JP used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationUK(update, context, regionUK):
    region = regionUK
    if regionUK == "Greater London":
        region = str((regionUK.replace("Greater","")).strip()).capitalize()
    elif regionUK == "Yorkshire and the Humber":
        region = "Yorkshire and The Humber"
    elif regionUK == "South West England":
        region = "South West"
    elif regionUK == "South East England":
        region = "South East"
    elif regionUK == "North East England":
        region = "North East"
    elif regionUK == "North West England":
        region = "North West"

    jsonContent = apiRequestUK()
    print(regionUK)
    updatedTime = jsonContent["metadata"]["lastUpdatedAt"]
    d1 = datetime.strptime(updatedTime,"%Y-%m-%dT%H:%M:%S.%fZ")
    uT = d1.strftime("%Y-%m-%d %H:%M:%S")
    
    for each in jsonContent['regions']:    
        if str(each["areaName"]) == region:
            confirmed = str(each["totalLabConfirmedCases"])
            newcases = str(each["dailyLabConfirmedCases"])
            break
    print(str(each["areaName"]))
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in region *"+region+"*\
        \n\
        \nConfirmed Cases : *"+confirmed+"**(↑"+newcases+")*\
        \nThe data was last updated on *"+uT+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for region *"+region+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler JP used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationNL(update, context, cityNL):
    cityNew = cityNL
    if cityNew == "The Hague":
        cityNew = "'s-Gravenhage"
    jsonContent = apiRequestNL()
    print(cityNew)
    for each in jsonContent["features"]:    
        if str(each['properties']["Gemeentenaam"]) == cityNew:
            confirmed = str(each['properties']["Meldingen"])
            deaths = str(each['properties']["Overleden"])
            province = str(each['properties']["Provincie"])
            updatedTime = (str(each['properties']["Datum"])).split()
            break
    print(str(each['properties']["Provincie"]))
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in region *"+cityNew+"* and is from Province *"+province+"*\
        \n\
        \nConfirmed Cases : *"+confirmed+"*\
        \nDeath Cases     : *"+deaths+"*\
        \nThis data was last updated on *"+updatedTime[0]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for city *"+cityNew+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler JP used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationRU(update, context, stateRU):
    state = stateRU
    try:
        c = region(state)
        print(c[0])
        jsonContent = apiRequestRU(c[0])
        for each in jsonContent:    
            confirmed = str(each['sick'])
            recovered = str(each['healed'])
            deaths = str(each['died'])
            date = str(each["date"])
            break
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in region *"+c[1]+"*\
        \n\
        \nConfirmed Cases : *"+confirmed+"*\
        \nDeath Cases       : *"+deaths+"*\
        \nRecovered Cases : *"+recovered+"*\
        \nThis data was last updated on *"+date+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for region *"+state+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler RU used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationAUS(update, context, stateAUS):
    stateau = stateAUS
    jsonContentAU = apiRequestAUS()
    for each in jsonContentAU["sheets"]["latest totals"]:
        if str(each["Long name"]) == stateAUS:
            confirmed = str(each["Confirmed cases (cumulative)"])
            recovered = str(each["Recovered"])
            deaths = str(each["Deaths"])
            date = str(each["Last updated"])
            break
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in region *"+stateAUS+"*\
        \n\
        \nConfirmed Cases  : *"+confirmed+"*\
        \nDeath Cases        : *"+deaths+"*\
        \nRecovered Cases  : *"+recovered+"*\
        \nThis data was last updated on *"+date+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for region *"+stateau+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler AUS used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationCA(update, context, provinceCA):
    provinceNew = provinceCA
    jsonContent = apiRequestCAN()
    print(provinceNew)
    today = datetime.today()
    yesterday = today - timedelta(days = 1)
    yday = yesterday.strftime('%Y/%m/%d')
    tday = today.strftime('%Y/%m/%d')
    print(tday)
    print(yday)
    for each in jsonContent["features"]:    
        if str(each['properties']["Province"]) == provinceNew:
            val = str(each['properties']["SummaryDate"]).split()
            if(str(val[0].strip()) == tday) or (str(val[0].strip()) == yday):
                confirmed = str(each['properties']["TotalCases"])
                deaths = str(each['properties']["TotalDeaths"])
                province = str(each['properties']["Province"])
                recovered = str(each["properties"]["TotalRecovered"])
                newCases = str(each["properties"]["DailyTotals"])
                print(str(each['properties']["Province"]))
                break
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in province *"+province+"*\
        \n\
        \nConfirmed Cases : *"+confirmed+"* *(↑"+newCases+")*\
        \nDeath Cases       : *"+deaths+"*\
        \nRecovered Cases : *"+recovered+"*\
        \nThe data was last updated at *"+val[0]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for province is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler CA used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationES(update, context, provinceCA):
    
    provinceNew = regionES(provinceCA)
    print(provinceNew)
    today = datetime.today()
    yesterday = today - timedelta(days = 1)
    yday = yesterday.strftime('%Y-%m-%d')
    tday = today.strftime('%Y-%m-%d')
    jsonContent = apiRequestES(tday)
    print(tday)
    print(yday)
    for each in jsonContent["dates"][tday]["countries"]["Spain"]["regions"]:    
        if str(each['name']) == provinceNew:
            confirmed = str(each['today_confirmed'])
            deaths = str(each["today_deaths"])
            province = str(each['name'])
            recovered = str(each["today_recovered"])
            newCases = str(each["today_new_confirmed"])
            break
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in province *"+province+"*\
        \n\
        \nConfirmed Cases : *"+confirmed+"* *(↑"+newCases+")*\
        \nDeath Cases       : *"+deaths+"*\
        \nRecovered Cases : *"+recovered+"*\
        \nThe data was last updated at *"+tday+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for province is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler ES used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationBR(update, context, stateBR):
    state_BR = stateBR
    jsonContent = apiRequestBrazil()
    if state_BR=="Federal District":
        state_BR = "Distrito Federal"
    for each in jsonContent['data']:    
        if str(each["state"]) == state_BR:
            confirmed = str(each["cases"]) 
            deaths = str(each["deaths"])
            updatedTime = str(each["datetime"])
            break
    d1 = datetime.strptime(updatedTime,"%Y-%m-%dT%H:%M:%S.%fZ")
    uT = d1.strftime("%Y-%m-%d %H:%M:%S")
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in state *"+state_BR+"*\
        \n\
        \nConfirmed Cases  : *"+confirmed+"*\
        \nDeath Cases          : *"+deaths+"*\
        \nThe data was last updated at *"+uT+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for state *"+state_BR+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler BR used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationFR(update, context, countyFR):
    state = countyFR
    
    try:
        dept = regionFRA(state)
        print(dept)
        jsonContent = apiRequestFR(dept)
        for each in jsonContent["LiveDataByDepartement"]:    
            confirmed = str(each['hospitalises'])
            recovered = str(each['gueris'])
            deaths = str(each['deces'])
            date = str(each["date"])
            ICU = str(each["reanimation"])
            break
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in Département *"+dept+"*\
        \n\
        \nConfirmed Cases(hospitalises)       : *"+confirmed+"*\
        \nDeath Cases(deces)                         : *"+deaths+"*\
        \nRecovered Cases(gueris)                : *"+recovered+"*\
        \nCases Intensive Care(reanimation) : *"+ICU+"*\
        \nThis data was last updated on *"+date+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for Département *"+countyFR+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler FR used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationIT(update, context, stateIT):
    print(stateIT)
    state_it = regionIT(stateIT)
    jsonContent = apiRequestItaly()
    try:
        if state_it == "P.A. Bolzano P.A. Trento" :
            for each in jsonContent:
                if str(each["region"]) == "P.A. Bolzano":
                    confirmed = str(each['totalCases'])
                    newCases = str(each['newCases'])
                    recovered = str(each['recovered'])
                    deaths = str(each['deaths'])
                    updated = str(datetime.fromtimestamp((each["updated"])/1000).replace(microsecond=0))
                    break
            context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in region/state *P.A. Bolzano* or\
            \n\
            \nConfirmed Cases   : *"+confirmed+"* *(↑"+newCases+")*\
            \nDeath Cases           : *"+deaths+"*\
            \nRecovered Cases   : *"+recovered+"*\
            \nThis data was last updated on *"+updated+"*",parse_mode=telegram.ParseMode.MARKDOWN)

            for each in jsonContent:
                if str(each["region"]) == "P.A. Trento":
                    confirmed = str(each['totalCases'])
                    newCases = str(each['newCases'])
                    recovered = str(each['recovered'])
                    deaths = str(each['deaths'])
                    updated = str(datetime.fromtimestamp((each["updated"])/1000).replace(microsecond=0))
                    break
            context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in region/state *P.A. Trento*\
            \n\
            \nConfirmed Cases   : *"+confirmed+"* *(↑"+newCases+")*\
            \nDeath Cases           : *"+deaths+"*\
            \nRecovered Cases   : *"+recovered+"*\
            \nThis data was last updated on *"+updated+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            for each in jsonContent:
                if str(each["region"]) == state_it:
                    confirmed = str(each['totalCases'])
                    newCases = str(each['newCases'])
                    recovered = str(each['recovered'])
                    deaths = str(each['deaths'])
                    updated = str(datetime.fromtimestamp((each["updated"])/1000).replace(microsecond=0))
                    break
            context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in region/state *"+state_it+"*\
            \n\
            \nConfirmed Cases   : *"+confirmed+"* *(↑"+newCases+")*\
            \nDeath Cases           : *"+deaths+"*\
            \nRecovered Cases   : *"+recovered+"*\
            \nThis data was last updated on *"+updated+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for region *"+state_it+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler IT used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def getLocationMX(update, context, state_mx):
    state_mex = state_mx
    print(state_mex)
    
    state = stateMX(state_mex)
    print(state)
    jsonContent = apiRequestMexStates()
    updatedTime = str(jsonContent["lastUpdatedAtSource"])
    d1 = datetime.strptime(updatedTime,"%Y-%m-%dT%H:%M:%S.%fZ")
    uT = d1.strftime("%Y-%m-%d %H:%M:%S")
    confirmed = str(jsonContent["State"][state]['infected'])
    deaths = str(jsonContent["State"][state]['deceased'])
    try:
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in Département *"+state+"*\
        \n\
        \nConfirmed Cases   : *"+confirmed+"*\
        \nDeath Cases           : *"+deaths+"*\
        \nThis data was last updated on *"+uT+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The data for state *"+state_mex+"* is not there at the moment",parse_mode=telegram.ParseMode.MARKDOWN)

    logger.info("location for county handler MX used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def germanToEnglish(update,context,var,var1):
    current_lat = var
    current_lon = var1
    contents = requests.get("https://locationiq.com/v1/reverse.php?key="+APIKey_LQ+"&lat="+current_lat+"&lon="+current_lon+"&format=json").json()
    try:
        state = contents["address"]["state"]
        if state == "North Rhine-Westphalia":
            state = "Nordrhein-West­falen"
        elif state == "Baden-Württemberg":
            state = "Baden-Württem­berg"
        elif state =="Bavaria":
            state = "Bayern"
        elif state =="Free Hanseatic City of Bremen":
            state = "Bremen"
        elif state =="Hesse":
            state = "Hessen"
        elif state =="Mecklenburg-Vorpommern":
            state = "Mecklenburg-Vor­pommern"
        elif state =="Lower Saxony":
            state = "Niedersachsen"
        elif state =="Rhineland-Palatinate":
            state = "Rhein­land-Pfalz"
        elif state =="Saxony":
            state = "Sachsen"
        elif state =="Saxony-Anhalt":
            state = "Sachsen-Anhalt"
        elif state =="Schleswig-Holstein":
            state = "Schles­wig-Holstein"
        elif state =="Thuringia":
            state = "Thüringen"
    except:
        state = contents["address"]["city"]

    return state

def getLocationMY(update, context, stateMY):
    val = state_malaysia(stateMY)
    context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in state *"+stateMY+"*\
        \n\
        \nConfirmed Cases   : *"+val[0]+"**("+val[3]+")*\
        \nDeath Cases           : *"+val[1]+"*\
        \nThis data was last updated on *"+val[2]+"*",parse_mode=telegram.ParseMode.MARKDOWN) 

    logger.info("location for county handler MY used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def healthCheck(update,context):
    df= pd.read_csv('api.csv')
    
    for url in df['urls']:
        response= requests.get(url)
        status= response.status_code
        if status != 200:
            context.bot.send_message(chat_id=update.effective_chat.id, text="API down for "+url,parse_mode=telegram.ParseMode.MARKDOWN)
        else :
            context.bot.send_message(chat_id=update.effective_chat.id, text="API is Up and running",parse_mode=telegram.ParseMode.MARKDOWN)

def News():
    
    main_url = "https://newsapi.org/v2/top-headlines?q=covid-19&language=en&apiKey="+NewsAPIKey
  
    # fetching data in json format 
    open_news_page = requests.get(main_url).json() 
    # getting all articles in a string article 
    article = open_news_page["articles"] 
    # empty list which will  
    # contain all trending news urls
    results = [] 
    for ar in article: 
        results.append(ar["url"]) 
    
    file = open("links.txt","w")      
    for i in range(len(results)): 
        # printing all trending news 
        file.write(results[i]+'\n')
    file.close()

def getNews(update,context):

    News()
    news = random_newsArticle('links.txt')
    context.bot.send_message(chat_id=update.effective_chat.id, text=news)
    logger.info("news handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

def countryTrend(update, context, code, conf, dead, countryName):
    ISO = code.upper()
    if ISO=="GB":
        ISO='UK'
    if ISO=="GR":
        ISO="EL"
    print(ISO)
    try:
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open("/home/ravindra/country/"+ISO+".png",'rb'))
    except:
        url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
        wget.download(url)
    #https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx
        ##Read the data
        data = pd.read_excel('COVID-19-geographic-disbtribution-worldwide.xlsx')

        #Change it to the country of your choice
        
        ##Reverse the data
        data = data.reindex(index=data.index[::-1])

        ##Remove the dates with no cases
        data = data[data.cases != 0]

        #indexNames = data[ data['popData2018'] == 3000].index
        #data.drop(indexNames , inplace=True)
        ##Remove useless columns
        data = data.drop(columns=['day', 'month', 'year', 'countryterritoryCode', 'popData2018'])
        #data = data.drop(data[data['geoId'] =='JPG11668'].index, inplace = True)

        ## Make the name of the columns more clean
        data.rename(columns={"countriesAndTerritories": "Country", 'dateRep': 'Date', 'cases': 'Cases', 'deaths': 'Deaths', 'geoId': 'Iso'}, inplace=True)

        ##Use only data for specific country
        data = data[data['Iso'].str.contains(ISO)== True]

        ## Total Death Percentage
        total_death_percentage = data.Deaths.sum() / data.Cases.sum() * 100
        print('\nTotal Death Percentage: ' + str(total_death_percentage) + '%')

        ## Total Cases and Deaths
        print('Total Cases: ', data.Cases.sum())
        print('Total Deaths: ', data.Deaths.sum())
        deaths = dead
        cases = conf
        country = countryName
        ## Plot size
        matplotlib.rcParams['figure.figsize'] = (70.0, 30.0)
        matplotlib.rcParams['font.size'] = (30)
        matplotlib.rcParams['legend.fontsize'] = (50)
        matplotlib.rcParams['xtick.major.pad']='10'
        ## Plot for Cases And Deaths(Greece)
        ax = plt.subplot()
        ax.xaxis.set_minor_locator(AutoMinorLocator(10))
        ax.plot(data.set_index('Date')['Cases'],color='blue', label='Total Cases= '+cases,linestyle='solid',linewidth=8.0)
        #ax.grid(b=True, which='major', color='b', linestyle='-',linewidth=4)
        ax.plot(data.set_index('Date')['Deaths'], color='red',label='Total Deaths= '+deaths,linestyle='--',linewidth=8.0)
        ax.set(xlabel='Date', ylabel='New cases')
        ax.set_title(country+': Daily New Cases And New Deaths',fontsize= 80)
        #ax.grid(b=True, which='major', color='b', linestyle='-',linewidth=4)
        ax.grid()
        ax.xaxis.get_label().set_fontsize(50)
        ax.yaxis.get_label().set_fontsize(50)
        #ax.set_xticks(rotation=45)'-*-' is not a valid value for ls; supported values are '-', '--', '-.', ':', 'None', ' ', '', 'solid','dashed', 'dashdot', 'dotted'
        
        ax.legend()
        #plt.show()
        plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        plt.savefig("/home/ravindra/country/"+ISO+'.png')
    
        os.remove("COVID-19-geographic-disbtribution-worldwide.xlsx")
        #os.remove(ISO+'.png')
        plt.cla()
        plt.clf()
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open("/home/ravindra/country/"+ISO+".png",'rb'))
    
def random_newsArticle(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))
    
def travel(update,context,code):
    
    jsonContent = apiTravelAlert()
    for each in jsonContent:
        if str(each["countryCode"]) == str(code).upper():
            countryName = str(each["countryName"]) 
            alertMessage = str(each["alertMessage"]) 
            print(countryName)
            print(len(alertMessage))
            if (len(alertMessage))>4096:
                lines = (i.strip() for i in alertMessage.splitlines())
                for line in lines:
                    for chunk in chunkstring(line, 4096):
                        print(chunk)
                        context.bot.send_message(chat_id=update.effective_chat.id, text="\
                        \n*"+chunk+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    return countryName,alertMessage
    
def travelAlert(update, context):
    country_code = ' '.join(context.args)
    letter = country_code.capitalize()
    print(country_code)
    if (country_code.isdigit()):
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a country code, Ex:'/travelAdvice NL'",parse_mode=telegram.ParseMode.MARKDOWN)
    elif country_code == "":
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text="Add a country code, Ex:'/travelAdvice NL'",parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        content_k = travel(update,context,letter)
        FlagIcon = flag.flag(letter)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The Travel Advice from country *"+content_k[0]+"* "+FlagIcon+" is as below\
        \n\
        \n*"+content_k[1]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        #context.bot.send_photo(chat_id=update.message.chat_id, photo=photo_file,parse_mode=telegram.ParseMode.MARKDOWN)
        print("This User checked travel alert:"+update.message.from_user.first_name)
        logger.info("Country handler used ", update.message.chat.id, update.message.from_user.first_name)
        captureID(update)

def get_state_msg():
    
    jsonContent = apiRequestsIndia()
    state_data = sorted(jsonContent[0]["statewise"], key = lambda i: (int(i['deltaconfirmed']),i['state']),reverse=True)
    #state_msg = "State-wise Covid-19 stats till now in <b>{state_name}</b>\n".format(state_name=state_name)
    for each in state_data:
        confirmed = str(each["confirmed"]) 
        deltaconfirmed = str(each["deltaconfirmed"])
        stateName = str(each["state"])
    return state_data

def indianStatesSorted(update, context):
    #var = ' '.join(context.args)
    state = []
    confirmed =[]
    delta_confirmed=[]
    jsonContent = apiRequestsIndia()
    for each in jsonContent[0]["statewise"]:
        delta_confirmed.append(int(each["deltaconfirmed"]))
        state.append(str(each["state"]))
        confirmed.append(str(each["confirmed"]))
    #print(confirmed)
    delta_confirmed.sort(reverse = True)
    j=0
    for i in jsonContent[0]["statewise"]:
        for each in jsonContent[0]["statewise"]:
            confirmedN = each["deltaconfirmed"]
            if (i == confirmedN):
                delta_confirmed.append(str(each["deltaconfirmed"]))
                state.append("No:"+str(j+1)+">> "+str(each["state"])) 
                confirmed.append(str(each["confirmed"]))
                j += 1
                
    countryName_confirmed = ' \n'.join(["*"+str(a)+"*"+" has *"+ str(b) +"* new cases and *"+str(c)+"* confirmed cases" for a,b,c in zip(state,delta_confirmed,confirmed)])
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text="Indian states with new confirmed cases of Covid-19 are : \
    \n\
    \n"+countryName_confirmed+"",parse_mode=telegram.ParseMode.MARKDOWN)

def main():
    BotToken = ""
    updater = Updater(BotToken,use_context=True)
    print (dateToday())
    #print(get_state_msg())
    dp = updater.dispatcher
    logging.basicConfig(
        filename="bot.log",
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('india',india))
    dp.add_handler(CommandHandler('state',indianstate))
    dp.add_handler(CommandHandler('world',world))
    dp.add_handler(CommandHandler('statecode',indian_state_code))
    dp.add_handler(CommandHandler('countrycode',country_code))
    dp.add_handler(CommandHandler('country',countryWiseData))
    dp.add_handler(CommandHandler('official_TC',officialTelegramChannels))
    dp.add_handler(CommandHandler('topD',topD))
    dp.add_handler(CommandHandler('topC',topC))
    dp.add_handler(CommandHandler('indianStatesSorted',indianStatesSorted))
    dp.add_handler(CommandHandler('districtwise',districtwise))
    dp.add_handler(CommandHandler('ListUSAStates',us_statewise))
    dp.add_handler(CommandHandler('USAState',usa_state))
    dp.add_handler(CommandHandler('asia',asia))
    dp.add_handler(CommandHandler('africa',africa))
    dp.add_handler(CommandHandler('europe',europe))
    dp.add_handler(CommandHandler('northamerica',northamerica))
    dp.add_handler(CommandHandler('southamerica',southamerica))
    dp.add_handler(CommandHandler('australia',australia))
    dp.add_handler(CommandHandler('healthcheck',healthCheck))
    dp.add_handler(CommandHandler('commands',commands))
    dp.add_handler(CommandHandler('news',getNews))
    dp.add_handler(CommandHandler('travelAdvice',travelAlert))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.location,getLocation))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()