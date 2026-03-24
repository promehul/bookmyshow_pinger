import os
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIG ---
TARGET_URL = "https://in.bookmyshow.com/buytickets/dhurandhar-the-revenge-bengaluru/movie-bang-ET00478890-MT/20260327"
VENUE_NAME = "PVR: VR Bengaluru"

def send_email():
    sender = 'MS_Lr507l@test-eqvygm0wqmdl0p7w.mlsender.net'
    password = 'mssp.56Cx1tf.k68zxl2y3qe4j905.Mq6mx47'
    receiver = "khetanmehul@gmail.com"
    
    msg = MIMEText(f"Tickets for Dhurandhar are LIVE at {VENUE_NAME}!\nBook here: {TARGET_URL}")
    msg['Subject'] = "ALERT: Dhurandhar Tickets Available!"
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL('smtp.mailersend.net', 587) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

def check_tickets():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(TARGET_URL)
        time.sleep(10) # Heavy React sites need extra time on GH runners
        if VENUE_NAME.lower() in driver.page_source.lower():
            print(f"MATCH FOUND: {VENUE_NAME}")
            send_email()
            return True
        print(f"Status: {VENUE_NAME} not found yet.")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    check_tickets()