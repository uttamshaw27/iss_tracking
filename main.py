import requests
from datetime import datetime, timezone, timedelta
import smtplib
import time


MY_EMAIL = "sharehome20@gmail.com"
MY_PASSWORD = "xbfknrnualnmxjaj"
MY_LATITUDE = 22.572645
MY_LONGITUDE = 88.363892


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    print(iss_latitude, iss_longitude, datetime.now())

    # Your position is +5 or -5 degrees of ISS position
    if MY_LATITUDE - 5 <= iss_latitude <= MY_LATITUDE + 5 and MY_LONGITUDE - 5 <= iss_longitude <= MY_LONGITUDE + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LATITUDE,
        "log": MY_LONGITUDE,
        "formatted": 0,
    }
    response = requests.get(url="http://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now(timezone(timedelta(hours=+5))).hour
    print(time_now)

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(10)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="shaw.uttam03@gmail.com",
            msg=f"Subject:Look up\n\nThe ISS is above you in the sky."
        )
        print("Msg has been sent!")
