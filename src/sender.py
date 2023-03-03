import smtplib
import sys
 
CARRIERS = {
  "verizon": "vtext.com",
  "tmobile": "tmomail.net",
  "sprint": "messaging.sprintpcs.com",
  "at&t": "txt.att.net",
  "boost": "smsmyboostmobile.com",
  "cricket": "sms.cricketwireless.net",
  "uscellular": "email.uscc.net",
}
 
EMAIL = "mrfancypants123321@gmail.com"
PASSWORD = "sfmllcrfzemdbthd"
 
def send_message(phone_number, carrier, message):
  recipient = f"{phone_number.strip()}@{(CARRIERS[carrier]).strip()}"
  auth = (EMAIL, PASSWORD)

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(auth[0], auth[1])
  server.sendmail(auth[0], recipient, message)

# phone_number = '7142228402'
# carrier = 'tmobile'
# message = ""

# send_message(phone_number, carrier, message)
