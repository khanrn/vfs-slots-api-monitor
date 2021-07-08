#!/usr/bin/env python
import os
import time
import json
import requests
import subprocess
from playsound import playsound
from urllib.parse import urlencode, quote_plus
from datetime import datetime

class NewsVFS: 
    # default constructor
    def __init__(self, params):
        self.params = params

    def get_response(self, params):
        resp = requests.get(params["url"], headers=params["headers"])
        if not 200 == resp.status_code:
            return False
        
        try:
            resp = resp.json()
        except ValueError as e:
            return False

        return resp

    def get_total(self, resp, key):
        if key in resp:
            return resp[key]
        return False

    def check_by_total(self, current, post_date):
        if key in resp:
            return resp[key]
        return False

    def intialize(self):
        print("""
██    ██ ███████ ███████     ███    ██ ███████ ██     ██ ███████          
██    ██ ██      ██          ████   ██ ██      ██     ██ ██               
██    ██ █████   ███████     ██ ██  ██ █████   ██  █  ██ ███████          
 ██  ██  ██           ██     ██  ██ ██ ██      ██ ███ ██      ██          
  ████   ██      ███████     ██   ████ ███████  ███ ███  ███████ ██ ██ ██""")
        print("\n")
        print("Watching VFS news API for update...")
        print("\n")

        count = 0
        while True:
            # Putting the script to sleep for the delay
            count += 1
            resp = self.get_response(self.params)

            print(".", end="", flush=True),

            if False == resp:
                continue
            
            total = self.get_total(resp, "total")
            if total > self.params["max_num"]:
                break
            time.sleep(self.params["delay"])
            
        print("\n")
        print("The total news count is", end =": ")
        print(total)
        subprocess.call([
            "/usr/bin/notify-send",
            "VFS Notice Update!",
            "New article published at VFS notice borad."
        ])
        print("\n")
        for i in resp["items"]:
            print("-", end =" ")
            print(i["fields"]["date"], end =" --- ")
            print(i["fields"]["body"]["content"][0]["content"][0]["value"])
            print(">>", end =" ")
            print(i["fields"]["body"]["content"][1]["content"][0]["value"])
            print("\n")
        playsound(self.params["sound"])

def main(params):
    if not os.path.isfile(params):
        return False

    path = os.path.realpath(params)
    read = open(path, "r")
    params = json.loads(read.read())
    read.close()

    params["url"] = params["url"] \
        + "?" \
        + urlencode(params["urlparams"], quote_via=quote_plus)

    resp = NewsVFS(params)
    resp.intialize()

if __name__ == "__main__":
    main("./news_creds.json")
