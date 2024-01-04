# Nicolo Taylor UND Ops Push Notification Server
import time
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, messaging

# Flight Restrictions URL
fr_url = "https://aims-asp.aero.und.edu/sof2/sof2.aspx?site=U"

# Flight Restriction Storage
fixedwing_last = " "
helicopter_last = " "
uas_last = " "
gfk_raw_last = " "
autowx_time_last = 9999
sof_last = " "
mod_last = " "

cred = credentials.Certificate("UNDOps_firebase.json")
firebase_admin.initialize_app(cred)


def send_topic_push(title, body, topic):
   message = messaging.Message(
      notification=messaging.Notification(title=title, body=body),
      topic=topic,
      apns=messaging.APNSConfig(payload=messaging.APNSPayload(aps=messaging.Aps(sound='default')
      )))

   messaging.send(message)

def flight_restrictions(url):
    output = []
    # Getting data
    data = requests.get(url)
    html = BeautifulSoup(data.text, 'html.parser')
    textdata1 = html.select('.auto-style1b')[0].get_text()
    output.append(textdata1)
    textdata2 = html.select('.auto-style2b')[0].get_text()
    output.append(textdata2)
    textdata3 = html.select('.auto-style3b')[0].get_text()
    output.append(textdata3)
    data.close()
    return output


while True:

    fr_live = flight_restrictions(fr_url)

    # Fixed Wing Flight Restrictions
    if fr_live[0] != fixedwing_last:
        if fixedwing_last == " ":
            # Storing last posted values
            fixedwing_last = fr_live[0]
        else:
            # Storing last posted values
            fixedwing_last = fr_live[0]
            # Posting to FR Fixed Wing channel
            send_topic_push("UND Ops", f"Fixed Wing: {fr_live[0]}", "fixedwing")

    # Helicopter Flight Restrictions
    if fr_live[1] != helicopter_last:
        if helicopter_last == " ":
            # Storing last posted values
            helicopter_last = fr_live[1]
        else:
            # Storing last posted values
            helicopter_last = fr_live[1]
            # Posting to FR Helicopter channel
            send_topic_push("UND Ops", f"Helicopter: {fr_live[1]}", "helicopter")

    # UAS Flight Restrictions
    if fr_live[2] != uas_last:
        if uas_last == " ":
            # Storing last posted values
            uas_last = fr_live[2]
        else:
            # Storing last posted values
            uas_last = fr_live[2]
            # Posting to FR UAS channel
            send_topic_push("UND Ops", f"UAS: {fr_live[2]}", "uas")
    
    time.sleep(60)
