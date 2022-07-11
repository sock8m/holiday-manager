# Holiday Manager
- This application is meant to be run on the command line by running the holiday_manager.py file: python holiday_manager.py
- You will need version 3.8 Python or higher.

## Functionality
- This holiday manager comes preloaded with an initial holidays.json file, as well as web scraped holiday names and dates from the two years ago to two years in the future. To change the file paths or the present year benchmark used in the program, change associated variables at the top of the holiday_manager.py file.
- This holiday manager creates a list of Holiday objects for the user to interact with. You can add holidays by inputting the name and date, remove holidays by inputting the name (and later deciding on the specific date), view holidays (and weather if the you are only viewing the current week), and save your edits to a json file (output_holidays.json)
- The weather API used in this project is the Open Weather Data API hosted by RapidAPI. You have to fill out the API key in the config file. The city location of the weather API can be edited at the top of the holiday_manager.py file.
- The config.py file only includes the weather API key.