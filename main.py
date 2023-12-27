# birthday_checker.py

from datetime import datetime
import smtplib
import email
import ssl
from providers import PROVIDERS

with open('birthdays.txt', 'r') as file:
    birthday_dict = {bday.strip(): [num.strip(), carrier.strip(), name.strip(), relationship.strip()] for bday, name, num, carrier, relationship in (line.split(":") for line in file)}

with open('sender_credentials.txt', 'r') as credentials:
    gmail, password = credentials.readlines()

current_date = current_month = '-'.join(str(datetime.now().date()).split("-")[1:])

def send_sms_via_email(
    number: str, 
    message: str, 
    provider: str, 
    sender_credentials: tuple, 
    subject: str = "", 
    smtp_server = "smtp.gmail.com", 
    smtp_port: int = 465
):
    sender_email, email_password = sender_credentials
    reciever_email = f"{number}@{PROVIDERS.get(provider).get('sms')}"

    email_message = f"Subject:{subject}\nTo:{reciever_email}\n{message}"

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, reciever_email, email_message)

if current_date in birthday_dict.keys():
    info = birthday_dict[current_date]
    message = f"Happy birthday {info[2]}!"
    if info[3] == "Friend":
        message = "happy bday bro"
    sender_credentials = (gmail.strip(), password.strip())
    try:
        send_sms_via_email(info[0], message, info[1], sender_credentials)
    except:
        pass