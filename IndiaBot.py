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
from pyshorteners import Shorteners

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)
today = date.today()
regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


def apiRequestsIndia():
    r = requests.get('https://api.covid19india.org/data.json')
    j = r.json()
    r = requests.get('https://api.covid19india.org/v2/state_district_wise.json')
    dist_data = r.json()

    return j,dist_data

def apiWorld():
    rCountry1 = requests.get('https://corona.lmao.ninja/v2/countries')
    jCountry1 = rCountry1.json()
    return jCountry1

def apiRequestUSA():
    rUS = requests.get('https://covidtracking.com/api/states/info')
    jstates = rUS.json()

    rUS_states = requests.get('https://covidtracking.com/api/states')
    states_us = rUS_states.json()

    us_county = requests.get('https://corona.lmao.ninja/v2/jhucsse/counties')
    county_us = us_county.json()

    return jstates,states_us,county_us

def apiRequestGermany():
    germany = requests.get("https://rki-covid-api.now.sh/api/states")
    statejson = germany.json()
    return statejson
    
def apiWorldNew():
    world = requests.get("https://corona.lmao.ninja/v2/all").json()
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

APIKey_LQ = ""
API_key_M = ""

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
        \nConfirmed cases  : *"+content[0]+"* *(↑"+content[1]+")*\
        \nDeath cases           : *"+content[3]+"* *(↑"+content[2]+")*\
        \nRecovered cases   : *"+content[4]+"*\
        \nAffected countries  : *"+content[5]+"*\
        \nActive cases          :*"+content[6]+"*\
        \nCases per million     :*"+content[7]+"*\
        \nDeaths per million    :*"+content[8]+"*\
        \nTests                 :*"+content[9]+"*\
        \nTests per million     :*"+content[10]+"*\
        \nActive per million    :*"+content[11]+"*\
        \nRecovered per million :*"+content[12]+"*\
        \nThis data was last updated at *"+str(updatedTime)+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked world :"+update.message.from_user.first_name)
    logger.info("World handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)
    
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
    return confirmed,deaths,recovered,deltaconfirmed,lastupdatedtime,deltarecovered,deltadeaths,active

def india(update, context):
    content = new_count_India()
    chat_id = update.message.chat_id
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=chat_id, text="Below are the stats for *India* :\
    \n\
    \nActive cases           : *"+content[7]+"*\
    \nConfirmed cases    : *"+content[0]+"* *(↑"+content[3]+")*\
    \nDeath cases          : *"+content[1]+"* *(↑"+content[6]+")*\
    \nRecovered cases    : *"+content[2]+"* *(↑"+content[5]+")*\
    \nThis data was last updated at : *"+content[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
    print("This User checked India: "+update.message.from_user.first_name)
    logger.info("India handler used ", update.message.chat.id, update.message.from_user.first_name)
    captureID(update)

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
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Below are the stats for *"+content_k[5]+"* \
        \n\
        \nActive cases           : *"+content_k[8]+"*\
        \nConfirmed cases    : *"+content_k[0]+"* *(↑"+content_k[3]+")*\
        \nDeath cases            : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered cases    : *"+content_k[2]+"* *(↑"+content_k[6]+")*\
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
    for each in jsonContent:
        if str(each["countryInfo"]["iso2"]) == str(var).upper():
            confirmed = str(each["cases"])
            deaths = str(each["deaths"]) 
            recovered = str(each["recovered"])
            populationHere = str(each["population"])
            lastupdatedtime = str(datetime.fromtimestamp((each["updated"])/1000).replace(microsecond=0))
            countryName = str(each["country"])
            new_case = str(each["todayCases"])
            new_deaths = str(each["todayDeaths"])
            casesPerOneMillion = str(each["casesPerOneMillion"])
            deathsPerOneMillion = str(each["deathsPerOneMillion"])
            activePerOneMillion = str(each["activePerOneMillion"])
            recoveredPerOneMillion = str(each["recoveredPerOneMillion"])
            testsPerOneMillion = str(each["testsPerOneMillion"])
    return confirmed,deaths,recovered,populationHere,lastupdatedtime,countryName,new_case,new_deaths,casesPerOneMillion,deathsPerOneMillion,activePerOneMillion,recoveredPerOneMillion,testsPerOneMillion

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
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The stats for country *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases    : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases            : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases    : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nCases per million    : *"+content_k[8]+"*\
        \nDeath per million    : *"+content_k[9]+"*\
        \nActive per million    : *"+content_k[10]+"*\
        \nRecovered per million : *"+content_k[11]+"*\
        \nTests per million    : *"+content_k[12]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
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
    Now for karnataka use <b>'/state KA'</b> without the single quotes\n \
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
    f.write("\nUser is %d\r" % (update.message.chat.id)+": "+(update.message.from_user.first_name))

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
    jsonContentUS = apiRequestUSA()
    contents = requests.get("https://locationiq.com/v1/reverse.php?key="+APIKey_LQ+"&lat="+current_lat+"&lon="+current_lon+"&format=json").json()
    countryName = contents["address"]["country"]
    country = contents["address"]["country_code"]
    
    if country == "in":
        india(update,context)
        state_district = contents["address"]["state_district"]
        try:
            state = contents["address"]["state"]
        except:
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
        \nThis data was last updated at : *"+lastupdatedtime+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        getLocation1(update,context,current_lat,current_lon,lastupdatedtime)
        #links(context,update,current_lat,current_lon)
    elif country == "us":
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are currently located in or the Map location shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        state = contents["address"]["state"]
        print(state)
        for each in jsonContentUS[0]:
            if str(each["name"]) == state:
                value = us_statewise_stats(str(each["state"]))
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+state+"*\
        \n\
        \nConfirmed Cases: *"+value[0]+"*\
        \nDeath Cases    : *"+value[1]+"*\
        \nRecovered Cases: *"+value[2]+"*\
        \nThis data was last updated at : *2020/"+value[3]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        getLocation2(update,context,current_lat,current_lon)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "de":
        #state = contents["address"]["state"]
        #print(state)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        getLocation3(update,context,current_lat,current_lon)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "jp":
        state_jp = contents["address"]["state"]
        prefecture = str((state_jp.replace("Prefecture","")).strip())
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases          : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        getLocationJP(update,context,prefecture)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "gb":
        regionUK = contents["address"]["state_district"]
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        getLocationUK(update,context,regionUK)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "nl":
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        #links(context,update,current_lat,current_lon)
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
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        
        print(stateRU)
        getLocationRU(update,context,stateRU)
        print("This User checked this"+ content_k[5] +":"+update.message.from_user.first_name)
        captureID(update)
    elif country == "au":
        stateAUS = str((contents["address"]["state"]).strip())
        print(stateAUS)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        getLocationAUS(update,context,stateAUS)
        print("This User checked this"+ content_k[5] +":"+update.message.from_user.first_name)
        captureID(update)
    elif country == "ca":
        provinceCA = str(contents["address"]["state"]).upper()
        print(provinceCA)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        #links(context,update,current_lat,current_lon)
        getLocationCA(update,context,provinceCA)
        print("This User checked Now"+ content_k[5] +":"+update.message.from_user.first_name)
        captureID(update)
    elif country == "es":
        provinceCA = str(contents["address"]["state"])
        print(provinceCA)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nTests per million    : *"+content_k[12]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        #links(context,update,current_lat,current_lon)
        getLocationES(update,context,provinceCA)
        print("This User checked Now"+ content_k[5] +":"+update.message.from_user.first_name)
        captureID(update)
    elif country == "br":
        state_br = contents["address"]["state"]
        print(state_br)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases          : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        getLocationBR(update,context,state_br)
        #links(context,update,current_lat,current_lon)
        captureID(update)
    elif country == "fr":#country = url['country_code']
        county = contents["address"]["county"]
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        #links(context,update,current_lat,current_lon)
        print(county)
        getLocationFR(update,context,county)
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
    elif country == "it" :#country = url['country_code']
        contentsBDC = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client?latitude="+current_lat+"&longitude="+current_lon+"&localityLanguage=en").json()
        stateIT = contentsBDC["principalSubdivision"]
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        #links(context,update,current_lat,current_lon)
        getLocationIT(update,context,stateIT)
        print("This User checked "+ content_k[5] +":"+update.message.from_user.first_name)
    else :#country = url['country_code']
        print(contents)
        content_k = countryWiseStatsCollect(country)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The location you shared is in *"+content_k[5]+"* \
        \n\
        \nConfirmed Cases : *"+content_k[0]+"* *(↑"+content_k[6]+")*\
        \nDeath Cases       : *"+content_k[1]+"* *(↑"+content_k[7]+")*\
        \nRecovered Cases   : *"+content_k[2]+"*\
        \nCurrent Population : *"+content_k[3]+"*\
        \nThis data was last updated at : *"+content_k[4]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
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
    print(contents)
    for each in contents['results']:
        stateName = str(each["state"])
        district = str(each["district"])
    dist = str((district.replace("District","")).strip())
    
    rd = requests.get('https://api.covid19india.org/state_district_wise.json')
    rdj = rd.json()
    state = rdj[stateName]
    dist = districtIN(dist)
    try:
        active = str(state["districtData"][dist]["active"])
        confirmed_d = str(state["districtData"][dist]["confirmed"])
        new_case = str(state["districtData"][dist]["delta"]["confirmed"])
        death = str(state["districtData"][dist]["deceased"])
        delta_death = str(state["districtData"][dist]["delta"]["deceased"])
        recovered = str(state["districtData"][dist]["recovered"])
        delta_recovered = str(state["districtData"][dist]["delta"]["recovered"])
        print(recovered)
        context.bot.send_message(chat_id=update.message.chat_id,text="The location you shared is in *"+dist+"*\
        \n\
        \nActive Cases        : *"+active+"*\
        \nConfirmed Cases : *"+confirmed_d+"* *(↑"+new_case+")*\
        \nDeath Cases          : *"+death+"* *(↑"+delta_death+")*\
        \nRecovered Cases : *"+recovered+"* *(↑"+delta_recovered+")*\
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
        content_k = us_statewise_stats(us_state_code)
        sN = getUS_stateName(us_state_code)
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        context.bot.send_message(chat_id=update.effective_chat.id, text="The stats for *"+sN+"* are:\
        \n\
        \nConfirmed Cases  : *"+content_k[0]+"*\
        \nDeath Cases       : *"+content_k[1]+"*\
        \nRecovered Cases  : *"+content_k[2]+"*\
        \nThis data was last updated at : *2020/"+content_k[3]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
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
            print("Awesome")
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

def healthCheck(update,context):
    df= pd.read_csv('api.csv')
    
    for url in df['urls']:
        response= requests.get(url)
        status= response.status_code
        if status != 200:
            context.bot.send_message(chat_id=update.effective_chat.id, text="API down for "+url,parse_mode=telegram.ParseMode.MARKDOWN)
        else :
            context.bot.send_message(chat_id=update.effective_chat.id, text="API is Up and running",parse_mode=telegram.ParseMode.MARKDOWN)
       
def main():
    
    BotToken = ""
    updater = Updater(BotToken,use_context=True)
    print (today)
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
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.location,getLocation))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()