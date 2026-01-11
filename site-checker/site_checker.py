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
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def send_telegram_alert(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": f"Site Checker Alert:\n{message}",
        "parse_mode": "HTML"
    }
    
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        log_event(f"Error in sending alert via telegram: {e}", level="ERROR")

# check if url starts with http or https and if not add https as default
def prepare_url(url: str):
    # strip lower
    url = url.strip().lower()
    print(url, 'NEW')
    if '.' not in url:
        raise ValueError(f"URL non valido: {url} (manca il dominio)")
    if not url.startswith(("http://", "https://")):
        url = "https://"+ url

    return url


# function use to check site status
def site_status_checker(url: str):
    try:
        response = requests.get(url, timeout=5)
        print(response.status_code)
        if response.status_code != 200:
            log_event(f"Request failed for {url} , status: {response.status_code}", level="ERROR")   
        else:
            log_event(f"Request success for {url} site alive , status: {response.status_code}", level="INFO")   
    except ValueError as ve:
        print(f'{ve}')

# ssl checker
def ssl_checker(hostname: str):
    print('####### STARTING WITH SSL CHECK #######')

    try:
        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # extract cert information
                cert = ssock.getpeercert()
                
                # get data format of certification
                expiry_str = cert['notAfter']
                expiry_date = datetime.datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                
                # calculate the diff from expiring date and today
                delta = expiry_date - datetime.datetime.now()
                return delta.days
    except Exception as e:
        log_event(f"Ssl check failed for {hostname}: {e}", level="ERROR")
        return None


def threshold_checker(days: int):
    print(days)
    if days < 7:
        return "CRITICAL"
    if days < 30:
        return "WARNING"
    else:
        return "OK"


# logging function to keep track of results
def log_event(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] [{level}] {message}"

    # print logs on screen
    print(formatted_message)

    # get the folder where this file is
    script_dir=os.path.dirname(os.path.abspath(__file__))
    # construct the absolute path for log file
    log_path= os.path.join(script_dir, "site_checker.log")
    
    # persistent logging for operational audit and disk usage tracking
    with open(log_path, "a") as f:
        f.write(formatted_message + "\n")



parser = argparse.ArgumentParser(description="Site and SSL Health checker")
parser.add_argument('-u', "--url", help="Check a specific url")
parser.add_argument('-t', "--threshold",  type=int, help="Minimum days before expiration. Default is 7")


# function that contains all the checks on the websites
def run_checks(url: str):
    clean_url = prepare_url(url)    
    site_status_checker(clean_url)
    days_left = ssl_checker(urlparse(clean_url).hostname)

    if days_left is not None:
        threshold = threshold_checker(days_left)

        if threshold in ["WARNING", "CRITICAL"]:
            alert_msg = f"⚠️ <b>{url}</b>\nScadenza SSL: {days_left} giorni!\nStatus: {threshold}"
            send_telegram_alert(alert_msg)

        log_event(f"Days left for cert expiration of {clean_url}: {days_left} days", threshold)
    else:
        log_event(f"SSL certificate could not be verified for {clean_url}", level="CRITICAL")

def main_check():
    target="./sites.json"

    args = parser.parse_args()
    # get the folder where this file is
    script_dir=os.path.dirname(os.path.abspath(__file__))
    # construct the absolute path for log file
    json_path= os.path.join(script_dir, target)


    # url check for single file
    if args.url: 
        print(f"Controllo il singolo url {args.url}")
        
        run_checks(args.url)
    else:
        # url check from json
        print(f"Nessun URL , leggo il file site.json")
        with open(json_path) as f:
            d = json.load(f)
            for data in d:
                name = data.get('name', 'no name specified')    
                url = data.get('url')
                if not url:
                    print(f" Skipping {name} url missing \n")
                print(f"Checking {name}: {url} \n")
                run_checks(url)



def main():
  log_event("####### START CHECK #######")
  try:
     main_check()
  finally:      
    log_event(f'####### END CHECK ####### \n')


if __name__ == "__main__":
    main()

