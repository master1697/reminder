import os
from celery import Celery
from celery.utils.log import get_task_logger
import smtplib

app = Celery('tasks', broker=os.getenv("CELERY_BROKER_URL"))
logger = get_task_logger(__name__)

EMAIL = "remindmenotif@gmail.com"
PASSWORD = "xkzgnnyogyoakduo"

@app.task
def send_sms(recipient, message):
    logger.info(f'Adding {recipient} + {message}')
    # SMTP setup and message creation here...
    # ...
    auth = (EMAIL, PASSWORD)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
    server.sendmail(auth[0], recipient, message)
    server.quit()