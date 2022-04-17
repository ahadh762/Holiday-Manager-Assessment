import time
import datetime
import json
from bs4 import BeautifulSoup
import requests

"""
Setup:
    pip install requests[socks]
    if on MacOS:
        pip install "requests[socks]"
    These should be already installed
"""

proxy = {
    'http':  'socks5://localhost:9050',
    'https': 'socks5://localhost:9050',
}



class Holiday:
    def __init__(self,holiday_name,date):
        self.__holiday_name = holiday_name

        if not isinstance(date, datetime.date):
            raise TypeError("Date must be a Datetime object!")
        else:
            self.__date = date

    def get_name(self):
        return self.__holiday_name

    def get_date(self):
        return self.__date

    def __str__ (self):
        return f'{self.__holiday_name} ({self.__date})'
        # String output
        # Holiday output when printed.



class HolidayList:

    def __init__(self):
        self.innerHolidays = []

    def addHoliday(self, holidayObj):
        if not isinstance(holidayObj, Holiday):
            raise TypeError("\nHoliday must be a Holiday Object!\n")
        else:
            self.innerHolidays.append(holidayObj)
            print(f"Success:\n{holidayObj} has been added to the holiday list.\n")
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def findHoliday(self, HolidayName, Date):
        found_holiday = None
        for holiday in self.innerHolidays:
            if HolidayName == holiday.get_name() and Date == holiday.get_date():
                found_holiday = holiday
        return found_holiday

        # Find Holiday in innerHolidays
        # Return Holiday


    def removeHoliday(self, HolidayName, Date):
        holiday = self.findHoliday(HolidayName, Date)
        if holiday is None:
            print(f"Error:\n{HolidayName} not found.\n")
        else:
            self.innerHolidays.remove(holiday)
            print(f"Success:\n{HolidayName} has been removed from the holiday list.\n")
            
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday


    def read_json(self, filelocation):
        count = 0
        with open(filelocation) as f:
            holidays_dict = json.load(f)
            for i in range(len(holidays_dict['holidays'])):
                holiday_name = holidays_dict['holidays'][i]['name']
                holiday_date = holidays_dict['holidays'][i]['date']
                holiday_date = datetime.date.fromisoformat(holiday_date)
                holiday = Holiday(holiday_name, holiday_date)
                self.addHoliday(holiday)
                count += 1
            f.close()
        print(f'{count} Holiday(s) loaded from file "{filelocation}"\n')
            
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
    

    def save_to_json(self, filelocation):
        master_holiday_list = []
        holiday_dict = {}
        for i in range(len(self.innerHolidays)):
            holiday_name = self.innerHolidays[i].get_name()
            holiday_date = str(self.innerHolidays[i].get_date())
            one_holiday = {"name": holiday_name,"date": holiday_date}
            master_holiday_list.append(one_holiday)

        master_holiday_list = sorted(master_holiday_list, key = lambda x: (x['date'], x['name']))

        holiday_dict = {'holidays': master_holiday_list}
        updated_holiday_json = json.dumps(holiday_dict, indent=3, separators=(',', ': '))
        
        with open(f"{filelocation}.json", "w") as outfile:
            outfile.write(updated_holiday_json)
            outfile.close()

         # Write out json file to selected file.

    def Scraped_Holiday_List(self, URL, year):
            
        try:
            html = requests.get(URL, proxies = proxy)
            html.raise_for_status()
            html = html.text
        except requests.exceptions.HTTPError as err:
            print(err)

        soup = BeautifulSoup(html,"html.parser")

        # Remove Holidays with Tentative Dates
        for tentative_date in soup.select('a:-soup-contains("(Tentative Date)")'):
            tentative_date.decompose()

        # Find Table with Data
        table = soup.find('article',attrs = {'class':'table-data'})
        for row in table.find_all_next('tbody'): 
            # Find any tag that contains href /holidays/us/
            holidays = row.select('a[href *= "/holidays/us/"]')
            for holiday in holidays:
                holiday_name = holiday.text

                # Date is contained in text in the tag that is 3 tags prior to the href tag
                date = holiday.find_previous().find_previous().find_previous()
                # Fix encoding errors (consequence of using Tor Browser)
                date = date.getText().replace('.','')
                date = date.replace('i','y')
                date = date.replace('k','c')
                date = date.replace('des','dec')
                date = date.replace('ä','a')
                date = date.replace('z','c')
                holiday_date = date + f" {year}"
                format = '%d %b %Y'
                holiday_date = datetime.datetime.strptime(holiday_date, format).date()

                # Add Non-Duplicates to Inner List
                find_holiday = self.findHoliday(holiday_name, holiday_date)

                if find_holiday is None:
                    # Instantiate Holiday Objects and Add them to List of Objects
                    holidayObj = Holiday(holiday_name, holiday_date)
                    self.innerHolidays.append(holidayObj)


    def scrapeHolidays(self):

        # Add 2020 Holidays
        URL = "https://www.timeanddate.com/holidays/us/2020"
        self.Scraped_Holiday_List(URL, 2020)

        # Add 2021 Holidays
        URL = "https://www.timeanddate.com/holidays/us/2021"
        self.Scraped_Holiday_List(URL, 2021)

        # Add 2022 Holidays
        URL = "https://www.timeanddate.com/holidays/us/2022"
        self.Scraped_Holiday_List(URL, 2022)

        # Add 2023 Holidays
        URL = "https://www.timeanddate.com/holidays/us/2023"
        self.Scraped_Holiday_List(URL, 2023)

        # Add 2024 Holidays
        URL = "https://www.timeanddate.com/holidays/us/2024"
        self.Scraped_Holiday_List(URL, 2024)


        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.
        
    def numHolidays(self):
        return len(self.innerHolidays)
        # Return the total number of holidays in innerHolidays

    def filter_holidays_by_week(self, year, week_number):
        holidays = list(filter(lambda x: x.get_date().isocalendar()[1] == week_number \
                and x.get_date().isocalendar()[0] == year, self.innerHolidays))
        
        return holidays
        
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays


    @staticmethod
    def displayHolidaysInWeek(holiday_list):
        for i in range(len(holiday_list)):
            print(holiday_list[i])
        print()
            
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.


    @staticmethod
    def Get_Previous_Weather_Data(days_ago):

        url = "https://community-open-weather-map.p.rapidapi.com/onecall/timemachine"

        today = datetime.datetime.today()
        days_past = datetime.timedelta(days = days_ago)
        date = today - days_past
        
        timestamp = int(date.timestamp())

        querystring = {"lat":"26.6406","lon":"-81.8723","dt":timestamp}

        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "a2ba6e432emshba867077d11af9ap1a0278jsnc4e59674ffb8"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring).json()

            unix_timestamp = int(response['current']['dt'])

        except KeyError:
            raise KeyError("Limit the Number of API Calls you make! Wait at least 30 seconds and try again.")
        
        day = datetime.datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d')
        weather = response["current"]['weather'][0]['description']
        
        return day, weather



    @staticmethod
    def Get_Forecasted_Weather_Data():
        try:
            url = "https://community-open-weather-map.p.rapidapi.com/forecast/"

            querystring = {"q":"Fort Myers,us",}

            headers = {
                "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
                "X-RapidAPI-Key": "a2ba6e432emshba867077d11af9ap1a0278jsnc4e59674ffb8"
            }

            response = requests.get(url, headers=headers, params=querystring).json()

            timestamp = time.strftime('%H:%M:%S')
            time_list = ['24:00:00','03:00:00','06:00:00','09:00:00','12:00:00','15:00:00','18:00:00','21:00:00']
            future_time_stamp = ""
            for i in range(len(time_list)):
                if str(timestamp) <= time_list[i]:
                    future_timestamp = time_list[i]
                elif future_timestamp == '24:00:00':
                    future_time_stamp = '00:00:00'

            weather_list = []
            date_list = []

            for i in range(len(response['list'])):
                if future_time_stamp in response['list'][i]['dt_txt']:
                    date = response['list'][i]['dt_txt']
                    date = date.replace(f' {future_time_stamp}', '')
                    date_list.append(date)
                    weather = response['list'][i]['weather'][0]['description']
                    weather_list.append(weather)

        except KeyError as err:

            raise err

        return weather_list, date_list


    def getWeather(self):
        my_date = datetime.date.today()
        year, current_week, _ = my_date.isocalendar()
        holidays = self.filter_holidays_by_week(year, current_week)      

        previous_days = 5
        previous_days_list = []
        previous_weather_list = []
        while previous_days >= 0:
            day, weather = HolidayList.Get_Previous_Weather_Data(previous_days)
            previous_days_list.append(day)
            previous_weather_list.append(weather)
            previous_days -= 1

        forecasted_weather_list, forecasted_days_list = HolidayList.Get_Forecasted_Weather_Data()
        days_list = previous_days_list + forecasted_days_list
        weather_list = previous_weather_list + forecasted_weather_list
        weather_dict = {}
        for i in range(len(weather_list)):
            weather_dict[days_list[i]] = weather_list[i]
        
        for i in range(len(holidays)):
            holiday_date = str(holidays[i].get_date())
            if holiday_date in weather_dict:
                print(f"{holidays[i]} - {weather_dict[holiday_date]}")
            else:
                print(f"{holidays[i]} - Weather Data not found")
        print()

        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

        
