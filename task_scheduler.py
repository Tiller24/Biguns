#!/usr/bin/env python3
from database import database
import time
import os

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

db = Database()


def email(m, s):
    # me == the sender's email address
    # you == the recipient's email address
    msg = MIMEText(m)
    msg['Subject'] = s
    msg['From'] = 'bigunsapp@gmail.com'
    msg['To'] = 'bigunsapp@gmail.com'

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    gmail_user = os.environ['GMAIL_USR']
    gmail_pwd = os.environ['GMAIL_PWD']
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_pwd)
    smtpserver.sendmail(gmail_user, gmail_user, msg.as_string())
    smtpserver.quit()


# attempt to add the most recent biguns
try:
    recent_biguns = db.first_page()  # Get the frontpage for the most recent biguns
    if recent_biguns:
        db.new_playlist(recent_biguns)  # Try to add to the database
        print("Successfully Added to the Database")
        email("Successfully Added to the Database", "Success")
    else:
        print("There is no new biguns")

except Exception as e:
    # TODO: Explane in more detail what error is
    print("There was an exception scraping: ", e)
    email(str(e, 'Error Scraping'))
time.sleep(60)  # delay for 60 seconds
