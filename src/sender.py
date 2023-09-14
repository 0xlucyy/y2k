import smtplib
from src.config import _Base


CARRIERS = _Base.CARRIERS
EMAIL = _Base.EMAIL
PASSWORD = _Base.PASSWORD
PHONE_NUM = _Base.PHONE_NUM
 
def send_message(phone_number: str, carrier: str, message: str) -> bool:
  '''
  Sends a message to a phone.
  '''
  try:
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
    return True
  except Exception as error:
    return False

''' Working test which sends a msg to a phone '''
# phone_number = PHONE_NUM
# carrier = 'tmobile'
# message = "Discount is {num}%"
# send_message(phone_number, carrier, message.format(num=123))
