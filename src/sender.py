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
  to_list = []
  _msg = '''
    From: Watcher Bot
    Subject: Discount Alert
    {_message}
  '''
  recipient = f"{phone_number.strip()}@{(CARRIERS[carrier]).strip()}"
  to_list.append(recipient)
  auth = (EMAIL, PASSWORD)

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(auth[0], auth[1])

  server.sendmail(from_addr=auth[0], to_addrs=to_list, msg=_msg.format(_message=message))

# phone_number = '7142228402'
# carrier = 'tmobile'
# message = "Discount is {num}%"
# send_message(phone_number, carrier, message.format(num=666))
