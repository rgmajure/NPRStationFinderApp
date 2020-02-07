import json, requests

#This functions returns weather summary data such as sunny, raining, etc as well as the temperature for
    #a specific latitude and longitude in degrees
#This weather data is displayed on the Favorite Radio stations table for each station U.S. city.

#DarkSky is the weather service provider.

#This function will generate a test file for use in debug and test if generate_weathertest_file is True.
#If weather_test_mode is True, the generated data will be used in place of actual calls to the DarkSky API.

def DarkSkyaccess(weather_latitude,weather_longitude,weather_auth,
                  weather_test_mode, generate_weathertest_file):

    #These next lines construct the weatherstring URL string for use in requesting the data for the API endpoint.

    weatherurl = "https://api.darksky.net/forecast/"
    weather_auth = str(weather_auth) + '/'
    weather_latitude = str(weather_latitude)
    weather_longitude = str(weather_longitude)
    weatherstring = weatherurl + weather_auth + weather_latitude + ',' + weather_longitude

    #Check if this is test mode
    if not weather_test_mode:
        #make the API call using the requests library
        response = requests.get(weatherstring)
        y = json.loads(response.text)

        #Check for a valid API response
        if response.status_code == 200:
            weather_valid = True
            weather_daily_limit = False
            #Retrieve the summary and temperature from the JSON file
            weather_summary = (y["currently"]["summary"])
            weather_temperature = (y["currently"]["temperature"])
        else:
            weather_valid = False
            if response.status_code == 423:
                weather_daily_limit = True

        #If needed, create a test file using the live API data
        if generate_weathertest_file:
            with open('darkskytestdata.txt', 'w') as f:
                f.write(response.text)
                f.close()
    else:
        #Use the stored data instead of making the API call
        #This reduces the number of API requests during test and debug
        with open('darkskytestdata.txt', 'r') as f:
            x = f.read()
            y = json.loads(x)
            f.close()
            weather_valid = True
            #Retrieve the summary and temperature from the JSON file
            weather_summary = (y["currently"]["summary"])
            weather_temperature = (y["currently"]["temperature"])

    #Store the summary and temperature for return in a data dictionary
    weatherdata = {"summary": weather_summary, "temperature":
        weather_temperature, "valid" : weather_valid, "weatheer_daily_limit" : weather_daily_limit}

    return weatherdata
