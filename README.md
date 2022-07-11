# Holiday Manager
- This application is meant to be run on the command line by running the holiday_manager.py file: python holiday_manager.py
- You will need version 3.8 Python or higher.

## Notes (for graders!!)
- There is a config.py file that needs to be made. It only includes a variable for the weather API key: "weatherAPIKey". Just create a python file named config py and have the following line: weatherAPIKey = "(your rapidAPI 16 day forecase API key)"
- I wasn't sure if the every single addition to the holiday list needed to be an output. This is because when the program scrapes the website, it runs around 670 times. If you want to see 670 lines of output, you can uncomment the very last print in class HolidayList -> addHoliday().
- For the planning part of the rubric: a lot of my code was developed in the assessment.ipynb file in the plans folder. It's organized very loosely. In general I created code outside of the class function to test, and then tested it inside of the class member functions.

## Functionality
- This holiday manager comes preloaded with an initial holidays.json file, as well as web scraped holiday names and dates from the two years ago to two years in the future. To change the file paths or the present year benchmark used in the program, change associated variables at the top of the holiday_manager.py file.
- This holiday manager creates a list of Holiday objects for the user to interact with. You can add holidays by inputting the name and date, remove holidays by inputting the name (and later deciding on the specific date), view holidays (and weather if the you are only viewing the current week), and save your edits to a json file (output_holidays.json)
- The weather API used in this project is the Open Weather Data API hosted by RapidAPI. You have to fill out the API key in the config file. The city location of the weather API can be edited at the top of the holiday_manager.py file.