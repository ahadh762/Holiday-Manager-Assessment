# Holiday-Manager-Assessment

* This repository is for the Holiday Manager Assessment, coded using Python by Ahad Hussain. <br />

* The holiday manager is preloaded with 1498 holidays (including 7 from the holidays.json file) <br />

* The script allows users to add holidays, remove holidays, and list holidays based on year and week of the year. <br />

* For holidays in the current week of the current year, users can call [Open Weather Map API](https://rapidapi.com/community/api/open-weather-map/) 
 to retrieve information on the weather conditions for each of the holidays in the current week


## Files

* [holiday-manager.py - USE THIS FILE](https://github.com/ahadh762/Holiday-Manager-Assessment/blob/master/holiday-manager.py):
    * Contains Python script 

* [holiday-manager-Torr-Requests.py](https://github.com/ahadh762/Holiday-Manager-Assessment/blob/master/holiday-manager-Tor-Requests.py)
    * Because I was IP banned for webscraping [US Holidays 2022](https://www.timeanddate.com/holidays), I used HTTP proxies to make HTTP requests through the [Tor Browser](https://www.torproject.org)
    * Though it is not recommended for use, I included it just to show what I used to get the project up and running

* [holidays.json](https://github.com/ahadh762/Holiday-Manager-Assessment/blob/master/holidays.json):
    * JSON file containing initial list of holidays used to seed application
   
* [preloaded-holidays.json](https://github.com/ahadh762/Holiday-Manager-Assessment/blob/master/preloaded_holidays.json)
  * JSON file containing holidays from [holidays.json](https://github.com/ahadh762/Holiday-Manager-Assessment/blob/master/holidays.json) as well as those scraped from [US Holidays 2022](https://www.timeanddate.com/holidays/us/2020) over a range of 5 years (2020-2024)

* [Previous-Weather Sample.json](https://github.com/ahadh762/Holiday-Manager-Assessment/blob/master/Weather%20Samples/Previous-weather%20Sample.json)
  * JSON file containing sample output from querying [Open Weather Map API](https://rapidapi.com/community/api/open-weather-map/) for a previous day
  * The 'current' timestamp is a Unix timestamp and corresponds to Tue Apr 12 2022 15:00:00 GMT-0400 (EDT)
 
* [forecast_weather_sample.json](https://github.com/ahadh762/Holiday-Manager-Assessment/blob/master/Weather%20Samples/forecast_weather_sample.json)
  * JSON file containing sample output for [Open Weather Map API](https://rapidapi.com/community/api/open-weather-map/) Query for a forecast of the next 5 days
  * File contains forecasts for every 3 hours starting from "2022-04-18 00:00:00"


   
