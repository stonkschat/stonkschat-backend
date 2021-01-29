import praw
from praw.models import MoreComments
import time
import datetime
from wsb.config import Config
from operator import attrgetter
import logging

import json
import socketio

logger = logging.getLogger(__name__)
logger = logging.getLogger("fetchPosts")
# logger.setLevel(logging.INFO)

class Scraper:
    def __init__(self, socketio):
        logger.info("getting born!")
        self.authenticate()
        self.last_comment_time = 0
        self.socketio = socketio


    def get_current_thread(self):
        """
        Get the current live daily discussion thread from today
        """
        subreddit = self.client.subreddit('wallstreetbets')
        dailies = subreddit.search( 'flair:Daily Discussion',time_filter ='day')
        
        freshest = max(dailies,key=attrgetter('created') )
        freshest.comment_sort = "new"
        return freshest

    def is_certified( self, comment ):
        """
        This should be made way more flexible and allow for more filtering
        """
        if isinstance(comment, MoreComments) :
            return( False )
        if comment.author is None or comment.created_utc <= self.last_comment_time:
            return( False )
    
        retard = self.client.redditor( comment.author )
        days_old = ( time.time() - retard.created_utc ) / (60*60*24 )
        logger.debug( "{} is {} days old!".format(comment.author, days_old))
        return( days_old > 700 )

    def authenticate(self):
        logger.info( "authenticating...")
        creds = Config.REDDIT_CREDENTIALS
        self.client =  praw.Reddit(username = creds['username'],            
            password = creds['password'],            
            client_id = creds['client_id'],            
            client_secret = creds['client_secret'],            
            user_agent = creds['user_agent'])     
    

    def run(self, endless = False):
        submission = self.get_current_thread()
        logger.info("let's see what's in {}!".format( submission.title))
        # start the iterator and count down until you run out of comments
        # count down so that we print things in order
        i = min( len(submission.comments)-1, 10 ) # show the last couple comments in case nothing is live

        while True:
            self.socketio.sleep(0.3)
            if i:
                comment = submission.comments[i]
                i -= 1
                if self.is_certified( comment ):
                    try:
                        st = datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                        logger.info("User:{} - {}".format(comment.author, st))
                        logger.info(comment.body )
                        data = { 'body_html':comment.body_html, 'user':comment.author.name, 'timestamp':st}
                        
                        self.socketio.emit( 'new comment', data, broadcast=True)
                        self.last_comment_time = comment.created_utc
                    except:
                        logger.error('uhoh')
            else:  
                if not endless:
                    logger.debug("IM DONE")
                    break 
                submission = self.get_current_thread() # calling constructor refreshes
                submission.comment_sort = "new"
                i = len(submission.comments)-1
                logger.info("waiting for more tendies from {}".format(submission.title))
                self.socketio.sleep(2) #chill
                logger.debug('wake')



logger.info("getting born!")

if __name__ == "__main__":
    logger.info("getting born!")
    # scraper = Scraper(5) #todo make work as console script again
    # scraper.run()
