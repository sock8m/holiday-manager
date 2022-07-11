# all packages
import json
from dataclasses import dataclass, field
from os import remove
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
from datetime import timedelta

currentYear = 2022
city = "New York City, USA"
weatherAPIKey = "55e9611df7msh8d9a1794a95dd96p1ff35bjsn79b2ab7fe896"
starterjsonfileloc = 'holidays.json'
newfilelocation = "test_holiday.json"

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
      
    def __init__(self,name,date):
        #Your Code Here
        self.name = name
        if not isinstance(date, datetime):
            raise TypeError("date must be set to an datetime")
        self.date = date        
    
    def __str__(self):
        # String output
        # Holiday output when printed. Holiday Name (Date)
        outputstr = (f"{self.name} ({self.date.strftime('%Y-%m-%d')})")
        return outputstr

    def dictionaryOut(self):
        # to turn this element into a dictionary, date needs to be formatted as a string
        dictOut = {}
        dictOut['name'] = self.name
        dictOut['date'] = self.date.strftime('%Y-%m-%d')
        return dictOut
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
        self.innerHolidays = []

    def __repr__(self):
        returnList = list(map(lambda b: b.__str__(), self.innerHolidays))
        returnStr = "\n".join(returnList)
        return returnStr

    def __str__(self):
        returnList = list(map(lambda b: b.__str__(), self.innerHolidays))
        returnStr = "\n".join(returnList)
        return returnStr
   
    def addHoliday(self,holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if not isinstance(holidayObj, Holiday):
            raise TypeError("entry must be a Holiday type object")
        # Use innerHolidays.append(holidayObj) to add holiday
        self.innerHolidays.append(holidayObj)
        # print to the user that you added a holiday, would do this but the output would be really crowded...
        # print(f"{holidayObj.__str__()} has been added to the list!")
    
    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        if HolidayName == None and Date == None:
            results = "not found! no search terms defined!"
        elif Date == None:
            results = list(filter(lambda a: (a.name == HolidayName), self.innerHolidays))
            # print(f"Searching for holidays with name {HolidayName}: {len(results)} results")
        elif HolidayName == None:
            if not isinstance(Date, datetime):
                raise TypeError("date must be set to an datetime")
            results = list(filter(lambda a: (a.date == Date), self.innerHolidays))
            # print(f"Searching for holidays with date {Date}: {len(results)} results")
        else:
            if not isinstance(Date, datetime):
                raise TypeError("date must be set to an datetime")
            results = list(filter(lambda a: (a.name == HolidayName) and (a.date == Date), self.innerHolidays))
            # print(f"Searching for holidays with date {Date} and name {HolidayName}: {len(results)} results")
        # Return Holiday
        return results

    def removeHoliday(self, HolidayName, Date):
        if not isinstance(Date, datetime):
            raise TypeError("date must be set to an datetime")
        # Find Holiday in innerHolidays by searching the name and date combination.
        search = self.findHoliday(HolidayName, Date)
        holidayObject = Holiday(HolidayName,Date)
        if len(search) == 0: print(f"this holiday was not found on {Date}, please try again")
        else:
            print(f"{search[0].__str__()} has been removed from the list!")
        # remove the Holiday from innerHolidays
            self.innerHolidays = list(filter(lambda a: (a.name != HolidayName or a.date != Date), self.innerHolidays))
        # inform user you deleted the holiday
            # print("this holiday has been removed")
    
    def read_json(self,filelocation):
        # Read in things from json file location
        with open(filelocation) as file:
            holidaysJSON = json.load(file)['holidays']
        for i in range(0, len(holidaysJSON)):
            datetimeJSON= datetime.strptime(holidaysJSON[i]['date'], '%Y-%m-%d')
            singleHoliday = Holiday(holidaysJSON[i]['name'], datetimeJSON)
        # Use addHoliday function to add holidays to inner list.
            self.addHoliday(singleHoliday)

    def save_to_json(self,filelocation):
        # Write out json file to selected file.
        listHolidayDictionaries = list(map(lambda b: b.dictionaryOut(), self.innerHolidays))
        fullOutputDictionary = {'holidays': listHolidayDictionaries}
        JSONFormatting = json.dumps(fullOutputDictionary, indent=2)
        with open(filelocation, "w") as file:
            file.write(JSONFormatting)

    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. 
        # You can scrape multiple years by adding year to the timeanddate URL. 
        # For example https://www.timeanddate.com/holidays/us/2022
        global currentYear
        for year in range(currentYear-2,currentYear+3):
            url = "https://www.timeanddate.com/holidays/us/{}?hol=33554809".format(year)
            response = requests.get(url).text
            soup = BeautifulSoup(response,'html.parser')

            # isolate just the holiday table body
            holidayTable = soup.find('table',attrs={'id':'holidays-table'}).find('tbody')

            # get a list of all the specific holidays, taking out the first one because it is not a holiday lol
            perHoliday = holidayTable.find_all('tr', attrs={'class':'showrow'})
            count = 0 # to make sure all the holidays have been counted

            # going through all the holidays and getting the info
            for i in range(0,len(perHoliday)):
                # getting the date, converting to datetime using strings
                dateRaw = perHoliday[i].find('th', attrs={'class':'nw'}).text
                dateString = (f"{dateRaw} {year}")
                dateObject = datetime.strptime(dateString, "%b %d %Y")
                # getting the name
                name = perHoliday[i].find('a').text
                # search to see if it's already in the list
                # Check to see if name and date of holiday is in innerHolidays array
                search = self.findHoliday(name, dateObject)
                # Add non-duplicates to innerHolidays
                if len(search) == 0: 
                    self.addHoliday(Holiday(name, dateObject))
                    count += 1
                else:
                    # print(f"{name} on {dateString} is already in the list!")
                    pass
        
        # print(f"{count} holidays have been added for the year {year}.")
        # Handle any exceptions.     

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        holidayNum = len(self.innerHolidays)
        return holidayNum

    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # filter by year
        yearFilter = list(filter(lambda a: (a.date.year == year), self.innerHolidays))
        # filter by week number
        weekFilter = list(filter(lambda a: (a.date.isocalendar()[1] == week_number), yearFilter))
        # return your holidays
        return weekFilter

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        # i don't really understand this function, just use print to display?
        for i in holidayList: print(i)

    def getWeather(self,year,weekNum):
        global city
        global weatherAPIKey
        global currentYear
        # Convert weekNum to range between two days
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        monday = datetime.strptime(f'{year} {weekNum} 1', '%G %V %u')
        timeDiff = today - monday
        # Use Try / Except to catch problems
        # the API only queries for current weather data, the historical data is not working
        if timeDiff.days < -14 or timeDiff.days > 0:
            print("This weather API only works for the current day and a forecast of 2 weeks.")
            print("There is no weather data for this time period. Please try again!")
            print(f"Current year: {currentYear}, Current week: {today.isocalendar()[1]}")
            return
        # Query API for weather in that week range
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
        querystring = {"q":city,"lat":"35","lon":"139","cnt":"16","units":"metric or imperial"}
        headers = {
            "X-RapidAPI-Key": weatherAPIKey,
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com"
        }
        weather = requests.request("GET", url, headers=headers, params=querystring).text
        # Format weather information and return weather string.
        weatherDictRaw = json.loads(weather)["list"]
        weatherDictDate = {}
        for i in range(0,len(weatherDictRaw)):
            delta = timedelta(days=i)
            day = today + delta
            weatherDictDate[day] = weatherDictRaw[i]['weather'][0]['main']
        # filter and display output for just the days in that week
        weatherDictWeek = {}
        for i in range(1,8):
            weekday = datetime.strptime(f'{year} {weekNum} {i}', '%G %V %u')
            if weekday in list(weatherDictDate.keys()):
                weatherDictWeek[weekday] = weatherDictDate[weekday]
            else:
                weatherDictWeek[weekday] = "no data"
        return weatherDictWeek

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        year = today.year
        weekN = today.isocalendar()[1]
        # Use your filter_holidays_by_week function to get the list of holidays for the current week/year
        weekHolidays = self.filter_holidays_by_week(year, weekN)
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        while True:
            weatherDisplay = str(input("Would you like to see this week's weather? [y/n]: "))
            if weatherDisplay == "y" or weatherDisplay == "n":
                break
            else: print("invalid input!")
        # If yes, use your getWeather function and display results
        print("These are the holidays for this week:")
        if weatherDisplay == "y":
            weatherData = self.getWeather(year,weekN)
            # match each holiday date to weather date and print in an f string
            for event in weekHolidays:
                weatherEvent = weatherData[event.date]
                print(f"{event} - {weatherEvent}")
        elif weatherDisplay == "n":
            self.displayHolidaysInWeek(weekHolidays)

# putting all the separate UI pages into function definitions:
def StartUp():
    theList = HolidayList()
    theList.read_json('holidays.json')
    theList.scrapeHolidays()
    totalNum = theList.numHolidays()
    print("Holiday Management")
    print("====================")
    print(f"There are {totalNum} holidays stored in the system")
    return theList

def MainMenu(theList):
    savedState = True
    while True:
        print("====================")
        print("====================")
        print("Holiday Menu")
        print("====================")
        print("1. Add a Holiday")
        print("2. Remove a Holiday")
        print("3. Save Holiday List")
        print("4. View Holidays")
        print("5. Exit")
        nextPage = int(input("What would you like to do? Enter the number of the option needed: "))
        if nextPage not in range(1,6):
            print("Wrong input!")
        else:
            if nextPage == 1: theList, savedState = AddHoliday(theList) # edits list, ss, always changes ss to false
            elif nextPage == 2: theList, savedState = RemoveHoliday(theList, savedState) 
                # edits list, ss, does not always change ss to false bc there is a leave option with 0
                # passes out new ss, list
            elif nextPage == 3: savedState = SaveHolidayList(theList, savedState)
                # option to not save -> ss required
                # needs list passed in, does not change list though
            elif nextPage == 4: ViewHolidays(theList)
                # only viewing option, no changes made to list
            elif nextPage == 5: 
                # all the saved state variables are for that one line in the exit() function
                exitstatus = Exit(savedState)
                if exitstatus == True: break

def AddHoliday(theList):
    print("Add a Holiday")
    print("====================")
    newHolidayName = str(input("Holiday: "))
    newHolidayDateRaw = str(input("Date (YYYY-MM-DD): "))
    while True:
        try:
            newHolidayDate = datetime.strptime(newHolidayDateRaw, '%Y-%m-%d')
            break
        except:
            print("Error: \nInvalid date. Please try again.")
            newHolidayDateRaw = str(input(f"Date for {newHolidayName} (YYYY-MM-DD): "))
    newHolidayObject = Holiday(newHolidayName,newHolidayDate)
    theList.addHoliday(newHolidayObject)
    print(f"Success:\n{newHolidayObject} has been added to the holiday list.")
    savedState = False
    return theList, savedState

def RemoveHoliday(theList, savedState):
    print("Remove a Holiday")
    print("====================")
    datelist = []
    datestr = ""
    count = 0

    while True:
        removeHolidayName = str(input("Holiday Name: "))
        if removeHolidayName == "0": 
            break
        allDates = theList.findHoliday(removeHolidayName,None)
        count = 0
        if len(allDates) != 0:
            for i in allDates:
                datelist.append(i.date)
                datestr += i.date.strftime("%Y-%m-%d, ")
            print(f"This holiday has been found for the following dates.")
            print(datestr)
            while True:
                removeDateRaw =  str(input("Date to be removed (YYYY-MM-DD), [a] for all: "))
                if removeDateRaw == "a": 
                    for j in datelist: theList.removeHoliday(removeHolidayName, j)
                    count += 1
                    break
                try:
                    removeDate = datetime.strptime(removeDateRaw, '%Y-%m-%d')
                    theList.removeHoliday(i.name, removeDate)
                    count += 1
                    break
                except:
                    print("Error: \nInvalid date or input. Please try again.")
            print(f"Success:\n{removeHolidayName} has been removed from the holiday list {count} times.")
            savedState = False
            break
        else:
            print(f"Error: \n{removeHolidayName} not found. Please try again, or enter 0 to exit.")
    return theList, savedState

def SaveHolidayList(theList, savedState):
    print("Saving Holiday List")
    print("====================")
    while True:
        save = str(input("Are you sure you want to save your changes? [y/n]: "))
        if save == "y":
            theList.save_to_json(newfilelocation)
            savedState = True
            print(f"Success:\nYour changes have been saved.")
            break
        elif save == "n":
            print(f"Canceled:\nHoliday list file save canceled.")
            break
        else: print("Wrong input!")
    return savedState


def ViewHolidays(theList):
    print("View Holidays")
    print("====================")
    global currentYear

    #correct year loop
    while True:
        year = int(input("Which year? "))
        if year in range(currentYear-2,currentYear+3): break
        else: 
            print("This year is likely not supported, or is in the wrong format.")
            print(f"Please enter a year between 2010 and {currentYear+2}")

    #correct week loop
    while True:
        week = str(input("Which week? #[1-52, Leave blank for the current week]: "))
        if week == "": break
        elif int(week) in range(1,53): break
        else: 
            print("This is not a possible calendar week number within a year, or is in the wrong format.")
            print(f"Please enter a week number between 1 and 52, or leave the input blank.")

    # a week input is not given: run view current week function
    if week == "":
        theList.viewCurrentWeek()
    elif int(week) in range(1,53):
        print(f"These are the holidays for {year} week #{week}:")
        displayList = theList.filter_holidays_by_week(year, int(week))
        theList.displayHolidaysInWeek(displayList)


def Exit(savedState):
    print("Exit")
    print("====================")
    while True:
        if savedState:
            exitStatus = str(input("Are you sure you want to exit? [y/n]: "))
        else: 
            exitStatus = str(input("Are you sure you want to exit?\nYour changes will be lost.\n[y/n]: "))
        if exitStatus == "y" or exitStatus == "n":
            break
        print("Wrong input!")
    if exitStatus == "y":
        # end program
        return True


def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    holidays = StartUp()
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.
    MainMenu(holidays)
    # If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





