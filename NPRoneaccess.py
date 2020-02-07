import json, requests

def NPRoneaccess(station_search_parameter,authorization_token,
			   NPRstation_test_mode, generate_NPRstationtest_file):

#This function accepts the station_search_parameter and must be a U.S. city or 4 station call letters such as "KUOW".
	#An Oauth 2.0 authorization token is required to access the NPR One API. The developer supplies their own token.
	#For my demonstration site I use a personal NPR account which limits API calls to 300 maximum per day.
	#Authorization details can be found on the NPR One Dev website.

#NPRstation_test_mode and generate_NPRstationtest-file.
	#I provide the above test-related flags to assist in test and debug while avoid the 300 daily call limit.
	#If NPRstation_test_mode is True, this function reads a JSON file instead of using the NPR One API.
	#If generate_NPRstationtest_file is True, this function generates a JSON test file from an actual NPR One API call.


	headers = {
		'accept': 'application/json',
		'Authorization': authorization_token,
	}

	#The station search parameter must be a U.S. city or station call letters.

	params = (
		('q', station_search_parameter),
	)

	if NPRstation_test_mode:

		#Use pre-stored API call data instead of an actual API call

		with open('NPRStationtestdata.txt', 'r') as f:
			x = f.read()
			y = json.loads(x)
			f.close()
			#Set the station valid flag as if real data was acquired from the API
			NPRstation_valid = True
			NPR_daily_limit = False
	else:
		#Issue the API call through the NPR one endpoint
		#Use the requests library to initiate the API call
		response = requests.get('https://station.api.npr.org/v3/stations?',
					headers = headers, params = params)
		#Check that we received valid response from the endpoint and if so, set the NPR_station_valid flag to True
		#For a personal NPR account, you may receive a status code of 429, indicated you exceeded the daily rate limit
		if response.status_code == 200:
			y = json.loads(response.text)
			NPR_daily_limit = False
			#Check to see if the NPR station data is populated, even with a valid API response
			#Specific stations may not have correctly populated their response
			if (y["items"]):
				NPRstation_valid = True
				#Check if we need to save the resopnse as a test file for future testing use,
					#thus avoiding too many API calls
				if generate_NPRstationtest_file:
					with open('NPRStationtestdata.txt', 'w') as f:
						f.write(response.text)
						f.close()
			else:
				NPRstation_valid = False
		else:
			NPRstation_valid = False
			#check to see if NPR's daily call limit exceeded
			if response.status_code == 429:
				NPR_daily_limit = True


	#Assuming we have valid data, let's capture specific items we want for our web page
	if NPRstation_valid:
		#Even now, let's be careful and use a "try" to avoid crashing our page if a data element is missing
		try:
			programfeedurl = (y["items"][0]["attributes"]["programFeeds"][0]["href"])
			programfeedname = (y["items"][0]["attributes"]["programFeeds"][0]["programId"])
			band = (y["items"][0]["attributes"]["brand"]["band"])
			call = (y["items"][0]["attributes"]["brand"]["call"])
			freq = (y["items"][0]["attributes"]["brand"]["frequency"])
			marketCity = (y["items"][0]["attributes"]["brand"]["marketCity"])
			marketState = (y["items"][0]["attributes"]["brand"]["marketState"])
			tagline = (y["items"][0]["attributes"]["brand"]["tagline"]).replace(",", ".")
			stationstreamtype = (y["items"][0]["attributes"]["streamsV2"][0][
			"urls"][0]["typeName"])
			stationstreamurl = (y["items"][0]["attributes"]["streamsV2"][0]["urls"][0]["href"])
		except:
			#Even though we've run multiple data checks, if something is missing at this point, let's set the validity to False
			NPRstation_valid = False
			NPR_daily_limit = False


	if ((NPRstation_valid == False) and (NPR_daily_limit == False)):
		band = "No Station Found"
		call = "No Station Found"
		freq = "No Station Found"
		marketCity = "No Station Found"
		marketState = "No Station Found"
		tagline = "No Station Found"
		programfeedname = "No Station Found"
		programfeedurl = "No Station Found"
		stationstreamtype = "No Station Found"
		stationstreamurl = "No Station Found"

	if NPR_daily_limit:
		band = "NPR Daily Call Limit Exceeded"
		call = "NPR Daily Call Limit Exceeded"
		freq = "NPR Daily Call Limit Exceeded"
		marketCity = "NPR Daily Call Limit Exceeded"
		marketState = "NPR Daily Call Limit Exceeded"
		tagline = "NPR Daily Call Limit Exceeded"
		programfeedname = "NPR Daily Call Limit Exceeded"
		programfeedurl = "NPR Daily Call Limit Exceeded"
		stationstreamtype = "NPR Daily Call Limit Exceeded"
		stationstreamurl = "NPR Daily Call Limit Exceeded"

	#Let's populate the stationdate Python dictionary.
	stationdata = {"band" : band, "call" : call, "freq"
	: freq, "marketCity" : marketCity, "marketState" : marketState, "tagline"
	: tagline, "programfeedname": programfeedname, "programfeedurl": programfeedurl,
	"stationstreamtype": stationstreamtype,"stationstreamurl" : stationstreamurl, "stationvalid" : NPRstation_valid,
	"NPR_daily_limit" : NPR_daily_limit}


	return stationdata
