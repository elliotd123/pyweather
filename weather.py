#!/usr/bin/python3
import http.client
import sys
import simplejson as json
import datetime

class weather:
  def __init__(self,city="Cedar Rapids",appid=""):
    self.city = city
    self.current = json.loads("{}")
    self.five_day = json.loads("{}")
    self.sixteen_day = json.loads("{}")
    self.appid = appid
  
  def update(self):
    conn = http.client.HTTPConnection("api.openweathermap.org")
    headers = {
        'cache-control': "no-cache"
        }
    
    
    #Get current weather
    conn.request("GET", "/data/2.5/weather?q=" + self.city.replace(" ","%20") + "&units=imperial&APPID=" + self.appid, headers=headers)
    res = conn.getresponse()
    data = res.read()
    self.current = json.loads(data)

    #Get 5-day forecast
    conn.request("GET", "/data/2.5/forecast?q=" + self.city.replace(" ","%20") + "&units=imperial&APPID=" + self.appid, headers=headers)
    res = conn.getresponse()
    data = res.read()
    self.five_day = json.loads(data)

    #Get 16-day forecast
    conn.request("GET", "/data/2.5/forecast/daily?q=" + self.city.replace(" ","%20") + "&units=imperial&APPID=" + self.appid, headers=headers)
    res = conn.getresponse()
    data = res.read()
    self.sixteen_day = json.loads(data)


def show_summary(w):
    result = ""
    result += "Name:\t\t" + w.current['name']
    result += "\nTemp:\t\t" + str(w.current['main']['temp']) + "F"
    result += "\nPressure:\t" + str(w.current['main']['pressure']) + " hPa"
    result += "\nHumidity:\t" + str(w.current['main']['humidity']) + "%"

    result += "\n"

    result += "\nShort term Forecast:"
    for i in range(0,5):
      day = i + 1
      result += "\n\t" + str(datetime.datetime.utcfromtimestamp(w.five_day['list'][i]['dt']))
      high = w.five_day['list'][i]['main']['temp_max']
      low = w.five_day['list'][i]['main']['temp_min']
      condition = w.five_day['list'][i]['weather'][0]['description']
      result += "\n\t\tHigh: " + str(high)
      result += "\n\t\tLow : " + str(low)
      result += "\n\t\tDesc: " + str(condition)
      result += "\n"

    result += "\nLong term Forecast:"
    for i in range(1,6):
      day = i + 1
      result += "\n\t" + str(datetime.datetime.utcfromtimestamp(w.sixteen_day['list'][i]['dt']))
      high = w.sixteen_day['list'][i]['temp']['max']
      low = w.sixteen_day['list'][i]['temp']['min']
      condition = w.sixteen_day['list'][i]['weather'][0]['description']
      result += "\n\t\tHigh: " + str(high)
      result += "\n\t\tLow : " + str(low)
      result += "\n\t\tDesc: " + str(condition)
      result += "\n"

    print(result)

if __name__ == "__main__":
  settings = open('settings.json','r')
  settings_js = json.loads(settings.read())
  settings.close()
  city = settings_js.get('default_city',None)
  appid = settings_js.get('appid',None)
  if not city:
    city = "Cedar Rapids"
  if not appid or appid == "":
    print("Please set appid in settings.json file.")
    sys.exit(1)

  w = weather(city=city,appid=appid)
  if (len(sys.argv) >= 2):
    w.city = sys.argv[1]
  
  w.update()
  show_summary(w)
