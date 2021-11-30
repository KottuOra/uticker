#!/usr/bin/env python
import logging 
import requests
import config 
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

TAB = "   "

def get_trends():
    resultset = {}

    try:
        for location in config.trends["locations"] :
            url = config.trends["apiurl"] + "?id=" + str(location); 
            payload = {}
            headers = {'Authorization': 'Bearer '+ config.trends["token"]}
            response = requests.request("GET", url, headers=headers, data=payload)
            if (response.status_code == 200):
                data = response.json()[0]
                location = data["locations"][0]['name']
                trends = data['trends']
                line = ""
                for i in range(0,min(len(trends),config.trends["items"])):
                    line += trends[i]['name'] + TAB
                    logging.debug("Trend: %s", trends[i])
                key = "{trends " + location +"}"
                resultset[key] = lcdfriendlytext(line)
    except Exception as e:
        logging.error("Error getting trends content :" + str(e))
        resultset = {"{trends}":"!Couldn't load content, please check your config."}

    logging.info("Resultset: {0}".format(resultset))
    return resultset

def get_weather():
    resultset = {}

    try:
        url = config.weather["apiurl"]
        params = {"q":config.weather["city"],"units":config.weather["units"],"APPID":config.weather["appid"] }
        headers = {}
        response = requests.request("GET", url, headers=headers, params=params)
        if (response.status_code == 200):
            data = response.json()
            line = data['weather'][0]['main'] + " "
            if (config.weather["show_highlow"]):
                line += "high:" + str (data['main']['temp_max'] )+ " "
                line += "low:" + str(data['main']['temp_min'] )+ " "
            if (config.weather["show_humidity"]):
                line += "hum:" +  str(data['main']['humidity']) + "% "
            if (config.weather["show_wind"]):
                line += "wind speed:" +  str(data['wind']['speed']) + " "
            if (config.weather["show_pressure"]):
                line += "pressure:" +  str(data['main']['pressure']) + " bar "

            key = "{weather " + data['name'] + "}"
            resultset[key] = line
    except Exception as e:
        logging.error("Error getting weather content :" + str(e))
        resultset = {"{weather}":"!Couldn't load content, please check your config."}

    logging.info("Resultset: {0}".format(resultset))
    return resultset


def get_exchange():
    resultset = {}
    line =""
    try:
        url = config.exchange["apiurl"]; 
        payload = {}
        headers = {
        'x-rapidapi-host': config.exchange["x-rapidapi-host"] ,
        'x-rapidapi-key': config.exchange["x-rapidapi-key"] 
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if (response.status_code == 200):
            data = response.json()
            line = ""
            for currency in config.exchange["currencies"]:
                if (data['rates'][currency]['value'] >= 1000):
                    line +=  "{:,.0f}".format( data['rates'][currency]['value'] )+ " " + currency + " : "  
                else:
                    line +=  "{:,.2f}".format( data['rates'][currency]['value'] )+ " " + currency + " : "  

        key = "{exchange rates}"
        resultset[key] = line

    except Exception as e:
        logging.error("Error getting exchange rate :" + str(e))
        resultset = {"{exchange}":"!Couldn't load content, please check your config."}

    logging.info("Resultset: {0}".format(resultset))
    return resultset

def get_news():
    resultset = {}

    try:
        url = config.news["apiurl"]
        params = {"country":config.news["country"],"apikey":config.news["apikey"] }
        
        response = requests.request("GET", url, params=params)
        if (response.status_code == 200):
            data = response.json()
            articles = data['articles']
            line = ""
            for i in range(0,min(len(articles),config.news["items"])):
                line += "["+ articles[i]['source']['name'] +"] " +articles[i]['title'] + " "
            key = "{news}"
            resultset[key] = line
    except Exception as e:
        logging.error("Error getting trends content :" + str(e))
        resultset = {"{news}":"!Couldn't load content, please check your config."}

    logging.info("Resultset: {0}".format(resultset))
    return resultset

def lcdfriendlytext(original):
    ltext = ''
    for c in original:
        r = c
        #sorry match statements are not compatible 
        if(ord(c) == 305):
            r = "i"
        elif (ord(c) == 304):
            r = "I"
        elif (ord(c) == 231):
            r = "c"
        elif (ord(c) == 199):
            r = "C"
        elif (ord(c) == 287):
            r = "g"
        elif (ord(c) == 286):
            r = "G"
        elif (ord(c) == 351):
            r = "s"
        elif (ord(c) == 350):
            r = "S"
        elif (ord(c) == 246):
            r = "o"
        elif (ord(c) == 214):
            r = "O"
        elif (ord(c) == 252):
            r = "u"
        elif (ord(c) == 220):
            r = "U"
        ltext += r

    return ltext

def main():
    logging.debug("Starting the TickerSources")
    #results = get_trends()
    #get_weather()
    #get_exchange()
    #get_news()
    otext = "ıİçÇğĞşŞöÖüÜ"
    ltext = lcdfriendlytext(otext)
    logging.debug ("original  text:%s" , otext)
    logging.debug ("converted text:%s" , ltext)
if __name__ == "__main__":
    main()
