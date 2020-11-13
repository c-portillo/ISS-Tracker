import requests
from datetime import datetime

# set my location
MY_LATITUDE = 40.712776
MY_LONGITUDE = -74.005974

# get ISS location data
ISS_location_response = requests.get(url='http://api.open-notify.org/iss-now.json')

# raise appropriate error if response is not successful
ISS_location_response.raise_for_status()

# parse ISS location data
ISS_data = ISS_location_response.json()
latitude = ISS_data['iss_position']['latitude']
longitude = ISS_data['iss_position']['longitude']

# get my location's sunrise/sunset time data
parameters = {
    'lat': MY_LATITUDE,
    'lng': MY_LONGITUDE,
    'formatted': 0  # switch formatting off to get 24-hour time
}
sunrise_sunset_response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
sunrise_sunset_response.raise_for_status()

# parse sunrise/sunset data - NOTE: all times are in UTC
sunrise_sunset_data = sunrise_sunset_response.json()
sunrise = sunrise_sunset_data['results']['sunrise'].split('T')[1].split(':')[0]
sunset = sunrise_sunset_data['results']['sunset'].split('T')[1].split(':')[0]

# get current time
time_now = datetime.utcnow().hour

# test
print(f'sunrise: {sunrise}')
print(f'sunset: {sunset}')
print(f'time now: {time_now}')
print(f'ISS latitude: {latitude}')
print(f'ISS longitude: {longitude}')

