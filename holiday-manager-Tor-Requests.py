import time
import datetime
import json
from bs4 import BeautifulSoup
import requests

"""
Setup:
    I got IP-banned from https://www.timeanddate.com/holidays/us so I have to use a Tor Proxy to access the website

    Commands to install libraries:

    pip install requests[socks]

    if on MacOS:
        pip install "requests[socks]"

    Install Tor Browser: https://tb-manual.torproject.org/installation/

    By default, Tor should use port 9050 for the localhost proxy. If errors occur, try changing to port 9150.

"""


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

    def get_year(self):
        return str(self.__date.year)

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
            print(f"\nSuccess:\n{holidayObj} has been added to the holiday list.\n")

        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday


    def findHoliday(self, HolidayName, Date):
        found_holiday = None
        for holiday in self.innerHolidays:
            if HolidayName.lower() == holiday.get_name().lower() and Date == holiday.get_date():
                found_holiday = holiday
        return found_holiday

        # Find Holiday in innerHolidays
        # Return Holiday


    def removeHoliday(self, HolidayName, Date):
        holiday = self.findHoliday(HolidayName, Date)
        self.innerHolidays.remove(holiday)
        print(f"\nSuccess:\n{HolidayName} has been removed from the holiday list.\n")
            
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
        print(f'\n{count} Holiday(s) loaded from file "{filelocation}"\n')
            
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
        
        proxy = {
            'http':  'socks5://localhost:9150',
            'https': 'socks5://localhost:9150',
        }

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
                date = date.replace('mey','may')
                date = date.replace('des','dec')
                date = date.replace('ä','a')
                date = date.replace('z','c')
                date = date.replace('yan','jan')
                date = date.replace('yun','jun')
                date = date.replace('yul','jul')
                date = date.replace('noy','nov')
                date = date.replace('sty','jan')
                date = date.replace('lut','feb')
                date = date.replace('cwy','apr')
                date = date.replace('maj','may')
                date = date.replace('cce','jun')   
                date = date.replace('lyp','jul')        
                date = date.replace('sye','aug')
                date = date.replace('wrc','sep')
                date = date.replace('pac','oct')    
                date = date.replace('lys','nov') 
                date = date.replace('gru','dec')         
                date = date.replace('Січ','jan')
                date = date.replace('Лют', 'feb')
                date = date.replace('Бер', 'mar')
                date = date.replace('Кві', 'apr')
                date = date.replace('Тра', 'may')
                date = date.replace('Чер', 'jun')
                date = date.replace('Лип', 'jul')
                date = date.replace('fév','feb')
                date = date.replace('avr', 'apr')
                date = date.replace('juyn','jun')
                date = date.replace('juyl','jul')
                date = date.replace('aoû', 'aug')
                date = date.replace('déc','dec')
                date = date.replace('mrt','mar')

                holiday_date = date+ f" {year}"
                try:
                    format = "%b %d %Y"
                    holiday_date = datetime.datetime.strptime(holiday_date, format).date()
                except:
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
                and x.get_year() == year, self.innerHolidays))
        
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

        # Get Weather from a Previous Day, up to 5 Days in the Past

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
            time_list = ['03:00:00','06:00:00','09:00:00','12:00:00','15:00:00','18:00:00','21:00:00','24:00:00']
            future_time_stamp = ""
            for i in range(len(time_list)):
                if str(timestamp) <= time_list[i]:
                    future_timestamp = time_list[i]
                    break

            if future_timestamp == '24:00:00':
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

        # Get Weather Forecast for Next 5 Days
        # Each Day has 8 Forecasts, One for every 3 hours, so select the next applicable forecast based on current time
        # Return list of weather descriptions and the list of their respective dates


    def getWeather(self):
        my_date = datetime.date.today()
        year, current_week, _ = my_date.isocalendar()
        year = str(year)
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

        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        # Query API for weather in that week range
        # Use the Datetime Module to look up current week and year
        # Get 5 previous weather forecasts and 5 future weather forecasts
        # Store forecasts in dictionary with key = Date and value = weather description
        # Find the holidays in the week and use the dictionary to get their weather
        # Use Try / Except to catch problems


    @staticmethod
    def Validate_Input(input_type, message, range_of_values = 1):
        valid_value = False
        while valid_value == False:
            if input_type == 'number':
                try:
                    user_input = input(message)
                    if user_input == '' and range_of_values == 52:
                        return user_input
                    user_input = int(user_input)
                    if user_input < 1 or user_input > range_of_values:
                        print('\nError: Invalid Input!\n')
                    else:
                        return user_input
                except ValueError:
                    print("\nError: Input must be numeric!\n")
                    continue

            elif input_type == 'string':
                user_input = input(message).lower()
                if user_input == 'y' or user_input == 'n':
                    return user_input
                else:
                    print()
                    print("Error: Invalid input.\n")

            else:
                try:
                    date_text = input(message)
                    date_text = datetime.datetime.strptime(date_text, '%Y-%m-%d').date()
                    return date_text
                except ValueError:
                    print("\nIncorrect Date Format, should be YYYY-MM-DD")
                    continue

        # Validates input based on input type
        # If input is invalid, keeps prompting the user until a valid input is received

    def View_Holidays(self, save_status):

        print("\nView Holidays\n=================")
        year_found = False
        while year_found == False:
            year = input('Which Year?: ')
            for i in range(len(self.innerHolidays)):
                if year == self.innerHolidays[i].get_year():
                    year_found = True
                    break
            if year_found == False:
                print('\nError: Year not found!\n')
        
        week = self.Validate_Input('number', 'Which week? #[1-52, Leave blank for the current week]: ', 52)
        print()
        if week == "":
            week = datetime.date.today().isocalendar()[1]
            
        if week == datetime.date.today().isocalendar()[1] and year == str(datetime.date.today().isocalendar()[0]):
            weather = self.Validate_Input('string', 'Would you like to see this week\'s weather? [y/n]: ', 52)
            print()
            if weather == 'y':
                self.getWeather()
            else:
                holiday_list = self.filter_holidays_by_week(year, week)
                self.displayHolidaysInWeek(holiday_list)
        else:
            holiday_list = self.filter_holidays_by_week(year, week)
            self.displayHolidaysInWeek(holiday_list)

        self.Main_Menu(save_status)       

        # Displays holidays based on user input data (Year and Week)
        # For current year and current week, prompt to show weather

    def User_Add_Holiday(self):

        print("\nAdd a Holiday\n=============")
        holiday_exists = 'yes'
        while holiday_exists is not None:
            holiday_name = input('Holiday: ')
            date = HolidayList.Validate_Input('date', 'Date (YYYY-MM-DD): ')
            print()
            holiday_exists = self.findHoliday(holiday_name, date)
            if holiday_exists is None:
                holiday_obj = Holiday(holiday_name, date)
                self.addHoliday(holiday_obj)
            else:
                print("Error: Holiday already in list!\n")

        self.Main_Menu()

        # Adds holidays based on user input (year string and holiday name)
        # Checks if holiday is already in holiday_list


    def User_Remove_Holiday(self):

        print("\nRemove a Holiday\n================")
        holiday_found = False
        holiday_removed = False

        while holiday_found == False:
            holiday_name = input('Holiday: ')
            for i in range(len(self.innerHolidays)):
                if holiday_name.lower() == self.innerHolidays[i].get_name().lower():
                    holiday_found = True
            if holiday_found == False:
                print(f"\nError:\nHoliday {holiday_name} not found!\n")
        
        while holiday_removed == False:
            date = HolidayList.Validate_Input('date', f'Date for {holiday_name} (YYYY-MM-DD): ')
            holiday = self.findHoliday(holiday_name, date)
            if holiday is None:
                print(f"\nError:\n{holiday_name} not found.\n")
            else:
                self.removeHoliday(holiday_name,date)
                holiday_removed = True

        self.Main_Menu()

        # Adds holidays based on user input (year string and holiday name)
        # Checks if holiday is in holiday_list before removing it


    def Main_Menu(self, save_status = 0):

        print()
        print("Participant Menu\n================")
        print("1. Add a Holiday\n2. Remove a Holiday\n3. Save Holiday List\n4. View Holidays\n5. Exit\n")
        menu_message = ("Select an option to continue: ")
        menu_selection = HolidayList.Validate_Input('number', menu_message, 5)
        print()

        if menu_selection == 1:
            self.User_Add_Holiday()

        elif menu_selection == 2:
            self.User_Remove_Holiday()

        elif menu_selection == 3:  # If user wishes to save changes
            print("\nSaving Holiday List\n====================")
            save = self.Validate_Input("string","Are you sure you want to save your changes? [y/n]: ")
            print()

            if save == 'y':
                filename = input('Enter a filename (you do not need a file extension): ')
                print()
                self.save_to_json(filename)
                print(f'\nSuccess:\nChanges saved to "{filename}.json"\n')
                save_status = 1

            self.Main_Menu(save_status)

        elif menu_selection == 4:

            self.View_Holidays(save_status)

        else:  # If player wishes to exit program
            print("\nExit\n=====")
            if save_status == 0:
                message = 'Are you sure you want to exit?\nYour changes will be lost.\n[y/n]: '
            else:
                message = 'Are you sure you want to exit? [y/n]: '

            choice = self.Validate_Input('string', message)

            if choice == 'y':
                print('\nGoodbye!\n')
            else:
                self.Main_Menu(save_status)
                
        # Main Menu displays menu options and prompts user for an int input
        # Once input is received, menu runs appropriate method and, if necessary, calls helper functions

def main():

    holiday_manager = HolidayList()
    holiday_manager.read_json('holidays.json')
    holiday_manager.scrapeHolidays()
    print("\nHoliday Management\n===================")
    print(f"There are {holiday_manager.numHolidays()} holidays stored in the system.\n")
    holiday_manager.Main_Menu()

    # Main method
    # Instantiates class holiday_manager and initializes empty holiday list
    # Seeds holiday_list with holidays from holidays.json file
    # Scrapes usholidays.com website for holidays in the year range 2020-2024
    # Prints number of preloaded holidays 
    # Calls Main_Menu() function


if __name__ == "__main__":
    main();

# Calls main method