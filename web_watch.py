#!/bin/python
import requests, smtplib
from pathlib import Path
import json
import hashlib
from bs4 import BeautifulSoup
import os

dirname = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(dirname, 'config.json')

def send_mail(body):
    email_address = 'xxxxx@gmail.com'
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(email_address, 'xxxxxxx')

    from email.mime.text import MIMEText
    msg = MIMEText(body)
    msg['From'] = email_address
    msg['To'] = email_address
    msg['CC'] = "yyyyy@gmail.com"
    msg['Subject'] = "WEBSITE CHANGE ALERT"
    s.send_message(msg)
    s.quit()
    del msg


def alert_changed(site_to_alert):
    print('changed..' + site_to_alert['url'])
    send_mail(site_to_alert['url'])


def run_main():
    config_json = Path(CONFIG_FILE).read_text()
    config = json.loads(config_json)

    for idx, site in enumerate(config):
        page = requests.get(site['url'])
        soup = BeautifulSoup(page.content, 'html.parser')
        hashed = hashlib.md5(soup.text.encode('utf8')).hexdigest()
        if hashed != site['hash']:
            alert_changed(site)
        config[idx]['hash'] = hashed

    with open(CONFIG_FILE, 'w') as fp:
        json.dump(config, fp, sort_keys=True, indent=4)


if __name__ == '__main__':
    run_main()

