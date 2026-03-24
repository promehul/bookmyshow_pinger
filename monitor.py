import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from mailersend import MailerSendClient, EmailBuilder

# --- CONFIG ---
TARGET_URL = "https://in.bookmyshow.com/buytickets/dhurandhar-the-revenge-bengaluru/movie-bang-ET00478890-MT/20260327"
VENUE_NAME = "PVR: VR Bengaluru"
RECIPIENT_EMAIL = "khetanmehul@gmail.com"

def send_alert_email():
    ms = MailerSendClient("mlsn.0ff401e8371ab2787f39f36f27efe619adda2d11607824e9b1748fa0949aeb56")

    email = (EmailBuilder()
            .from_email("MS_Lr507l@test-eqvygm0wqmdl0p7w.mlsender.net", "Harshit Khetan")
            .to_many([{"email": RECIPIENT_EMAIL, "name": "Recipient"}, {"email": "suyashsinha1999@gmail.com", "name": "Recipient"}, {"email": "avibyahut@gmail.com", "name": "Recipient"}])
            .subject(f"🔥 TICKETS LIVE: {VENUE_NAME}")
            .html(f"Dhurandhar: The Revenge shows for March 27th are now listed at {VENUE_NAME}. <br><br><b>Book Now:</b> <a href='{TARGET_URL}'>Click Here</a>")
            .build())

    response = ms.emails.send(email)
    print(f"Email sent: {response}")

def check_tickets():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(TARGET_URL)
        time.sleep(10) # Essential for BMS heavy React components
        
        # Case-insensitive check
        if VENUE_NAME.lower() in driver.page_source.lower():
            print(f"[{time.strftime('%H:%M:%S')}] FOUND: {VENUE_NAME}")
            send_alert_email()
            return True
        
        print(f"[{time.strftime('%H:%M:%S')}] Not found yet.")
        return False
    except Exception as e:
        print(f"Error during check: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    check_tickets()