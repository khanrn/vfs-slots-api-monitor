#!/usr/bin/env python
import os
import sys
import time
import json
import requests
import subprocess
from playsound import playsound
from urllib.parse import urlencode, quote_plus
from datetime import datetime, timedelta

class PingVFS:
    # default constructor
    def __init__(self, params):
        self.url = params["url"]
        self.urlparams = params["urlparams"]
        self.paths = params["paths"]
        self.auth = ""
        self.start_time = datetime.now()
        self.sound = params["sound"]

    def get_auth_token(self):
        if not os.path.isfile(self.paths["auth"]):
            return False

        path = os.path.realpath(self.paths["auth"])
        read = open(path, "r")
        auth = read.read().replace("\n", " ")
        read.close()

        if auth == self.auth:
            return self.auth

        self.auth = auth
        # os.remove(path)
        return self.auth

    def store_output(self, output):
        # Saving the output in result.txt.
        with open(self.paths["output"], "a") as file_object:
            # Append 'hello' at the end of file
            file_object.write(output)
    def get_foramtted_date(self, date):
        return datetime.strptime(str(date), "%Y-%m-%d").strftime("%d/%m/%Y")

    def hit_vfs(self):
        headers = {
            "Content-length" : "0",
            "Content-type" : "application/json",
        }

        headers["Authorization"] = self.auth

        from_date = datetime.now().date() + timedelta(days = 1)
        to_date = from_date + timedelta(days = 90)

        self.urlparams["fromDate"] = str(self.get_foramtted_date(from_date))
        self.urlparams["toDate"] = str(self.get_foramtted_date(to_date))

        url = self.url \
            + "?" \
            + urlencode(self.urlparams, quote_via=quote_plus)

        try:
            resp = requests.get(url, headers=headers)
        except:
            return "ERROR Connection Refused"

        if os.path.isfile(self.paths["auth"]):
            self.get_auth_token()

        try:
            resp = resp.json()
        except:
            return "ERROR " + str(resp.status_code)
        
        return json.dumps(resp)

    def init(self):
        auth = self.get_auth_token()
        count = 0

        print("""
██    ██ ███████ ███████     ███████ ██       ██████  ████████ ███████          
██    ██ ██      ██          ██      ██      ██    ██    ██    ██               
██    ██ █████   ███████     ███████ ██      ██    ██    ██    ███████          
 ██  ██  ██           ██          ██ ██      ██    ██    ██         ██          
  ████   ██      ███████     ███████ ███████  ██████     ██    ███████ ██ ██ ██""")

        print("\n")
        print("Started at:", end =" ")
        print(datetime.now())
        print("Trying to access VFS appointment API for slots...")
        print("\n")

        while True:
            time.sleep(5)

            request = self.hit_vfs()
            count += 1

            output = "\nOutput: " \
                + str(request) \
                + "\nTime: " \
                + str(datetime.now()) \
                + "\nCount: " \
                + str(count) \
                + "\n==="

            self.store_output(output)

            # Printing the output in terminal.
            # print(output)
            print(".", end="", flush=True),

            if request == "[[]]":
                continue
            try:
                request = json.loads(request)
            except:
                continue

            try:
                if request[0]["counters"] != None:
                    break
            except:
                continue

        subprocess.call([
            "/usr/bin/notify-send",
            "VFS Slots!!!",
            "Something Positive May Have Happend."
        ])
        print("\n")
        print(str(count) + " times HTTP 200 response received.")
        print("Ended at:", end =" ")
        print(datetime.now())
        time_diff = datetime.now() - self.start_time
        time_diff = time_diff.total_seconds() / 60.0
        print("Script ran for " + str(time_diff) + " minutes")
        # Will play the alert sound.
        playsound(self.sound)
        

def main(params):
    if not os.path.isfile(params):
        return False

    path = os.path.realpath(params)
    read = open(path, "r")
    params = json.loads(read.read())
    read.close()
    
    ping = PingVFS(params)
    ping.init()

if __name__ == "__main__":
    main("./ping_creds.json")
