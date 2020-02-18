from flask import Flask, render_template, redirect, url_for, request, flash
import csv, json
import NPRoneaccess
import DarkSkyaccess
import genlatlong
from station import Station

app = Flask(__name__)

stations = []
old_stations =[]

#The first part of this application is start-up focused
#Initializing arguments and credentials
#Updating the weather information for stations already in the database

#initialize DarkSky switch arguments
weather_test_mode = False
generate_weathertest_file = False

#initialize NPR One station switch arguments
NPRstation_test_mode = False
generate_NPRstationtest_file = False

#Initialize API credentials
#Each developer needs to establish accounts with DarkSky, NPR One, and Azure Maps Service

weather_auth = {your credential here}
NPR_authorization_token = {your credential here}
map_subscription_key = {your credential here}

#Read existing station database

with open('stations.txt') as csv_file:
    #The station storage file has commas for delimiters
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        #The storage file columns have headers
        if line_count == 0:
            #skip column titles
            line_count += 1
        else:
            old_station_search_parameter = row[0]
            old_station_call_letters = row[1]
            old_station_band = row[2]
            old_station_frequency = row[3]
            old_station_city = row[4]
            old_station_state = row[5]
            old_station_format = row[6]
            old_station_weather_summary = row[7]
            old_station_weather_temperature = row[8]
            old_station_tagline = row[9]
            old_station_programfeedurl = str(row[10])
            #Get current weather conditions for stations in database
            #getlatlong uses the Azure Map Service to retrieve latitude and longitude for station's city
            if (old_station_call_letters != "No Station Found") and (old_station_call_letters != 'NPR Daily Call Limit Exceeded'):
                getlatlong = genlatlong.genlatlong(old_station_city, old_station_state, map_subscription_key)
                latlong_valid = getlatlong["map_latlong_valid"]
                weather_latitude = getlatlong["map_latitude"]
                weather_longitude = getlatlong["map_longitude"]
                #Ensure getlatlong returned a valid response before accessing the DarkSky API
                if latlong_valid:
                    weather = DarkSkyaccess.DarkSkyaccess(weather_latitude,
                            weather_longitude,
                            weather_auth,
                            weather_test_mode, generate_weathertest_file)
                    #Check for valid url response
                    weather_valid = (weather["valid"])
                    old_station_latitude = weather_latitude
                    old_station_longitude = weather_longitude
                    #If we received a valid weather response, store it for previously searched stations
                    ifweather_valid == True:
                        old_station_weather_summary = (weather["summary"])
                        old_station_weather_temperature = int(weather["temperature"])
                    else:
                        #List weather as unavailable for previously searched stations
                        old_station_weather_summary = "unavailable"
                        old_station_weather_temperature = "unavailable"
                else:
                    #If we didn't receive a valid latitude and longitude, also list weather as unavailable
                    old_station_weather_summary = "unavailable"
                    old_station_weather_temperature = "unavailable"

                #update existing stations with updated weather information
                old_station = Station(old_station_search_parameter, old_station_call_letters, old_station_band,
                                  old_station_frequency, old_station_city,
                                  old_station_state, old_station_format,
                                  old_station_weather_summary,
                                  old_station_weather_temperature,
                                  old_station_tagline, old_station_programfeedurl)
                stations.append(old_station)

            line_count += 1

csv_file.close()

#This concludes the start-up section


#This section is about responding to a user search request (station or call letters)

@app.route("/", methods=["GET", "POST"])
def stations_page():
    if request.method == "POST":
        #All stations must be "NPR" but I carry the station format variable for future feature expansion
        new_station_format = "NPR"
        #After each search request, we do a fresh read of the database
            #This supports stateless operation
        stations.clear()
        station_call_letters_dup = []
        station_city_dup = []
        with open('stations.txt') as csv_file:
            # The station storage file has commas for delimiters
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # The storage file columns have headers
                if line_count == 0:
                    # skip column titles
                    line_count += 1
                else:
                    old_station_search_parameter = row[0]
                    old_station_call_letters = row[1]
                    old_station_band = row[2]
                    old_station_frequency = row[3]
                    old_station_city = row[4]
                    old_station_state = row[5]
                    old_station_format = row[6]
                    old_station_tagline = row[9]
                    old_station_programfeedurl = str(row[10])
                    
                    #Prepare for duplication check later by saving the old station
                    if old_station_call_letters != "No Station Found":
                        station_call_letters_dup.append(old_station_call_letters)
                        station_city_dup.append(old_station_city)

                    if ((old_station_call_letters != "No Station Found") and (old_station_call_letters != "NPR Daily Call Limit Exceeded")):
                        # Get current weather conditions for stations in database
                        # getlatlong uses the Azure Map Service to retrieve latitude and longitude for station's city

                        getlatlong = genlatlong.genlatlong(old_station_city, old_station_state, map_subscription_key)
                        latlong_valid = getlatlong["map_latlong_valid"]
                        weather_latitude = getlatlong["map_latitude"]
                        weather_longitude = getlatlong["map_longitude"]
                        # Ensure getlatlong returned a valid response before accessing the DarkSky API
                        if latlong_valid:
                            weather = DarkSkyaccess.DarkSkyaccess(weather_latitude,
                                                              weather_longitude,
                                                              weather_auth,
                                                              weather_test_mode, generate_weathertest_file)
                            # Check for valid url response
                            weather_valid = (weather["valid"])
                          # If we received a valid weather response, store it for previously searched stations
                            if (weather_valid == True):
                                old_station_weather_summary = (weather["summary"])
                                old_station_weather_temperature = int(weather["temperature"])
                            else:
                                # List weather as unavailable for previously searched stations
                                old_station_weather_summary = "unavailable"
                                old_station_weather_temperature = "unavailable"
                        else:
                            # If we didn't receive a valid latitude and longitude, also list weather as unavailable
                            old_station_weather_summary = "unavailable"
                            old_station_weather_temperature = "unavailable"

                        #update existing stations in database with updated weather information

                        old_station = Station(old_station_search_parameter, old_station_call_letters, old_station_band,
                                          old_station_frequency, old_station_city,
                                          old_station_state, old_station_format,
                                          old_station_weather_summary,
                                          old_station_weather_temperature,
                                          old_station_tagline, old_station_programfeedurl)
                        stations.append(old_station)
                    line_count += 1
        csv_file.close()

