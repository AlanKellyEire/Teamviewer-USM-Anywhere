# Created by Alan Kelly (alan.kelly@levelblue.com)
# Last updated 20032025

import requests
import json
import os
import datetime
import socket

CONFIG_FILE = 'teamviewer-config.json'
CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), CONFIG_FILE)
CONFIG_DATA = {
    "sensor_ip": "x.x.x.x",
    "access_token": "XXXXXX",
    "last_log_time": "YYYY-MM-DDTHH:MM:SSZ",
}

try:
    # try to load user data from file
    with open(CONFIG_PATH) as f:
        CONFIG_DATA = json.load(f)
except ValueError:
    # if file exists but it's malformed we load add a flag
    CONFIG_DATA['malformed'] = True
except Exception:
    # if file doesn't exist, we create it
    with open(CONFIG_PATH, 'w') as f:
        f.write(json.dumps(CONFIG_DATA, indent=4, sort_keys=True))
if any(item not in CONFIG_DATA for item in
       ['access_token', 'last_log_time', 'sensor_ip']):
    print("Config is Malformed")



# UDP port to send the log to. UDP port.
UDP_PORT = 514
# TCP port to send the log to. UDP port.
TCP_PORT = 601


# sending logs over TCP
def send_tcp(ip, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
    except Exception as e:
        print(
            f"Exiting!! Error Occured when trying to connect to Sensor! Please make sure Sensor is reachable on {ip} and on port {port}")
        print(e)
        exit(1)
    s.sendall(bytes(str(message), "utf-8"))
    s.close()


# Sending logs over UDP
def send_udp(ip, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(bytes(str(message), "utf-8"), (ip, port))
    s.close()


# get logs from api response and loop through
def send_logs(ip, mylist):
    for idx, i in enumerate(mylist):
        # converting dict to json so it formats correctly in USMA
        json_object = json.dumps(i)
        print(json_object)
        # sending event/log to sensor via TCP
        send_tcp(ip, TCP_PORT, json_object)


def process_logs(list, CONFIG_DATA):
    # testing if results were gotten.
    if len(list) != 0:
        # sending logs to sensor if incidents returned by API.
        send_logs(CONFIG_DATA['sensor_ip'], list)


# headers for request with the access_token from the config
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f"Bearer {CONFIG_DATA['access_token']}"
}

#getting current time in correct format to query API.
time_now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z"

# Using time from config as start time and time now in request
data = { "startDate":f"{CONFIG_DATA['last_log_time']}", "endDate":f"{time_now}" }

# making request
rr = requests.post('https://webapi.teamviewer.com/api/v1/EventLogging', headers=headers, data=str(data))

# if only 1 page of results
if  rr.json()['ContinuationToken'] == None:
    # processing logs
    process_logs(rr.json()['AuditEvents'], CONFIG_DATA)
else:
    # processing logs
    process_logs(rr.json()['AuditEvents'], CONFIG_DATA)
    # if more than one page looping through them all
    while rr.json()['ContinuationToken'] != None:
        data["ContinuationToken"] = rr.json()['ContinuationToken']
        rr = requests.post('https://webapi.teamviewer.com/api/v1/EventLogging', headers=headers, data=str(data))
        process_logs(rr.json()['AuditEvents'], CONFIG_DATA)

# saving config with current time to use as start time the next time.
CONFIG_DATA['last_log_time'] = time_now
# saving config with new timestamp
with open(CONFIG_PATH, 'w') as f:
    f.write(json.dumps(CONFIG_DATA, indent=4, sort_keys=True))
