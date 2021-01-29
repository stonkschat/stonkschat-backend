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
    thread = thread["data"]

    if (Thread.query.filter_by(thread_id=thread["id"]).scalar() is None):
      post = Thread(thread_id=thread["id"], title=thread["title"], author=thread["author"])
      if thread["selftext"]:
        post.content = thread["selftext"]
      
      if thread["media"]:
        if thread["is_video"]:
          post.video_url = thread["media"]["reddit_video"]["fallback_url"]

      db.session.add(post)

  db.session.commit()

  logger.info("Threads updated.")