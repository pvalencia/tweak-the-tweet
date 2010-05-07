#!/usr/bin/env python
# A #Haiti Twitter stream listener for TweakTheTweet using Tweepy.
# Requires Python 2.6
# Requires Tweepy http://github.com/joshthecoder/tweepy
# http://creativecommons.org/licenses/by-nc-sa/3.0/us/
# Based on: http://github.com/joshthecoder/tweepy-examples
# Modifications by @ayman
 
import time
from getpass import getpass
from textwrap import TextWrapper
import tweepy
import re
import pprint
import MySQLdb
 
# Primary Filter, can be a comma seperated list.
PRIMARY_TRACK_LIST = "#chile, #earthquake, #tsunami, #terremotochile, #fuerzachile"

# Secondary filter, must be a regex.
SECONDARY_REGEX_FILTER = '#(need|offer|have|closed|open|taybien|toybien|tavivo|necesidad|tengo|tenemos|imok|ruok|missing|evac|damage|estasbien|estabien|estoybien|todobien|survivor|sebusca)'

  
class StreamWatcherListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=70,
                                 initial_indent=' ',
                                 subsequent_indent=' ')
    prog = re.compile(SECONDARY_REGEX_FILTER,
                      re.IGNORECASE)
 
    def __init__(self, u, p):
        self.auth = tweepy.BasicAuthHandler(username = u,
                                            password = p)
        self.api = tweepy.API(auth_handler = self.auth,
                              secure=True,
                              retry_count=3)
        return
 
    def on_status(self, status):
        global db
        global cursor
        
        try:           
            if self.prog.search(status.text):
 
                print self.status_wrapper.fill(status.text)
                print '%s %s via %s #%s\n' % (status.author.screen_name,
                                           status.created_at,
                                           status.source,
                                           status.id)
            
                sql = "INSERT INTO tweets (text, author, tweet_id, source, time) VALUES  ('%s', '%s', '%s', '%s', '%s' )" % \
                    (status.text, status.author.screen_name, status.id, status.source, status.created_at)
 
                try:
                    # Execute the SQL command
                    cursor.execute(sql)
                    # Commit your changes in the database
                    db.commit()
                    print "Commit"
            
                except:
                    # Rollback in case there is any error
                    db.rollback()
                    print "Rollback"
                  
        except:
            # Catch any unicode errors while printing to console and
            # just ignore them to avoid breaking application.
            pass
        return
 
    def on_limit(self, track):
        print 'Limit hit! Track = %s' % track
        return
 
    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True # keep stream alive
 
    def on_timeout(self):
        print 'Timeout: Snoozing Zzzzzz'
        return
 
def main():    
    username = raw_input('Twitter username: ')
    password = getpass('Twitter password: ')

    global db
    global cursor
    
    db = MySQLdb.connect (host = "localhost",
        user = "root",
        passwd = "",
        db = "haiti_db")
    cursor = db.cursor () 

    listener = StreamWatcherListener(username, password)
    stream = tweepy.Stream(username,
                           password,
                           listener,
                           timeout = None)
    track_list = [k for k in PRIMARY_TRACK_LIST.split(',')]
    stream.filter(track = track_list)
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nCiao!'
        db.close