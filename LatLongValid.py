
def LatLongValid(latitude,longitude):

    latlong_valid = False
    weather_latitude = "invalid"
    weather_longitude = "invalid"

    try:
        val_lat = int(latitude)
        val_long = int(longitude)
        latlong_isanumber = True
    except ValueError:
        try:
          val_lat = float(latitude)
          val_long = float(longitude)
          latlong_isanumber = True
        except ValueError:
            latlong_isanumber = False

    if latlong_isanumber:
        weather_latitude = float(latitude)
        weather_longitude = float(longitude)
        if ((weather_latitude >= -90.0) and (weather_latitude <= 90.0)):
            if ((weather_longitude >= -180.0) and (weather_longitude
                                               <= 180.)):
                latlong_valid = True
            else:
                latlong_valid = False

    latlong = {"latlong_valid": latlong_valid,
               "weather_latitude" : weather_latitude,"weather_longitude": weather_longitude }

    return latlong