#       Prompt user for input
        station_search_parameter = request.form.get("station_search_parameter", "")

#       Obtain NPR station data

        new_station_search_parameter = str(station_search_parameter)

        #check for duplication
        skip = False
        for i in range(len(station_city_dup)):
            print(station_city_dup[i])
            if station_city_dup[i] == new_station_search_parameter:
                skip = True
            if station_call_letters_dup[i] == new_station_search_parameter:
                skip = True
        print(skip)

        if skip == False:

            NPRstation = NPRoneaccess.NPRoneaccess(new_station_search_parameter,
                                                   NPR_authorization_token,
                                                   NPRstation_test_mode,
                                                   generate_NPRstationtest_file)
            NPRstation_valid = (NPRstation["stationvalid"])
            NPR_daily_limit = NPRstation["NPR_daily_limit"]

            #If we find a valid station, we retrieve the needed data from the JSON-like response(Python data dictionary)


            new_station_call_letters = (NPRstation["call"])
            new_station_band = (NPRstation["band"])
            new_station_frequency = (NPRstation["freq"])
            new_station_city = (NPRstation["marketCity"])
            new_station_state = (NPRstation["marketState"])
            new_station_tagline = (NPRstation["tagline"])
            new_station_programfeedurl = str((NPRstation["programfeedurl"]))

            if NPRstation_valid:
                #Obtain weather for new station

                # Get current weather conditions for stations in database
                # getlatlong uses the Azure Map Service to retrieve latitude and longitude for station's city
                getlatlong = genlatlong.genlatlong(new_station_city, new_station_state, map_subscription_key)
                latlong_valid = getlatlong["map_latlong_valid"]
                weather_latitude = getlatlong["map_latitude"]
                weather_longitude = getlatlong["map_longitude"]

                # Ensure getlatlong returned a valid response before accessing the DarkSky API
                if (latlong_valid):

                    weather = DarkSkyaccess.DarkSkyaccess(weather_latitude,
                                              weather_longitude,
                                              weather_auth,
                                              weather_test_mode, generate_weathertest_file)
                    # Check for valid url response
                    weather_valid = (weather["valid"])
                    # If we received a valid weather response, store it for previously searched stations
                    if weather_valid == True:
                       new_station_weather_summary= (weather["summary"])
                       new_station_weather_temperature = int(weather["temperature"])
                    else:
                        # List weather as unavailable for the searched stations
                        new_station_weather_summary = "unavailable"
                        new_station_weather_temperature = "unavailable"
                else:
                    #If we didn't receive a valid latitude and longitude, also list weather as unavailable
                    new_station_weather_summary = "unavailable"
                    new_station_weather_temperature = "unavailable"

            else:
                if NPR_daily_limit == False:
                    new_station_weather_summary = "Station Not Found"
                    new_station_weather_temperature = "Station Not Found"
                else:
                    new_station_weather_summary = "NPR Daily Call Limit Exceeded"
                    new_station_weather_temperature = "NPR Daily Call Limit Exceeded"

            #Store new station data in stations list
            new_station = Station(new_station_search_parameter, new_station_call_letters, new_station_band,
                    new_station_frequency, new_station_city,
                    new_station_state, new_station_format,
                    new_station_weather_summary,
                    new_station_weather_temperature, new_station_tagline, new_station_programfeedurl)
            stations.append(new_station)

#       Store new station in database
            with open('stations.txt', 'a+') as f:
                f.write(str(new_station_search_parameter) + ',' + str(new_station_call_letters) + ',' + str(new_station_band) + ',' + str(new_station_frequency) + ',' +str(new_station_city) + ',' + str(new_station_state) + ','+ str(new_station_format) + ',' +
                    str(new_station_weather_summary) + ',' + str(new_station_weather_temperature) + ',' + str(new_station_tagline) + ',' + str(new_station_programfeedurl) + '\n')
                f.close()

        return redirect(url_for("stations_page"))
    #Let's render the new page
    return render_template("index.html", stations=stations)

if __name__ == "__main__":
    app.run(debug=True)