test = HolidayList()
test.read_json('holidays.json')
test.scrapeHolidays()
test.save_to_json('sample')
num = test.numHolidays()
print(num)
holidays = test.filter_holidays_by_week(2022,15)
HolidayList.displayHolidaysInWeek(holidays)
test.getWeather()



# def main():
#     # Large Pseudo Code steps
#     # -------------------------------------
#     # 1. Initialize HolidayList Object
#     # 2. Load JSON file via HolidayList read_json function
#     # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
#     # 3. Create while loop for user to keep adding or working with the Calender
#     # 4. Display User Menu (Print the menu)
#     # 5. Take user input for their action based on Menu and check the user input for errors
#     # 6. Run appropriate method from the HolidayList object depending on what the user input is
#     # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


# if __name__ == "__main__":
#     main();


# # Additional Hints:
# # ---------------------------------------------
# # You may need additional helper functions both in and out of the classes, add functions as you need to.
# #
# # No one function should be more then 50 lines of code, if you need more then 50 lines of code
# # excluding comments, break the function into multiple functions.
# #
# # You can store your raw menu text, and other blocks of texts as raw text files 
# # and use placeholder values with the format option.
# # Example:
# # In the file test.txt is "My name is {fname}, I'm {age}"
# # Then you later can read the file into a string "filetxt"
# # and substitute the placeholders 
# # for example: filetxt.format(fname = "John", age = 36)
# # This will make your code far more readable, by seperating text from code.