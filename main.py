import requests

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

# test
print(f'latitude: {latitude}')
print(f'longitude: {longitude}')