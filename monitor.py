import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from mailersend import emails

# --- CONFIG ---
TARGET_URL = "https://in.bookmyshow.com/buytickets/dhurandhar-the-revenge-bengaluru/movie-bang-ET00478890-MT/20260327"
VENUE_NAME = "PVR: VR Bengaluru"
RECIPIENT_EMAIL = "khetanmehul@gmail.com"

def send_alert_email():
    # MailerSend Initialization using the official SDK pattern
    mailer = emails.NewEmail('mlsn.0ff401e8371ab2787f39f36f27efe619adda2d11607824e9b1748fa0949aeb56')

    # Define the sender (Must be a domain verified in your MailerSend dashboard)
    mail_from = {
        "name": "BMS Monitor",
        "email": 'MS_Lr507l@test-eqvygm0wqmdl0p7w.mlsender.net',
    }

    # Define the recipient
    recipients = [
        {
            "name": "Mehul Khetan",
            "email": RECIPIENT_EMAIL,
        }
    ]

    subject = f"🔥 TICKETS LIVE: {VENUE_NAME}"
    content = f"Dhurandhar: The Revenge shows for March 27th are now listed at {VENUE_NAME}. <br><br><b>Book Now:</b> <a href='{TARGET_URL}'>Click Here</a>"

    mailer.set_mail_from(mail_from, recipients)
    mailer.set_subject(subject)
    mailer.set_html_content(content)
    mailer.set_plaintext_content(f"Tickets for {VENUE_NAME} are LIVE! Book here: {TARGET_URL}")

    response = mailer.send()
    print(f"Email sent successfully. Response: {response}")

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