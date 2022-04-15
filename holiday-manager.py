import datetime
from doctest import master
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


def Get_HTML(url): # Function makes a get request for a URL and returns a JSON Dict
    response = requests.get(url)
    return response

def Create_Holiday_List(URL, year):
        
    html = Get_HTML(URL)

    soup = BeautifulSoup(html.content,"lxml")

    previous_year_str = str(year - 1)
    next_year_str = str(year + 1)

    # Remove Previous and Next Year Tags
    # Try-except blocks throw AttributeError exception when soup.find returns a None type

    try:
        previous_year = soup.find('a', href="/holidays/us/" + previous_year_str)
        previous_year.decompose()
    except AttributeError:
        for previous_year in soup.find_all('a', href="/holidays/us/"):
            previous_year.decompose()

    try:
        next_year = soup.find('a', href="/holidays/us/" + next_year_str)
        next_year.decompose()
    except AttributeError:
        for next_year in soup.find_all('a', href="/holidays/us/"):
            next_year.decompose()


    for next_year in soup.find_all('a', href="/holidays/us/"):
        print(next_year, " chungus")
        next_year.decompose()

    # Remove Holidays with Tentative Dates
    for tentative_date in soup.select('a:-soup-contains("(Tentative Date)")'):
        tentative_date.decompose()

    # Remove You Might Like This/Might Also Like Section
    for extra in soup.find('h2',class_ = 'rel-posts__title'):
        extra.find_next().decompose()

    # Initialize list of Holidays and Dates
    holiday_list = list()
    date_list = list()

    # Find all US Holiday Names and Dates for Current Year
    # 11:17AM string is a placeholder to get the Datetime function to work
    for holiday in soup.select('a[href*="/holidays/us/"]'):
        date = holiday.find_previous().find_previous().find_previous()
        date = date.getText() + f" {year}" + ' 11:17AM'
        format = '%b %d %Y %I:%M%p'
        date = str(datetime.datetime.strptime(date, format).date())
        date_list.append(date)
        holiday_list.append(holiday.text)

    # Create Holiday Dictionary for Year
    all_holiday_list = list()
    for i in range(len(holiday_list)):
        one_holiday = {"name": holiday_list[i],"date":date_list[i]} 
        all_holiday_list.append(one_holiday)

    return all_holiday_list

# Sample JSON
with open('holidays.json') as f:
    sample_holidays = json.load(f)
    f.close()

sample_holiday_list = list(sample_holidays['holidays'])

# 2020 Holidays
URL = "https://www.timeanddate.com/holidays/us/2020"
holiday_list_2020 = Create_Holiday_List(URL, 2020)

# 2021 Holidays
URL = "https://www.timeanddate.com/holidays/us/2021"
holiday_list_2021 = Create_Holiday_List(URL, 2021)

# 2022 Holidays
URL = "https://www.timeanddate.com/holidays/us/2022"
holiday_list_2022 = Create_Holiday_List(URL, 2022)

# 2023 Holidays
URL = "https://www.timeanddate.com/holidays/us/2023"
holiday_list_2023 = Create_Holiday_List(URL, 2023)

# 2024 Holidays
URL = "https://www.timeanddate.com/holidays/us/2024"
holiday_list_2024 = Create_Holiday_List(URL, 2024)


# Combine various Year Lists into Master Holiday List
# Append Sample JSON List of Dictionaries to Master List
master_holiday_list = holiday_list_2020 + holiday_list_2021 + holiday_list_2022 + holiday_list_2023 + holiday_list_2024
for i in range(len(sample_holiday_list)):
    master_holiday_list.append(sample_holiday_list[i])

# Sort the Master Holiday List by Date before using Sorted() with lambda function
# Function sorts by Date and then Alphabetical Order by Name (for Holidays that have the same Date)
master_holiday_list = sorted(master_holiday_list, key = lambda x: (x['date'], x['name']))
holiday_dict = {'holidays': master_holiday_list}

# Dump Dictionary to Json and Write to File
updated_holiday_json = json.dumps(holiday_dict, indent=3, separators=(',', ': '))
with open("holidays_(2020-2024).json", "w") as outfile:
    outfile.write(updated_holiday_json)
    outfile.close()




# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------

class Holiday:

    def __init__(self,holiday_name,date):
        self.__holiday_name = holiday_name
        if not isinstance(date, datetime.date):
            raise TypeError("Date must be a Datetime object!")
        else:
            self.__date = date


    def __str__ (self):
        return f'{self.__holiday_name}, {self.__date}'
        # String output
        # Holiday output when printed.




# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
# class HolidayList:
#    def __init__(self):
#        self.innerHolidays = []
   
#     def addHoliday(holidayObj):
#         # Make sure holidayObj is an Holiday Object by checking the type
#         # Use innerHolidays.append(holidayObj) to add holiday
#         # print to the user that you added a holiday

#     def findHoliday(HolidayName, Date):
#         # Find Holiday in innerHolidays
#         # Return Holiday

#     def removeHoliday(HolidayName, Date):
#         # Find Holiday in innerHolidays by searching the name and date combination.
#         # remove the Holiday from innerHolidays
#         # inform user you deleted the holiday

#     def read_json(filelocation):
#         # Read in things from json file location
#         # Use addHoliday function to add holidays to inner list.

#     def save_to_json(filelocation):
#         # Write out json file to selected file.
        
#     def scrapeHolidays():
#         # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
#         # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
#         # Check to see if name and date of holiday is in innerHolidays array
#         # Add non-duplicates to innerHolidays
#         # Handle any exceptions.     

#     def numHolidays():
#         # Return the total number of holidays in innerHolidays
    
#     def filter_holidays_by_week(year, week_number):
#         # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
#         # Week number is part of the the Datetime object
#         # Cast filter results as list
#         # return your holidays

#     def displayHolidaysInWeek(holidayList):
#         # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
#         # Output formated holidays in the week. 
#         # * Remember to use the holiday __str__ method.

#     def getWeather(weekNum):
#         # Convert weekNum to range between two days
#         # Use Try / Except to catch problems
#         # Query API for weather in that week range
#         # Format weather information and return weather string.

#     def viewCurrentWeek():
#         # Use the Datetime Module to look up current week and year
#         # Use your filter_holidays_by_week function to get the list of holidays 
#         # for the current week/year
#         # Use your displayHolidaysInWeek function to display the holidays in the week
#         # Ask user if they want to get the weather
#         # If yes, use your getWeather function and display results



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