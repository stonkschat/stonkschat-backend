import logging
import requests

from wsb import app, db
from wsb.models import Thread

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
logger = logging.getLogger("eventLogger")

def getNew():
  r = requests.get("https://www.reddit.com/r/wallstreetbets/new.json?sort=new&limit=100", headers = {'User-agent': 'userAgent001'})

  threads = r.json()["data"]

  for thread in threads["children"]:
    thread = Thread(title=thread["data"]["title"])
    db.session.add(thread)
    db.session.commit()

  logger.info("Threads updated.")