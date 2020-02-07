<h1>National Public Radio (NPR) Station Finder</h1>

![](/radiobanner.png)

In the United States, we have a public radio network, National Public Radio (NPR), consisting of non-profit radio stations. Stations broadcast popular news and entertainment shows such as “Morning Edition” and “Wait, Wait, Don’t Tell Me.” 
From a technology perspective, NPR offers the NPR One Developement Center. https://dev.npr.org/api/

This NPR Station Finder Azure-based Python-Flask application and uses the NPR One Station Finder Service API to respond to a user query about a city or station call letters. Within the application, the Python module NPRoneaccess handles the query and returns either the station information or status indicating the station could not be found. Or, in some cases, the app exceeded the NPR daily call limit. To use this software, one must sign up for an NPR personal account and retrieve an Oauth 2.0 access token. For personal users the daily API call limit is 300.

In addition, to finding the NPR station, the app looks up the latitude and longitude of the station city, using the Azure Maps Service. And, it passes the location data to the DarkSky weather app that subsequently returns the weather conditions for the station’s city. All of this is displayed in a table format on the web page. Click here for the demo website: https://majureworksazure.azurewebsites.net/. The app flow is shown below.

![](/stationfinderflow.png)

<h2>Station Finder Python Functions<h3>

<h3>NPROne Access Function</h3>

This function accepts the station_search_parameter and must be a U.S. city or 4 station call letters such as "KUOW".

An Oauth 2.0 authorization token is required to access the NPR One API. The developer supplies their own token.

For my demonstration site I use a personal NPR account which limits API calls to 300 maximum per day.

Authorization details can be found on the NPR One Dev website.

**_NPROne Access Function - NPRstation_test_mode and generate_NPRstationtest-file_**

I provide the above test-related flags to assist in test and debug while avoiding the 300 daily call limit.

If NPRstation_test_mode is True, this function reads a JSON file instead of using the NPR One API.

If generate_NPRstationtest_file is True, this function generates a JSON test file from an actual NPR One API call.

**_Error Handling_**

If the NPR One API returns a status other than 200, then the function retuns either "No Station Found" or "NPR Daily Call Limit Exceeded" in the data dictionary values. The main program uses station_call_letters to check for these two situations.

<h3>genlatlong Function</h3>

The _genlatlong_ function uses the Azure Map Service to retrieve the latitude and longitude for the NPR station's market city and state. We need the latitude and longitude to access the DarkSky API. This function also returns a validity status so that we'll not try to generate weather data without valid latitude and longitude data.

<h3>DarkSkyAccess Functions</h3>

The DarkSKyAccess function builds an API query string for use with the DarkSky API. A developer needs a personal account with DarkSky. The access token placeholder is in the app.py file near the top. The free account limits daily calls to 1000. You can add a credit and bump up the daily limit (of your choosing) for minimal cost.

The DarkSkyAccess function also supports generating test data and using test data for debug; instead of call the API. This is useful if you've hit the daily call limit.

<h2>General Design and Behavior Notes</h2>

All station data is stored in a simple text file. To ensure qussi-stateless behavior, the app reads the text file it needs to change the station data. The exception is when the app does not find a station for the entered search criteria. In this case, the page table will show a line with the search parameter followed by "Station Not Found" for all entries. This row persists until the next time a user performs a search. Then, the row is replaced with the new station and weather results. Assuming the new query results in a valid station, the new station will now persist as a permanent row in the table. Even so, the "No Station Found" query is stored in the stations file. For future querys and table refreshes, the app ignores "Stations Not Found" rows in the stations file.

