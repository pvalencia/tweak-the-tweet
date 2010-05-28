#!/usr/bin/env python
# A #Haiti Twitter stream listener for TweakTheTweet using Tweepy.
# Requires Python 2.6
# Requires Tweepy http://github.com/joshthecoder/tweepy
# http://creativecommons.org/licenses/by-nc-sa/3.0/us/
# Based on: http://github.com/joshthecoder/tweepy-examples
# Modifications by @ayman

from textwrap import TextWrapper
import tweepy
import re

# Primary Filter, can be a comma seperated list.
PRIMARY_TRACK_LIST = "#chile, #earthquake, #tsunami, #terremotochile, #fuerzachile"

# Secondary filter, must be a regex.
SECONDARY_REGEX_FILTER = '#(need|offer|have|closed|open|taybien|toybien|tavivo|necesidad|tengo|tenemos|imok|ruok|missing|evac|damage|estasbien|estabien|estoybien|todobien|survivor|sebusca)'

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

class TweetSaverLog(object):
    status_wrapper = TextWrapper(width=70,
                                 initial_indent=' ',
                                 subsequent_indent=' ')

    def save_raw_tweet( self, text, author, tweet_id, source, time ):
        log.info(self.status_wrapper.fill(text))                            
        log.info('%s %s via %s #%s\n' % ( 
                                       author,
                                       time,
                                       source,
                                       tweet_id))

import csv, os
class TweetSaverCSV(object):
    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(self.filename):
            self.writerow(['text', 'author', 'tweet_id', 'source', 'time'])

    def writerow(self,row):
        with open(self.filename, 'a') as destfile:
            writer = csv.writer(destfile, delimiter=';', dialect='excel')
            writer.writerow(row)
    
    def save_raw_tweet(self, text, author, tweet_id, source, time ):
        self.writerow([text, author, tweet_id, source, time])

import MySQLdb
import traceback,sys
class TweetSaverMySQL(object):
    def __init__(self, host, db, user, passwd):
        self.db =  MySQLdb.connect(host = host, user = user ,passwd = passwd ,db = db)
        self.cursor = self.db.cursor()

    def save_raw_tweet(self, text, author, tweet_id, source, time ):
        sql = "INSERT INTO tweets (text, author, tweet_id, source, time) VALUES  ('%s', '%s', '%s', '%s', '%s' )" %  (text, author, tweet_id, source, time)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
            print "Commit"

        except:
            # Rollback in case there is any error
            self.db.rollback()
            print "Rollback"
            traceback.print_exc(file=sys.stdout)



class StreamWatcherListener(tweepy.StreamListener):
    prog = re.compile(SECONDARY_REGEX_FILTER,
                      re.IGNORECASE)

    def __init__(self, u, p, savers):
        self.auth = tweepy.BasicAuthHandler(username = u,
                                            password = p)
        self.api = tweepy.API(auth_handler = self.auth,
                              secure=True,
                              retry_count=3)
        self.savers = savers

    def on_status(self, status):
        log.debug(status.text)

        if self.prog.search(status.text):
            for saver in self.savers:
                saver.save_raw_tweet(status.text,
                                        status.author.screen_name,                                                      
                                        status.id,
                                        status.source,                                                   
                                        status.created_at)

    def on_limit(self, track):
        log.error('Limit hit! Track = %s' % track)

    def on_error(self, status_code):
        log.warn('An error has occured! Status code = %s' % status_code)
        return True # keep stream alive

    def on_timeout(self):
        log.error('Timeout: Snoozing Zzzzzz')

def main():
    try:
        username = 'TtTReadChile'
        password = 'TtT4Chile'
        
        log_saver = TweetSaverLog()
        csv_saver = TweetSaverCSV('tweets.csv')
        mysql_saver = TweetSaverMySQL('localhost', 'test', 'tweakthetweet', 'tweakthetweet')
        listener = StreamWatcherListener(username, password, [log_saver, csv_saver, mysql_saver])
        stream = tweepy.Stream(username,
                               password,
                               listener,
                               timeout = None)
        track_list = [k for k in PRIMARY_TRACK_LIST.split(',')]

        stream.filter(track = track_list)
    except KeyboardInterrupt:
        print '\nCiao!'

if __name__ == '__main__':
    main()
