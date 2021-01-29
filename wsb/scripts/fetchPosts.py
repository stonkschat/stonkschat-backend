import logging
import requests

from wsb import app, db
from wsb.models import Post

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
logger = logging.getLogger("eventLogger")

def getNew():
  r = requests.get("https://www.reddit.com/r/wallstreetbets/new.json?sort=new&limit=100", headers = {'User-agent': 'userAgent001'})

  posts = r.json()["data"]

  for post in posts["children"]:
    post = Post(title=post["data"]["title"])
    db.session.add(post)
    db.session.commit()

  logger.info("Posts updated.")