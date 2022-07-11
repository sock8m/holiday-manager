flowchart TB
	N14e["Startup"]
	N14f["1. initialize list"]
	N150["2. read the json file"]
	N151["Main Menu"]
	N152["Add Holidays"]
	N153["enter name and date"]
	N154["use HolidayList.addHoliday()"]
	N155["return holiday list and turn saved state to false"]
	N157["Remove Holidays"]
	N158["enter holiday name"]
	N159["use HolidayList.findHoliday() to find list of results with that name"]
	N15a["if there are 0 results returned, that holiday is not found"]
	N15d["if there are 1 or more results returned, user chooses dates to remove"]
	N160["Save Holiday List"]
	N161["does the user want to save?"]
	N162["use HolidayList.save_to_json() to save class attribute innerHolidays to json file"]
	N163["return saved state as true"]
	N164["return to main menu"]
	N167["View Holidays"]
	N168["get user input for year and week"]
	N169["run HolidayList.viewCurrentWeek()"]
	N16a["asks user if they want to display weather data"]
	N16b["grab open weather API data, match them up with dates in a dictionary, print holidays and match dates to weather dictionary"]
	N16f["filter holidays by week using function, display"]
	N171["Exit"]
	N172["do you want to exit?"]
	N175["you have edits to save. do you want to exit?"]
	N176["end Main Menu loop"]
	N178["3. scrape the holidays from website"]
	N14e --> N14f
	N14f --> N150
	N150 --> N151
	N151 --> N152
	N152 --> N153
	N153 --> N154
	N154 --> N155
	N155 --> N164
	N151 --> N157
	N157 --> N158
	N158 --> N159
	N159 --> N15a
	N15a --> N158
	N15a --> N164
	N159 --> N15d
	N15d --> N155
	N15d --> N164
	N151 --> N160
	N160 --> N161
	N161 -- "yes" --> N162
	N162 --> N163
	N163 --> N164
	N164 --> N151
	N161 -- "no" --> N151
	N151 --> N167
	N167 --> N168
	N168 -- "no week input" --> N169
	N169 --> N16a
	N16a -- "yes" --> N16b
	N16b --> N164
	N16a -- "no" --> N16f
	N16b --> N164
	N168 -- "week input between 1 and 52" --> N16f
	N16f --> N164
	N151 --> N171
	N171 -- "saved state is true" --> N172
	N172 -- "yes to exit" --> N176
	N172 -- "no to exit" --> N164
	N171 -- "saved state is false" --> N175
	N175 -- "yes to exit" --> N176
	N175 -- "no to exit" --> N164
	N14f --> N178
	N178 --> N151