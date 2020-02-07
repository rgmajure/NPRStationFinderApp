stations = []
#This the Station class used for retreiving and storing station data.
#At this point, I've not defined any methods; preferring to use the other functions for API access, etc.

class Station:


	def __init__(self, station_search_parameter, station_call_letters, station_band, station_frequency,
				 station_city, station_state, station_format,
				 station_weather_summary, station_weather_temperature,
				 station_tagline, station_programfeedurl):
		self.station_search_parameter = station_search_parameter
		self.station_call_letters = station_call_letters
		self.station_band = station_band
		self.station_frequency = station_frequency
		self.station_city = station_city
		self.station_state = station_state
		self.station_format = station_format
		self.station_weather_summary = station_weather_summary
		self.station_weather_temperature = station_weather_temperature
		self.station_tagline = station_tagline
		self.station_programfeedurl = station_programfeedurl
		self.stations_row = str(station_search_parameter) + ',' + str(station_call_letters) + ',' + str(station_band) + ',' + str(station_frequency) + ',' + str(station_city) + ',' + str(station_state) + ',' + str(station_format) + ',' + str(station_weather_summary) + str(station_weather_temperature) + ',' + str(station_tagline) + ',' + str(station_programfeedurl) + '\n'
		stations.append(self)


