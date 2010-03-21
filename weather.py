import simplejson as json
import urllib2 as ul
from datetime import datetime as dt
from datetime import timedelta as td
import sqlite3
 
forecast = "http://metservice.com/publicData/localForecastAuckland"
current  = "http://metservice.com/publicData/oneMinObs93110"
currentLarge = "http://metservice.com/publicData/localObs93110"
 
def getData(url):
    return json.loads(ul.urlopen(url).read())
 
 
def logCurrentConditions(c):
    currentConditions = getData(current)
    currentConditionsLarge = getData(currentLarge)["threeHour"]
    currentDT = dt.strptime(currentConditions["time"], "%I:%M%p %d %B %Y") + td(minutes = 1) # Adding the minute due to Metservice being one day behind
    currentDTF = currentDT.strftime("%Y-%m-%d %H:%M") # formats the datetime to yyyy-mm-dd hh:mm e.g. 2010-03-14 23:11
    c.execute('INSERT INTO observation (clothingLayers, humidity, pressure, rainfall, temperature, time, windChill, windDirection, windGustSpeed, windSpeed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (currentConditionsLarge["clothingLayers"],
              currentConditionsLarge["humidity"],
              currentConditionsLarge["pressure"],
              currentConditionsLarge["rainfall"],
              currentConditions["temperature"],
              currentDTF,
              currentConditions["windChill"],
              currentConditions["windDirection"],
              currentConditions["windGustSpeed"],
              currentConditions["windSpeed"]))
    
    return currentDT, currentDTF
 

def logForecasts(c, currentDT, currentDTF):
    days = getData(forecast)["days"]
    
    for (counter, day) in enumerate(days):
        forecastDate = currentDT + td(days = counter)
        forecastDate = forecastDate.strftime("%Y-%m-%d %H:%M")
        desc = day["forecast"]
        shortDesc = day["forecastWord"]

        # Grabbing the id of the description pair that is going to be applied to a forecast
        descriptionID = c.execute('SELECT id from description WHERE description = ? AND shortDescription = ?', (desc, shortDesc))
        descriptionID = descriptionID.fetchone()

        # If given pair does not already exist, insert it and grab its ID
        if descriptionID is None:
            c.execute('INSERT INTO description (description, shortDescription) VALUES (?, ?)', (desc, shortDesc))
            descriptionID = c.execute('SELECT id from description WHERE description = ? AND shortDescription = ?',
                                      (desc, shortDesc))
            descriptionID = descriptionID.fetchone()

        c.execute('INSERT INTO forecast (currentDate, forecastDate, descriptionID, maxTemperature, minTemperature) VALUES (?, ?, ?, ?, ?)',
                  (currentDTF,
                  forecastDate,
                  descriptionID[0],
                  day["max"],
                  day["min"]))  


conn = sqlite3.connect('weather.db')
c = conn.cursor()    
currentDT, currentDTF = logCurrentConditions(c)
logForecasts(c, currentDT, currentDTF)
conn.commit()
conn.close()
