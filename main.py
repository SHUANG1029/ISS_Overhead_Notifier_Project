import requests
import datetime as dt
import smtplib
import time

MY_LAT = -33.791770
MY_LNG = 151.080570

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}


def is_over_your_head():
    iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss.raise_for_status()
    iss_data = iss.json()
    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])
    if MY_LAT - 5 < iss_latitude < MY_LAT + 5 and MY_LNG - 5 < iss_longitude < MY_LNG + 5:
        return True


def is_at_night():
    time.sleep(60)
    time_now = dt.datetime.now()
    now_hour = time_now.hour
    response = requests.get(url="http://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]
    sunrise = sunrise.split("T")[1]
    sunrise = sunrise.split(":")
    sunrise_hour = int(sunrise[0]) + 10
    sunset = sunset.split("T")[1]
    sunset = sunset.split(":")
    sunset_hour = int(sunset[0]) + 10
    if sunrise_hour >= now_hour >= sunset_hour:
        return True


while True:
    if is_over_your_head() and is_at_night():
        my_email = "sophiameng88@gmail.com"
        password = "lfovowyqdgmguiqh"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="lovechangjin@gmail.com",
                msg="subject: Look Up!!👆 \n\nSatellite is flying over your head!"
            )
