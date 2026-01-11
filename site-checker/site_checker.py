# used to get ssl cert
import ssl
# used to open a tcp connection on 443
import socket
# used to check if website is up
import requests
# checking the params
import argparse
import datetime
import json
import os



# Prevent website downtime
# check that ssl certificate are not expired


parser = argparse.ArgumentParser(description="Site and SSL Health checker")
parser.add_argument('-u', "--url", help="Check a specific url")
parser.add_argument('-t', "--threshold",  type=int, help="Minimum days before expiration. Default is 7")



target="./sites.json"


args = parser.parse_args()

# get the folder where this file is
script_dir=os.path.dirname(os.path.abspath(__file__))
# construct the absolute path for log file
json_path= os.path.join(script_dir, target)

if args.url: 
    print(f"Controllo il singolo url {args.url}")
    site_status_checker(args.url)
else:
    print(f"Nessun URL , leggo il file site.json")
    with open(json_path) as f:
        d = json.load(f)
        for data in d:

            name = data.get('name', 'no name specified')    
            url = data.get('url')

            if not url:
                print(f" Skipping {name} url missing")
            print(f"Checking {name}: {url}")



        # insert here all the checking functions

def ssl_checker():
    print('Checked')

def site_status_checker(url = str):
    is_up = requests.get(url)
    print(is_up)


def main():
    print('Site checker launched')


if __name__ == "__main__":
    main()
