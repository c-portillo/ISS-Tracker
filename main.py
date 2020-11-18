import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime
from twilio.rest import Client

load_dotenv()   # loads .env file in current directory

# set my location
MY_LATITUDE = 40.712776
MY_LONGITUDE = -74.005974


def iss_overhead():
    """ Returns true if ISS is within 5 degrees of my current location, false otherwise """

    iss_location_response = requests.get(url='http://api.open-notify.org/iss-now.json')
    iss_location_response.raise_for_status()    # raise error if response is not successful

    # get current latitude and longitude of ISS
    iss_data = iss_location_response.json()
    latitude = float(iss_data['iss_position']['latitude'])
    longitude = float(iss_data['iss_position']['longitude'])

    # check if ISS is within 5 degrees of my location
    if MY_LATITUDE-5 <= latitude <= MY_LATITUDE+5 and MY_LONGITUDE-5 <= longitude <= MY_LONGITUDE+5:
        return True


def is_dark():
    """ Returns true if it is currently dark in my location, false otherwise """

    parameters = {
        'lat': MY_LATITUDE,
        'lng': MY_LONGITUDE,
        'formatted': 0  # switch formatting off to get 24-hour time
    }
    sunrise_sunset_response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
    sunrise_sunset_response.raise_for_status()  # raise error if response is not successful

    # parse sunrise/sunset data - NOTE: all times are in UTC
    sunrise_sunset_data = sunrise_sunset_response.json()
    sunrise = int(sunrise_sunset_data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(sunrise_sunset_data['results']['sunset'].split('T')[1].split(':')[0])

    time_now = datetime.utcnow().hour

    if time_now <= sunrise or time_now >= sunset:
        return True


while True:
    # Send SMS with Twilio if ISS is overhead and it is dark
    if iss_overhead() and is_dark():
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='Look up! The I.S.S. is overhead ☝️',
            from_=os.getenv('MY_TWILIO_NUMBER'),
            to=os.getenv('MY_PHONE_NUMBER')
        )
        print('Message sent')
        print(message.sid)

    time.sleep(60)  # execute every minute
