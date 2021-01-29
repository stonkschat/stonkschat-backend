import praw
from praw.models import MoreComments
import time
import datetime
import redcreds # file with your credentials
from operator import attrgetter

class Scraper:
    def __init__(self):
        self.authenticate()

    def get_current_thread(self):
        """
        Get the current live daily discussion thread from today
        """
        subreddit = self.client.subreddit('wallstreetbets')
        dailies = subreddit.search( 'flair:Daily Discussion',time_filter ='day')
        
        freshest = max(dailies,key=attrgetter('created') )
        freshest.comment_sort = "new"
        return freshest

    def is_certified( self, comment , cutoff, ):
        """
        This should be made way more flexible and allow for more filtering
        """
        if isinstance(comment, MoreComments) :
            return( False )
        if comment.author is None or comment.created_utc <= cutoff:
            return( False )
    
        retard = self.client.redditor( comment.author )
        days_old = ( time.time() - retard.created_utc ) / (60*60*24 )
        return( days_old > 700 )

    def authenticate(self):
        print( "authenticating...")
        creds = redcreds.creds
        self.client =  praw.Reddit(username = creds['username'],            
            password = creds['password'],            
            client_id = creds['client_id'],            
            client_secret = creds['client_secret'],            
            user_agent = creds['user_agent'])     
    

    def run(self):
        submission = self.get_current_thread()
        print("let's see what's in {}!".format( submission.title))

        # start the iterator and count down until you run out of comments
        # count down so that we print things in order
        i = min( len(submission.comments)-1, 10 ) # show the last couple comments in case nothing is live
        last_comment_time = 0
        
        while True:
            if i:
                comment = submission.comments[i]
                i -= 1
                if self.is_certified( comment, last_comment_time ):
                    st = datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    print("\n\nUser:{} - {}".format(comment.author, st))
                    print(comment.body )
                    last_comment_time = comment.created_utc
            else:    
                submission = self.get_current_thread() # calling constructor refreshes
                submission.comment_sort = "new"
                i = len(submission.comments)-1
                print("waiting for more tendies from {}".format(submission.title))
                time.sleep(10) #chill

if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
