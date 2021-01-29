import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = "W4dNaPqRXjW1eZG2d9vXW4dNaPqRXjW1eZG2d9vX"
  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "posts.db")

  JOBS = [
    # {
    #   "id": "sched_getNew",
    #   "func": "wsb.scraper.fetchPosts2:getNew",
    #   "trigger": "interval",
    #   "minutes": 1
    # }
  ]
  REDDIT_CREDENTIALS = {
    'username':'wsb_api_throwaway',
    'password':'Hunter2',
    'client_id':'xXq6FWhj3Q7dSg',
    'client_secret': 'pehEpglhVFg2MNFByjzwLXmLv6ha1A',
    'user_agent':'testscript by u/fakebot3 but not really i just copy pasted' }
